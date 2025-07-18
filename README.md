# CEINMS

CEINMS (Calibrated EMG-Informed Neuromusculoskeletal Modelling System) is a framework for estimating muscle forces and activations. **Note: CEINMS is only compatible with Windows operating systems.**


## Installation of Miniconda

1. Download the latest version of Miniconda and install it via powershell:
   - **Windows**: [Miniconda Windows quickstart install](https://www.anaconda.com/docs/getting-started/miniconda/install#quickstart-install-instructions) *OR* [Minconda Windows classic install via EXE](https://www.anaconda.com/download/)

3. Initialize Conda for PowerShell:
   - Open the Anaconda Prompt (can be found in the Start Menu)
   - Run the following command:
   ```
   conda init powershell
   ```
   - After this initialization, conda commands will be available in all PowerShell windows
   - Close and reopen any existing PowerShell windows

4. Verify the installation in powershell:
   ```powershell
   conda --version
   ```

## Setting up a CEINMS environment

Create and activate a new conda environment for CEINMS in powershell:

```powershell
conda create -n ceinms python=3.11 numpy
conda activate ceinms
```

## Installing OpenSim

1. Install Opensim via conda in powershell:
   ```powershell
   conda install opensim-org::opensim 
   ```

2. Verify the installation via powershell:
   ```powershell
   python -c "import opensim; print(opensim.__version__)"
   ```

## Install Requirements *if necessary*

Install all required dependencies via powershell:

```powershell
pip install -r requirements.txt
```

## Installing msk package
```powershell
pip install msk-modelling-python
```

