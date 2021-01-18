#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Geral
#
# Created:     25/06/2020
# Copyright:   (c) Geral 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from pylab import *
import numpy as np
import reikna.cluda as cluda
from reikna.fft import FFT as FFTcl

api = cluda.ocl_api()

thr = api.Thread.create()

a = ones((512,512),dtype=np.complex64)

dims = a.shape

res_dev = thr.array(dims, dtype=np.complex64)


a_dev = thr.to_device(a)

FFT = FFTcl(a_dev).compile(thr)


FFT(res_dev, a_dev)

res_cl = res_dev.get()

diffracted = np.fft.fftshift(np.abs(res_cl))


pcolormesh(diffracted)
show()

