#    PyWolf

PyWolf is a software that simulates the propagation of partially coherent light using parallel computing devices through PyOpenCL to decrease the computation time. 



Please see the following articless for more technical details: 

- https://doi.org/10.1016/j.cpc.2022.108336
- https://arxiv.org/abs/2203.02734



If you find this software useful for your research, please cite: 

> Tiago E.C. Magalhães, José M. Rebordão, "PyWolf: A PyOpenCL implementation for simulating the propagation of partially coherent light", Computer Physics Communications, Volume 276, 2022, 108336. [DOI](https://doi.org/10.1016/j.cpc.2022.108336)

> Tiago E.C. Magalhães, Daniela O. Santos, "A new version of PyWolf for the propagation of partially coherent light in media other than free space", Computer Physics Communications, Volume 294, 2024. [DOI](https://doi.org/10.1016/j.cpc.2023.108899)

## Support

PyWolf is build in Python 3.7.6 (x64). It was mostly implemented in Windows 10 (x64). It was tested in the following operating systems:

- Windows 7 (x64)
- Windows 8/8.1 (x64)
- Windows 10 (x64)
- Ubuntu 20.04.3 LTS (x64)

## Installation

To use PyWolf, the user needs to install the following packages:

- NumPy (numeric)
- SciPy (scientific)
- Matplolib (plots)
- PyOpenCL (parallel computing)
- PyQt5 (graphical user interface)
- psutil (only necessary to view the available RAM)

Using the package manager pip to install packages:

```bash
pip install numpy
pip install scipy
pip install matplotlib
pip install PyQt5
pip install psutil
```
Additionally, to load images, one needs to install Python's OpenCV. Using the package manager pip:
```bash
pip install opencv-python
```

**Install the PyOpenCL Python's package (cl12).**

- Windows users can download the PyOpenCL package (.whl) in [Christoph Gohlke' website](https://www.lfd.uci.edu/~gohlke/pythonlibs/), which contains Windows Binaries for Python Extension Packages. For best compatibility, we recomend the OpenCL 1.2 version (denoted in the package's name by "cl12"). Make sure to download and install the package with your Python version (e.g. *pyopencl‑2021.1.3+cl12‑cp37‑cp37m‑win_amd64.whl* for Python 3.7 x64). 
- Linux users (e.g., Ubuntu) can install PyOpenCL using the terminal: ```python3 -m pip install PyOpenCL```

Optionally, one can also install OpenCL SDK to have more OpenCL platforms available. For example:

- [Intel](https://software.intel.com/content/www/us/en/develop/tools/opencl-sdk.html) (Recommended for PyWolf)
- [NVIDIA](https://developer.nvidia.com/cuda-toolkit-32-downloads)
- [AMD](https://github.com/GPUOpen-LibrariesAndSDKs/OCL-SDK/releases) (Windows)

## Usage

To start PyWolf, execute main.py and a PyQT5 window will appear (see figure below).

![main](https://github.com/tiagoecmagalhaes/PyWolf/blob/master/screenshots/fig1.jpg?raw=true "Fig. 1")



## Troubleshooting

- When PyOpenCL is not correctly installed, the following error usually appears in the Python interpreter:

  `from pyopencl._cl import bitlog2  # noqa: F401
  ImportError: DLL load failed:`

- For Windows 7 users, the update [Universal C Runtime in Windows](https://support.microsoft.com/en-us/topic/update-for-universal-c-runtime-in-windows-c0514201-7fe6-95a3-b0a5-287930f3560c) must be installed.

- For Linux users (e.g., Ubuntu), if PyWolf crashes with the message "Backend terminated or disconnected.", it may be due to the lack of RAM available. Try decreasing the matrix size N or decrease the usage of RAM in other applications. 

## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)



