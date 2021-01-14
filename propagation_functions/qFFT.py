# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Name:        FFT
# Purpose:     PyProPCL
#
# Author:      Tiago Magalhaes
#
# Created:     2017
# Copyright:   (c) Tiago Magalhaes 2017
# Licence:     IA
#-----------------------------------------------------------------------------
##
##
#==============================================================================
# Where do things come from?
#==============================================================================


from numpy import zeros, complex64
from pylab import *

#import multiprocessing
#import pyfftw

from scipy import fft

import copy

#import reikna.cluda as cluda
#from reikna.fft import FFT as FFTcl




#from pylab import fftshift

#from numpy import fft
#from numpy import zeros
#from numpy import complex64
#from numpy.fft import fftshift
#------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
#
#
#==============================================================================
# FFT OLD
#==============================================================================

def func_fft2d_OLD(ui,data_in,FTinverse,zeropad=[]):
    "Returns the 2D Fourier Transform"
    if FTinverse:
        if zeropad[0]:

            N = data_in.shape[0]

            Np = int(zeropad[1])

            M1 = int(Np/2-N/2)
            M2 = int(Np/2+N/2)

            new_data = zeros((Np,Np), dtype=complex64)
            out_data = pyfftw.empty_aligned((Np,Np), dtype='complex64')


            new_data[M1:M2,M1:M2] = data_in


            #new_fft = ifftshift(ifft2(ifftshift(new_data)))
            new_fft = pyfftw.FFTW(fft.ifftshift(new_data), out_data,axes=(0,1),direction='FFTW_BACKWARD',threads=multiprocessing.cpu_count())
            return fft.ifftshift(out_data[M1:M2,M1:M2])

        else:
            N = data_in.shape[0]
            out_data = pyfftw.empty_aligned((N,N), dtype='complex64')
            new_fft = pyfftw.FFTW(fft.ifftshift(data_in), out_data,axes=(0,1),direction='FFTW_BACKWARD',threads=multiprocessing.cpu_count())
            return fft.ifftshift(out_data)


    else:
        if zeropad[0]:

            N = data_in.shape[0]

            Np = int(zeropad[1])

            M1 = int(Np/2-N/2)
            M2 = int(Np/2+N/2)

            new_data = zeros((Np,Np), dtype=complex64)
            out_data = pyfftw.empty_aligned((Np,Np), dtype='complex64')

            new_data[M1:M2,M1:M2] = data_in
            #new_fft = fftshift(fft2(fftshift(new_data)))
            new_fft = pyfftw.FFTW(fft.fftshift(new_data), out_data,axes=(0,1),direction='FFTW_FORWARD',threads=multiprocessing.cpu_count())
            return fft.fftshift(out_data[M1:M2,M1:M2])

        else:
            N = data_in.shape[0]
            out_data = pyfftw.empty_aligned((N,N), dtype='complex64')
            new_fft = pyfftw.FFTW(fft.fftshift(data_in),out_data,axes=(0,1),direction='FFTW_FORWARD',threads=multiprocessing.cpu_count())
            return fft.fftshift(out_data)





#------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------



#==============================================================================
# FFT ORIGINAL
#==============================================================================

def func_fft2d(ui,data_in,FTinverse,zeropad=[]):
    "Returns the 2D Fourier Transform"
    if FTinverse:
        if zeropad[0]:

            N = data_in.shape[0]

            Np = int(zeropad[1])

            M1 = int(Np/2-N/2)
            M2 = int(Np/2+N/2)

            new_data = zeros((Np,Np), dtype=complex64)


            new_data[M1:M2,M1:M2] = data_in

            new_fft = ifftshift(ifft2(ifftshift(new_data)))
            return new_fft[M1:M2,M1:M2]

        else:
            return (ifftshift(ifft2(ifftshift(data_in))))


    else:
        if zeropad[0]:

            N = data_in.shape[0]

            Np = int(zeropad[1])

            M1 = int(Np/2-N/2)
            M2 = int(Np/2+N/2)

            new_data = zeros((Np,Np), dtype=complex64)
            new_data[M1:M2,M1:M2] = data_in

            new_fft = fftshift(fft2(fftshift(new_data)))
            return new_fft[M1:M2,M1:M2]

        else:
            return (fftshift(fft2(fftshift(data_in))))




#------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------


#==============================================================================
# FFT MOD
#==============================================================================

def func_fft2d_as(ui,data_in,FTinverse,zeropad=[],api=0,thr=0,FFT=0,a_dev=0):
    "Returns the 2D Fourier Transform"
    if FTinverse:
        if zeropad[0]:

            N = data_in.shape[0]

            Np = int(zeropad[1])

            M1 = int(Np/2-N/2)
            M2 = int(Np/2+N/2)

            new_data = zeros((Np,Np), dtype=complex64)


            new_data[M1:M2,M1:M2] = data_in

            a = ifftshift(new_data)
            dims = a.shape

            # results to device
            res_dev = thr.array(dims, dtype=complex64)

            # data do device
            a_dev = thr.to_device(a)

            # performing FFT
            #FFT = FFTcl(a_dev).compile(thr)

            # copying results to res_dev
            FFT(res_dev, a_dev,inverse=True)


            res_cl = res_dev.get()

            new_fft = ifftshift(res_cl)

            return new_fft[M1:M2,M1:M2]

        else:

            a = ifftshift(data_in)
            dims = a.shape

            # results to device
            res_dev = thr.array(dims, dtype=complex64)

            # data do device
            a_dev = thr.to_device(a)

            # performing FFT
            #FFT = FFTcl(a_dev).compile(thr)

            # copying results to res_dev
            FFT(res_dev, a_dev,inverse=True)
            res_cl = res_dev.get()

            new_fft = ifftshift(res_cl)

            return new_fft


    else:
        if zeropad[0]:

            N = data_in.shape[0]

            Np = int(zeropad[1])

            M1 = int(Np/2-N/2)
            M2 = int(Np/2+N/2)

            new_data = zeros((Np,Np), dtype=complex64)
            new_data[M1:M2,M1:M2] = data_in


            a = fftshift(new_data)
            dims = a.shape

            # results to device
            res_dev = thr.array(dims, dtype=complex64)

            # data do device
            a_dev = thr.to_device(a)

            # performing FFT
            #FFT = FFTcl(a_dev).compile(thr)

            # copying results to res_dev
            FFT(res_dev, a_dev)
            res_cl = res_dev.get()

            new_fft = fftshift(res_cl)

            return new_fft[M1:M2,M1:M2]

        else:

            a = fftshift(data_in)
            dims = a.shape

            # results to device
            res_dev = thr.array(dims, dtype=complex64)

            # data do device
            a_dev = thr.to_device(a)

            # performing FFT
            #FFT = FFTcl(a_dev).compile(thr)

            # copying results to res_dev
            FFT(res_dev, a_dev)
            res_cl = res_dev.get()

            new_fft = fftshift(res_cl)

            return new_fft




#------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------
