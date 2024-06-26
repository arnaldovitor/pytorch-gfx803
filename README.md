# pytorch-rocm-gfx803

This is a tutorial for installing PyTorch 2.1.2 with ROCm support based on the repository by [viebrix](https://github.com/viebrix) (for which I am very grateful). For any questions or suggestions, you can create an issue, and I will respond as soon as possible

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

# Verify
rocminfo
rocm-smi
clinfo
```

## Install PyTorch

Download and install torch and torchvision using the wheels built at: https://github.com/viebrix/pytorch-gfx803/releases/tag/V2.1.2

```bash
pip install torch-2.1.2-cp310-cp310-linux_x86_64.whl
pip install torchvision-0.16.2-cp310-cp310-linux_x86_64.whl
pip install numpy==1.21.5 --force-reinstall # This is necessary to avoid the warning: "Failed to initialize NumPy: _ARRAY_API not found"
```

## Test

```bash
python3.10 test_torch.py
```
