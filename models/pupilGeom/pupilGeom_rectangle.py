#-------------------------------------------------------------------------------
# Name:        Rectangular Pupil
# Purpose:     PyWolf's Pupil Geometry Model
#
# Author:      Tiago E. C. Magalhaes
#
# Licence:     GNU GENERAL PUBLIC LICENSE Version 3
#-------------------------------------------------------------------------------


#===============================================================================
# Importing Packages
#===============================================================================
# PyOpenCL
from pyopencl import *

# Numpy
from numpy import zeros, float32, int32

# Copy
import copy
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Pre-requisites
#===============================================================================
pupilGeom_name = "Rectangular Pupil"

pupilGeom_parameters = ["width (a.u.)", "height (a.u.)"]
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Pupil Geometry Model Function
#===============================================================================
def geomFunc(user_interface,context,queue,W_main,N,parameters,parallel,debug):

    user_interface.update_outputText("Starting pupil geometric function...")

    # radius
    width  = parameters[0]
    height = parameters[1]

    if debug:
        user_interface.update_outputText("width: "+str(width)+"\nheight: "+str(height))

    # parameters
    M = N/2

    CL_geom = None

    if parallel:
        CL_geom=Program(context,"""
            __kernel void increase(__global float *res_real,
                                   __global float *res_imag,
                                   __global float *data_real,
                                   __global float *data_imag,
                                   const unsigned int N,
                                   const unsigned int M,
                                   const unsigned int i1,
                                   const unsigned int j1,
                                   const int a,
                                   const int b)
            {
                int row =  get_global_id(0);
                int col = get_global_id(1);

                int x=col-M;
                int y=(M-row);

                if (x<=a && y<=b && -x<=a && -y<=b){
                    res_real[col + N*row ]= data_real[col + N*row ];
                    res_imag[col + N*row ]= data_imag[col + N*row ];
                }
                else {
                    res_real[col + N*row ]=0.0;
                    res_imag[col + N*row ]=0.0;
                }
            }
        """).build()

        user_interface.update_outputText("PyOpenCL will be used. Starting Cycle...")
        user_interface.update_outputText("__")
        for i1 in range(0,N):
            user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
            for j1 in range(0,N):

                # Radius of point P1
                x1=j1-M
                y1=M-i1

                if abs(x1)<=width and abs(y1)<=height:

                    # Data
                    data_real=copy.copy(W_main[i1,j1].real)
                    data_imag=copy.copy(W_main[i1,j1].imag)

                    # creating memory on gpu
                    mf = mem_flags

                    data_real_gpu_memory = Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data_real)
                    data_imag_gpu_memory = Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data_imag)

                    # Result memory -> amplitude and phase conjugation
                    result_real=zeros((N,N)).astype(float32)
                    result_real_gpu_memory = Buffer(context, mf.WRITE_ONLY, size=result_real.nbytes)
                    result_imag=zeros((N,N)).astype(float32)
                    result_imag_gpu_memory = Buffer(context, mf.WRITE_ONLY, size=result_imag.nbytes)

                    # Running the program (kernel)
                    CL_geom.increase(queue,data_real.shape,None,result_real_gpu_memory,result_imag_gpu_memory,
                                    data_real_gpu_memory,data_imag_gpu_memory,
                                     int32(N), int32(M), int32(i1), int32(j1), int32(width), int32(height))

                    # Copying Result to PC memory
                    enqueue_copy(queue,result_real,result_real_gpu_memory)
                    enqueue_copy(queue,result_imag,result_imag_gpu_memory)

                    # Copying to Main Matrix
                    W_main.real[i1,j1]=copy.copy(result_real)
                    W_main.imag[i1,j1]=copy.copy(result_imag)

                else:
                    W_main[i1,j1]=W_main[i1,j1]*0.0

        user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")

    else:
        user_interface.update_outputText("PyOpenCL will NOT be used. Starting Cycle...")
        user_interface.update_outputText("__")
        for i1 in range(0,N):
            user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
            for j1 in range(0,N):
                x1=j1-M
                y1=M-i1

                if abs(x1)<=width and abs(y1)<=height:

                    for i2 in range(0,N):
                        for j2 in range(0,N):
                            x2=j2-M
                            y2=M-i2
                            if abs(x2)<=width and abs(y2)<=height:
                                W_main.real[i1,j1,i2,j2]=W_main.real[i1,j1,i2,j2]
                                W_main.imag[i1,j1,i2,j2]=W_main.imag[i1,j1,i2,j2]
                            else:
                                W_main[i1,j1,i2,j2]=0.0+0j
                else:
                    W_main[i1,j1]=abs(W_main[i1,j1])*0.0

        user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")

    return W_main
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================