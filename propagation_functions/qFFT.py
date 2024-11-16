#-------------------------------------------------------------------------------
# Name:        FFT Function
# Purpose:     PyWolf functions for Fourier Transform
#
# Author:      TEC MAGALHAES
#
# Licence:     GNU GENERAL PUBLIC LICENSE Version 3
#-------------------------------------------------------------------------------


#===============================================================================
# Importing Packages
#===============================================================================

from numpy import zeros, complex64, count_nonzero, empty_like#, fft

from scipy import fft

import copy, time

import threading


#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================

################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################


#==============================================================================
# THREADING FUNCTIONS
#==============================================================================


def fft2d_slice(data_slice, result_slice):
    """Perform 2D FFT on a single slice of the 3D matrix."""
    for i in range(data_slice.shape[0]):
        result_slice[i] = fft.fftshift(fft.fft2(fft.ifftshift(data_slice[i])))


def perform_fft_3d(matrix, N_threads):
    """Perform 2D FFT on each 2D slice of a 3D complex matrix using threads."""
    threads = []
    results = empty_like(matrix, dtype=complex64)

    NN = int(matrix.shape[0]/N_threads)

    for i in range(N_threads):
        thread = threading.Thread(target=fft2d_slice, args=(matrix[i*NN:(i+1)*NN], results[i*NN:(i+1)*NN]))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return results


def ifft2d_slice(data_slice, result_slice):
    """Perform 2D FFT on a single slice of the 3D matrix."""
    for i in range(data_slice.shape[0]):
        result_slice[i] = fft.fftshift(fft.ifft2(fft.ifftshift(data_slice[i])))


def perform_ifft_3d(matrix, N_threads):
    """Perform 2D FFT on each 2D slice of a 3D complex matrix using threads."""
    threads = []
    results = empty_like(matrix, dtype=complex64)

    NN = int(matrix.shape[0]/N_threads)

    for i in range(N_threads):

        thread = threading.Thread(target=ifft2d_slice, args=(matrix[i*NN:(i+1)*NN], results[i*NN:(i+1)*NN]))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return results
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================



#==============================================================================
# THREADING FUNCTIONS - zero padding
#==============================================================================


def fft2d_slice_zp(data_slice, result_slice, zeropad):
    """Perform 2D FFT on a single slice of the 3D matrix."""
    for i in range(data_slice.shape[0]):
        if count_nonzero(data_slice.real)!=0:
            N = data_slice.shape[0]

            Np = int(zeropad[1])

            M1 = int(Np/2-N/2)
            M2 = int(Np/2+N/2)

            new_data = zeros((Np,Np), dtype=complex64)

            new_data[M1:M2,M1:M2] = data_slice[i]

            result_slice[i] = fft.ffftshift(fft.fft2(fft.ifftshift(new_data)))[M1:M2,M1:M2]

def perform_fft_3d_zp(matrix, N_threads, zeropad):
    """Perform 2D FFT on each 2D slice of a 3D complex matrix using threads."""
    threads = []
    results = empty_like(matrix, dtype=complex64)

    NN = int(matrix.shape[0]/N_threads)

    for i in range(N_threads):
        thread = threading.Thread(target=fft2d_slice_zp, args=(matrix[i*NN:(i+1)*NN], results[i*NN:(i+1)*NN], zeropad))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return results


def ifft2d_slice_zp(data_slice, result_slice, zeropad):
    """Perform 2D FFT on a single slice of the 3D matrix."""
    for i in range(data_slice.shape[0]):
        if count_nonzero(data_slice.real)!=0:

            N = data_slice.shape[0]

            Np = int(zeropad[1])

            M1 = int(Np/2-N/2)
            M2 = int(Np/2+N/2)

            new_data = zeros((Np,Np), dtype=complex64)

            new_data[M1:M2,M1:M2] = data_slice[i]

            result_slice[i] = fft.fftshift(fft.ifft2(fft.ifftshift(new_data)))[M1:M2,M1:M2]


def perform_ifft_3d_zp(matrix, N_threads, zeropad):
    """Perform 2D FFT on each 2D slice of a 3D complex matrix using threads."""
    threads = []
    results = empty_like(matrix, dtype=complex64)

    NN = int(matrix.shape[0]/N_threads)

    for i in range(N_threads):

        thread = threading.Thread(target=ifft2d_slice_zp, args=(matrix[i*NN:(i+1)*NN], results[i*NN:(i+1)*NN], zeropad))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return results
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# FFT
#===============================================================================

