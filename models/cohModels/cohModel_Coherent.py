#-------------------------------------------------------------------------------
# Name:        Perfectly coherent
# Purpose:     PyWolf's Coherence Model
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

# NumPy
from numpy import int32, double, float32, zeros, count_nonzero, copy, sqrt


#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Pre-requisites
#===============================================================================

cohModel_name = "Coherent"

cohModel_parameters = []

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Coherece Model Function
#===============================================================================
def cohModelFunc(user_interface,context,queue,W_main,N,parameters,parallel,debug):

    user_interface.update_outputText("Starting Coherent model function...")


    # parameters
    M = N/2

    CL_coh = None

    if parallel:
        #***********************************************************************
        # PyOpenCL kernel function
        #***********************************************************************
        CL_coh=None

        # KERNEL: CODE EXECUTED ON THE GPU
        CL_coh=Program(context,"""
            //PYOPENCL_COMPILER_OUTPUT=1

            __kernel void increase(__global float *res,
                                   __global float *data,
                                   __global float *dataW,
                                   const unsigned int N,
                                   const unsigned int i1,
                                   const unsigned int j1)
            {
                int row = get_global_id(0);
                int col = get_global_id(1);

                float S2 = sqrt(data[col + N*row]); // comes from image
                float S1 = sqrt(dataW[j1 + N*i1]) ; // comes from W

                res[col + N*row ]= (float) S1*S2;


            }
        """).build()
        #_______________________________________________________________________


        user_interface.update_outputText("PyOpenCl will be used. Starting Cycle...")
        user_interface.update_outputText("__")


        # creating S1 S2
        S = zeros((N,N)).astype(float32)
        for i in range(0,N):
            for j in range(0,N):
                S[i,j] = W_main[i,j,i,j].real.copy()

        for i1 in range(0,N):
            user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
            for j1 in range(0,N):

                    # Defining
                    result  = zeros((N,N)).astype(float32)
                    dataW   = W_main[i1,j1].real.copy()
                    data    = S

                    # creating memory on gpu
                    mf = mem_flags

                    # Result memory
                    result_gpu_memory = Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=result)

                    # Data Memory
                    data_gpu_memory  = Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data)
                    dataW_gpu_memory = Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=dataW)

                    # Running the program (kernel)
                    CL_coh.increase(queue,result.shape,None,result_gpu_memory,data_gpu_memory,dataW_gpu_memory,int32(N),int32(i1),int32(j1))

                    #  Copying results to PCmemory
                    enqueue_copy(queue,result,result_gpu_memory)

                    # Copying results to matrices
                    W_main.real[i1,j1] = result

        user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")

    else:
            user_interface.update_outputText("PyOpenCl will NOT be used. Starting Cycle...")
            for i1 in range(0,N):
                user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
                for j1 in range(0,N):

                    if not count_nonzero(W_main[i1,j1])==0:

                        for i2 in range(0,N):
                                for j2 in range(0,N):
                                    W_main[i1,j1,i2,j2]=sqrt(W_main[i1,j1,i1,j1])*sqrt(W_main[i2,j2,i2,j2])


    return W_main

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


