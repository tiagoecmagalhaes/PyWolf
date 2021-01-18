#-------------------------------------------------------------------------------
# Name:        Incoherent
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
from numpy import int32, double, float32, float, zeros
from numpy import count_nonzero

# import copy
import copy

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Pre-requisites
#===============================================================================

cohModel_name = "Incoherent"

cohModel_parameters = []

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Coherece Model Function
#===============================================================================
def cohModelFunc(user_interface,context,queue,W_main,N,parameters,parallel,debug):

    user_interface.update_outputText("Starting Incoherent model function...")

    try:

        # parameters
        M = N/2

        CL_incoh = None

        if parallel:
            #***********************************************************************
            # PyOpenCL kernel function
            #***********************************************************************
            CL_incoh=None
            if parallel:
                # KERNEL: CODE EXECUTED ON THE GPU
                CL_incoh=Program(context,"""
                    //PYOPENCL_COMPILER_OUTPUT=1

                    __kernel void increase(__global float *res,
                                           __global float2 *data,
                                           const unsigned int N,
                                           const unsigned int M,
                                           const unsigned int i1,
                                           const unsigned int j1)
                    {
                        int row =  get_global_id(0);
                        int col = get_global_id(1);

                        int x=col-M;
                        int y=M-row;

                        if (row==i1 && col==j1){
                            res[col + N*row ]=data[col + N*row ].x;
                        }
                        else {
                            res[col + N*row ]=data[col + N*row ].x*0.0;
                        }
                    }
                """).build()
            #__________________________________________________________________________

            user_interface.update_outputText("PyOpenCl will be used. Starting Cycle...")
            user_interface.update_outputText("__")
            for i1 in range(0,N):
                user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
                for j1 in range(0,N):
                    if not count_nonzero(W_main[i1,j1])==0:

                        # Defining
                        result=zeros((N,N)).astype(float32)
                        data=W_main[i1,j1]

                        # creating memory on gpu
                        mf = mem_flags

                        # Result memory
                        result_gpu_memory = Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=result)

                        # Data Memory
                        data_gpu_memory = Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data)

                        # Running the program (kernel)
                        CL_incoh.increase(queue,result.shape,None,result_gpu_memory,data_gpu_memory,int32(N),
                                          int32(M),int32(i1),int32(j1))

                        #  Copying results to PCmemory
                        enqueue_copy(queue,result,result_gpu_memory)

                        # Copying results to matrices
                        W_main.real[i1][j1]=result

            user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")
        else:
            user_interface.update_outputText("PyOpenCl will NOT be used. Starting Cycle...")
            for i1 in range(0,N):
                user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
                for j1 in range(0,N):

                    #if not count_nonzero(W_main[i1,j1])==0:

                        for i2 in range(0,N):
                                for j2 in range(0,N):
                                    if i1==i2 and j1==j2:
                                        pass
                                    else:
                                        W_main[i1,j1,i2,j2]=0.0+0j

            user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")

    except Exception as error:
        user_interface.update_outputTextSameLine(str(error))


    return W_main
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


