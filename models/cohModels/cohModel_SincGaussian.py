#-------------------------------------------------------------------------------
# Name:        Sinc Gaussian Schell-model
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
from numpy import int32, double, float32, float, zeros, sinc, exp, copy, count_nonzero, pi

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Pre-requisites
#===============================================================================

cohModel_name = "Sinc Gaussian Schell-model"

cohModel_parameters = ["Standard Deviation (a.u.):","K1"]

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Coherece Model Function
#===============================================================================
def cohModelFunc(user_interface,context,queue,W_main,N,parameters,parallel,debug):

    user_interface.update_outputText("Starting Sinc Gaussian-Schell model function...")

    sigma_S = 2*float(parameters[0])**2

    K1 = parameters[1]


    try:

        # parameters
        M = N/2

        CL_pcohGS = None

        if parallel:
            #*******************************************************************
            # PyOpenCL kernel function
            #*******************************************************************

            # KERNEL: CODE EXECUTED ON THE GPU
            CL_pcohGS=Program(context,"""
                __kernel void increase(__global float *res,
                                       __global float *data,
                                       const unsigned int N,
                                       const unsigned int M,
                                       const unsigned int i1,
                                       const unsigned int j1,
                                       const double x1,
                                       const double y1,
                                       const double r1,
                                       const double sigma,
                                       const double K1)
                {
                    int row =  get_global_id(0);
                    int col = get_global_id(1);

                    int x2 = col-M;
                    int y2 = M-row;

                    double y22=(double) y2;
                    double x22=(double) x2;

                    double x3=x22-x1;
                    double y3=y22-y1;
                    double r1x=x3*x3;
                    double r1y=y3*y3;
                    double rl=r1x+r1y;

                    double r2  = (double) x2*x2+y2*y2;

                    double data_const=(double) data[col + N*row ];

                    double exp2 = exp(-r1/sigma)*exp(-r2/sigma);

                    double final;
                    double zero = (double) 0.0;

                    if (rl == zero){
                        double final=data_const*1.0;
                        res[col + N*row ]=(float) data_const*exp2;
                    }
                    else{
                        double SINE  = sin(K1*rl)/(K1*rl);
                        double final = data_const*exp2*SINE;
                        res[col + N*row ]=(float) final;
                    }



                }
            """).build()
            #___________________________________________________________________

            user_interface.update_outputText("PyOpenCl will be used. Starting Cycle...")
            user_interface.update_outputText("__")

            for i1 in range(0,N):

                user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")

                for j1 in range(0,N):

                    if not count_nonzero(W_main.real[i1,j1])==0.0:

                        # Defining
                        result=zeros((N,N)).astype(float32)
                        data= W_main.real[i1,j1].copy()

                        # Radius of point P1
                        x1=j1-M
                        y1=M-i1

                        r1 = x1**2+y1**2

                        # creating memory on gpu
                        mf = mem_flags

                        # Result memory
                        result_gpu_memory = Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=result)

                        # Data Memory
                        data_gpu_memory = Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data)

                        # Running the program (kernel)
                        CL_pcohGS.increase(queue,result.shape,None,result_gpu_memory,data_gpu_memory,
                                           int32(N),int32(M),int32(i1),int32(j1),double(x1),double(y1),
                                            double(r1),double(sigma_S),double(K1))

                        #  Copying results to PCmemory
                        enqueue_copy(queue,result,result_gpu_memory)

                        # Copying results to matrices
                        W_main.real[i1,j1]=result

            user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")

        # Without PyOpenCL
        else:
            user_interface.update_outputText("PyOpenCl will NOT be used. Starting Cycle...")
            for i1 in range(0,N):

                user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")

                for j1 in range(0,N):

                    x1=(j1-M)
                    y1=M-i1

                    for i2 in range(0,N):
                        for j2 in range(0,N):

                            x2=j2-M
                            y2=M-i2

                            x3  = x2-x1
                            y3  = y2-y1
                            r1x = x3**2
                            r1y = y3**2
                            rl  = r1x+r1y

                            r1 = x1**2+y1**2
                            r2 = x2**2+y2**2



                            W_main.real[i1,j1,i2,j2]=W_main.real[i1,j1,i2,j2]*sinc(K1*rl/pi)**exp(-r1/sigma_S)*exp(-r2/sigma_S)

            user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")

        return W_main

    except Exception as error:
        user_interface.update_outputTextSameLine(str(error))
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================

