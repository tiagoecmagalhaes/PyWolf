#    PyWolf

PyWolf is a software that simulates the propagation of partially coherent light using parallel computing devices through PyOpenCL to decrease the computation time. 

## Support

PyWolf is build in Python 3.7.6. It was tested in Windows 10 (x64) and Ubuntu 20.04.

## Installation

To use PyWolf, the user need to install the following packages:

- NumPy (numeric)
- SciPy (scientific)
- Matplolib (data plots)
- PyOpenCL (parallel computing)
- PyQT5 (graphical user interface)
- psutil (only necessary to view the available RAM)

Using the package manager pip to install packages:

```bash
pip install numpy
pip install scipy
pip install matplotlib
pip install PyQt5
pip install psutil
```

To install PyOpenCL, one can try:

```bash
pip install pyopencl
```

If installing through pip does not work, Windows users can download the PyOpenCL package (.whl) in [Christoph Gohlke' website](https://www.lfd.uci.edu/~gohlke/pythonlibs/), which contains Windows Binaries for Python Extension Packages. 

## Usage

To start PyWolf, execute main.py and a PyQT5 window will appear (see Fig. 1).

## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)



