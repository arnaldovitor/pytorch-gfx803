## Installing PyTorch 2.1.2 with ROCm Support on Linux Mint 21.2

This tutorial guides you through installing PyTorch 2.1.2 with ROCm support on Linux Mint 21.2 using a Radeon RX 480/580 8GB GPU.

### Prerequisites

Ensure your system meets the following requirements:

- **Linux Kernel:** Version 5.19.0-50-generic is required for compatibility with ROCm 5.5.
- **ROCm:** Version 5.5 is installed.
- **Python:** Version 3.10.6.

### Step 1: Downgrade Kernel (if necessary)

If your current kernel is newer than 5.19.0-50-generic, downgrade to this version:

```bash
KERN="5.19.0-50-generic"
sudo apt install "linux-image-$KERN" "linux-headers-$KERN" "linux-modules-$KERN" "linux-modules-extra-$KERN"
```

### Step 2: Install Dependencies

Install necessary dependencies for ROCm and PyTorch:

```bash
sudo apt autoremove rocm-core amdgpu-dkms
sudo apt install libopenmpi3 libstdc++-12-dev libdnnl-dev ninja-build libopenblas-dev libpng-dev libjpeg-dev
```

### Step 3: Install ROCm

Configure ROCm environment variables and install ROCm 5.5:

```bash
echo -e "ROC_ENABLE_PRE_VEGA=1\nHSA_OVERRIDE_GFX_VERSION=8.0.3" | sudo tee -a /etc/environment
sudo reboot

wget "https://repo.radeon.com/amdgpu-install/5.5/ubuntu/jammy/amdgpu-install_5.5.50500-1_all.deb"
sudo apt install ./amdgpu-install_5.5.50500-1_all.deb
sudo amdgpu-install -y --usecase=rocm,hiplibsdk,mlsdk

sudo usermod -aG video $LOGNAME
sudo usermod -aG render $LOGNAME
```

Verify ROCm installation:

```bash
rocminfo
rocm-smi
clinfo
```

### Step 4: Install PyTorch

Download and install torch and torchvision using the wheels built at [viebrix's releases](https://github.com/viebrix/pytorch-gfx803/releases/tag/V2.1.2) or from our Google Drive for guaranteed availability:

- [Google Drive link](https://drive.google.com/drive/folders/1guggUGdQve5n5ZvnvXaighnQhgAo8LBB?usp=sharing)


```bash
pip install torch-2.1.2-cp310-cp310-linux_x86_64.whl
pip install torchvision-0.16.2-cp310-cp310-linux_x86_64.whl
pip install numpy==1.21.5 --force-reinstall  # Resolve NumPy initialization issue
```

### Step 5: Test Installation

Verify PyTorch installation by running a test script:

```bash
python3.10 test_torch.py
```

---

This guide should help you install PyTorch 2.1.2 with ROCm support smoothly on your system. If you encounter any issues, feel free to refer to [viebrix's repository](https://github.com/viebrix) or raise an issue for assistance.
