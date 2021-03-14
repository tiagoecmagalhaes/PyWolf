#    PyWolf

PyWolf is a software that simulates the propagation of partially coherent light using parallel computing devices through PyOpenCL to decrease the computation time. 

## Support

PyWolf is build in Python 3.7.6 (x64). It was implemented and tested in Windows 10 (x64).

## Installation

To use PyWolf, the user need to install the following packages:

- NumPy (numeric)
- SciPy (scientific)
- Matplolib (data plots)
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

**To install PyOpenCL, one can follow two steps:**

1. Install OpenCL SDK. For example:
   - [Intel](https://software.intel.com/content/www/us/en/develop/tools/opencl-sdk.html) (Recomended for PyWolf)
   - [NVIDIA](https://developer.nvidia.com/cuda-toolkit-32-downloads)
   - [AMD](https://github.com/GPUOpen-LibrariesAndSDKs/OCL-SDK/releases) (Windows)
2. Install the PyOpenCL Python's package.
   - Windows users can download the PyOpenCL package (.whl) in [Christoph Gohlke' website](https://www.lfd.uci.edu/~gohlke/pythonlibs/), which contains Windows Binaries for Python Extension Packages. For best compatibility, we recomend the OpenCL 1.2 version (denoted in the package's name by "cl12"). Make sure to download and install the package with your Python version (e.g. *pyopencl‑2021.1.3+cl12‑cp37‑cp37m‑win_amd64.whl* for Python 3.7 x64). 

## Usage

To start PyWolf, execute main.py and a PyQT5 window will appear (see Fig. 1).

![main](https://github.com/tiagoecmagalhaes/PyWolf/blob/master/screenshots/fig1.jpg?raw=true "Fig. 1")



## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)