def func_fft2d(ui, data_in, useThreads, FTinverse,zeropad=[]):
    "Returns the 2D Fourier Transform"

    N = data_in.shape[0]

    #-----------------------------------------------------------
    # USING THREADS
    #-----------------------------------------------------------
    if useThreads[0]:
        ui.update_outputText("Multithreading will be used.")
        ui.update_outputText("___")

        if FTinverse:

            if zeropad[0]:

                for i in range(0, data_in.shape[0]):
                    ui.update_outputTextSameLine(str(round(i*100./N,1))+"% concluded ("+str(i)+"/"+str(N-1)+").")

                    new_fft = perform_ifft_3d_zp(data_in[i], useThreads[1], zeropad)

                    data_in[i] =  new_fft

                return data_in

            else:

                for i in range(0, data_in.shape[0]):
                    ui.update_outputTextSameLine(str(round(i*100./N,1))+"% concluded ("+str(i)+"/"+str(N-1)+").")

                    data_in[i] = perform_ifft_3d(data_in[i], useThreads[1])

                return data_in

        else:

            if zeropad[0]:

                for i in range(0, data_in.shape[0]):
                    ui.update_outputTextSameLine(str(round(i*100./N,1))+"% concluded ("+str(i)+"/"+str(N-1)+").")

                    new_fft = perform_fft_3d_zp(data_in[i], useThreads[1], zeropad)

                    data_in[i] =  new_fft

                return data_in

            else:

                for i in range(0, data_in.shape[0]):
                    ui.update_outputTextSameLine(str(round(i*100./N,1))+"% concluded ("+str(i)+"/"+str(N-1)+").")

                    data_in[i] = perform_fft_3d(data_in[i], useThreads[1])

            return data_in
    #-----------------------------------------------------------
    #///////////////////////////////////////////////////////////
    #-----------------------------------------------------------


    #-----------------------------------------------------------
    # WITHOUT THREADS
    #-----------------------------------------------------------
    else:
        ui.update_outputText("Multithreading will NOT be used...")

        if FTinverse:

            if zeropad[0]:

                ui.update_outputText("Zero padding will be used.")
                ui.update_outputText("___")

                for i in range(0, data_in.shape[0]):
                    ui.update_outputTextSameLine(str(round(i*100./N,1))+"% concluded ("+str(i)+"/"+str(N-1)+").")
                    for j in range(0, data_in.shape[1]):

                        if count_nonzero(data_in[i][j].real)!=0:

                            N = data_in[i,j].shape[0]

                            Np = int(zeropad[1])

                            M1 = int(Np/2-N/2)
                            M2 = int(Np/2+N/2)

                            new_data = zeros((Np,Np), dtype=complex64)


                            new_data[M1:M2,M1:M2] = data_in[i][j]

                            new_fft = fft.ifftshift(fft.ifft2(fft.ifftshift(new_data)))
                            data_in[i][j] = new_fft[M1:M2,M1:M2]

                return data_in

            else:
                ui.update_outputText("___")
                for i in range(0, data_in.shape[0]):
                    ui.update_outputTextSameLine(str(round(i*100./N,1))+"% concluded ("+str(i)+"/"+str(N-1)+").")
                    for j in range(0, data_in.shape[1]):
                        if count_nonzero(data_in[i][j].real)!=0:
                            data_in[i][j] = fft.ifftshift(fft.ifft2(fft.ifftshift(data_in[i][j])))

                return data_in
        else:
            if zeropad[0]:
                ui.update_outputText("Zero padding will be used.")
                ui.update_outputText("___")

                for i in range(0, data_in.shape[0]):
                    ui.update_outputTextSameLine(str(round(i*100./N,1))+"% concluded ("+str(i)+"/"+str(N-1)+").")
                    for j in range(0, data_in.shape[1]):

                        if count_nonzero(data_in[i][j].real)!=0:
                            N = data_in.shape[0]

                            Np = int(zeropad[1])

                            M1 = int(Np/2-N/2)
                            M2 = int(Np/2+N/2)

                            new_data = zeros((Np,Np), dtype=complex64)

                            new_data[M1:M2,M1:M2] = data_in[i][j]

                            new_fft = fft.fftshift(fft.fft2(fft.fftshift(new_data)))


                            data_in[i][j] = new_fft[M1:M2,M1:M2]

                return data_in

            else:
                ui.update_outputText("___")
                for i in range(0, data_in.shape[0]):
                    ui.update_outputTextSameLine(str(round(i*100./N,1))+"% concluded ("+str(i)+"/"+str(N-1)+").")
                    for j in range(0, data_in.shape[1]):

                        if count_nonzero(data_in[i][j].real)!=0:
                            data_in[i][j] = fft.fftshift(fft.fft2(fft.ifftshift(data_in[i][j])))

                return data_in
    #-----------------------------------------------------------
    #///////////////////////////////////////////////////////////
    #-----------------------------------------------------------

#------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------