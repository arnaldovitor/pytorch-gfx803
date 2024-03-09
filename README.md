# PyTorch ROCm gfx803

build pytorch 2.1.2 with ROCm support for automatic stable-diffusion-webui

```
Linux Mint 21.2
Kernel 5.19.0-50-generic
Radeon RX 480/580 8GB
RoCm 5.5

Python 3.10.6
- pytorch 2.1.2
- torchvision 0.16.2
```

## Kernel version requirement
The installation procedure involves building the kernel modules from the `amdgpu-dkms` package. DKMS from ROCm 5.5 will **not** build on kernels above 5.19 such as 6.2.x and 6.5.x that are already available in Linux Mint repos. At the time of writing the latest kernel version where `amdgpu-dkms` works is **5.19.0-50**. Make sure to downgrade in advance if you run a freshier kernel.
```bash
KERN="5.19.0-50-generic"
sudo apt install "linux-image-$KERN" "linux-headers-$KERN" "linux-modules-$KERN" "linux-modules-extra-$KERN"
```
If you are running v5.19 already but you have freshier kernels installed then DKMS *might* quietly fail to build, breaking `dpkg` installation routines.

## Install dependencies

```bash
sudo apt autoremove rocm-core amdgpu-dkms
sudo apt install libopenmpi3 libstdc++-12-dev libdnnl-dev ninja-build libopenblas-dev libpng-dev libjpeg-dev
```

## Install ROCm

```bash
echo -e "ROC_ENABLE_PRE_VEGA=1\nHSA_OVERRIDE_GFX_VERSION=8.0.3" | sudo tee -a /etc/environment
# Reboot after this

wget "https://repo.radeon.com/amdgpu-install/5.5/ubuntu/jammy/amdgpu-install_5.5.50500-1_all.deb"
sudo apt install ./amdgpu-install_5.5.50500-1_all.deb
sudo amdgpu-install -y --usecase=rocm,hiplibsdk,mlsdk

sudo usermod -aG video $LOGNAME
sudo usermod -aG render $LOGNAME

# verify
rocminfo
rocm-smi
clinfo
```

## Build

You may need to install addional dependencies, and the build will take a long time.

#in home directory create directory pytorch2.1.2
#Build Torch
```bash
cd pytorch2.1.2
git clone --recursive "https://github.com/pytorch/pytorch.git" -b v2.1.2
cd pytorch
pip install cmake mkl mkl-include
pip install -r requirements.txt
sudo ln -s /usr/lib/x86_64-linux-gnu/librt.so.1 /usr/lib/x86_64-linux-gnu/librt.so
export PATH=/opt/rocm/bin:$PATH ROCM_PATH=/opt/rocm HIP_PATH=/opt/rocm/hip
export PYTORCH_ROCM_ARCH=gfx803
export PYTORCH_BUILD_VERSION=2.1.2 PYTORCH_BUILD_NUMBER=1
export USE_CUDA=0 USE_ROCM=1 USE_NINJA=1
python3 tools/amd_build/build_amd.py
python3 setup.py bdist_wheel
```

### Build torchvision

```bash
cd ..
git clone "https://github.com/pytorch/vision.git" -b v0.16.2
cd vision
export BUILD_VERSION=0.16.2
FORCE_CUDA=1 ROCM_HOME=/opt/rocm/ python3 setup.py bdist_wheel
```

### install in Automatic SD WebUI

```bash
cd ..

git clone "https://github.com/AUTOMATIC1111/stable-diffusion-webui"
cd stable-diffusion-webui
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip wheel
pip uninstall torch torchvision
pip3 install /home/*******/pytorch2.1.2/pytorch/dist/torch-2.1.2-cp310-cp310-linux_x86_64.whl
pip3 install /home/*******/pytorch2.1.2/vision/dist/torchvision-0.16.2-cp310-cp310-linux_x86_64.whl
pip list | grep 'torch'
```
******* is your home directory username

## Test

```bash
# maybe you need: python setup.py develop && python -c "import torch"
python3.10 test_torch.py
```

## Reference

- https://github.com/RadeonOpenCompute/ROCm/issues/1659
- https://github.com/xuhuisheng/rocm-gfx803
- https://github.com/xuhuisheng/rocm-gfx803/issues/27#issuecomment-1534048619
- https://github.com/Tokoshie/pytorch-gfx803/releases/tag/v2.1.0a0
- https://github.com/xuhuisheng/rocm-gfx803/issues/27#issuecomment-1892611849
- https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki
