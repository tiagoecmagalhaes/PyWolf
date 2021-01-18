#-------------------------------------------------------------------------------
# Name:        Quasi-homogeneous Lasjunen-Saastamoinen
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
cohModel_name = "Quasi-homogeneous Lasjunen-Saastamoinen"

cohModel_parameters = ["x0","y0","wc"]
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Coherece Model Function
#===============================================================================
def cohModelFunc(user_interface,context,queue,W_main,N,parameters,parallel,debug):

    user_interface.update_outputText("Starting Quasi-homogeneous Lasjunen-Saastamoinen model function...")


    X0=[parameters[0],parameters[1]]
    X0_x=parameters[0]
    X0_y=parameters[1]
    sigma=parameters[2]

    sigma=sigma**4

    try:

        # parameters
        M = N/2

        CL_pcohGS = None

        if parallel:
            #*******************************************************************
            # PyOpenCL kernel function
            #*******************************************************************
            # KERNEL: CODE EXECUTED ON THE GPU
            CL_pcohNUG=Program(context,"""
                __kernel void increase(__global float *res,
                                       __global float *data,
                                       const unsigned int N,
                                       const unsigned int M,
                                       const unsigned int i1,
                                       const unsigned int j1,
                                       const double x1,
                                       const double y1,
                                       const double x1_n,
                                       const double y1_n,
                                       const double X0_x,
                                       const double X0_y,
                                       const double sigma,
                                       const double R1)
                {
                    int row =  get_global_id(0);
                    int col = get_global_id(1);

                    int x22=col-M;
                    int y22=M-row;

                    double y2=(double) y22;
                    double x2=(double) x22;

                    double x2_n=x2-X0_x;
                    double y2_n=y2-X0_y;

                    double R2=(x2_n*x2_n)+(y2_n*y2_n);

                    double rl=R2-R1;

                    double arg_miu= exp(-(rl*rl)/sigma);


                    double data_const=(double) data[col + N*row ];


                    double final=data_const*arg_miu;


                    res[col + N*row ]=(float) final;

                }
            """).build()
            #___________________________________________________________________

            user_interface.update_outputText("PyOpenCl will be used. Starting Cycle...")
            user_interface.update_outputText("__")

            for i1 in range(0,N):

                user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")

                for j1 in range(0,N):
                    # Radius of point P1
                    x1= j1-M
                    y1= M-i1

                    x1_n= x1-X0_x
                    y1_n= y1-X0_y

                    R1 = (x1_n**2)+(y1_n**2)

                    # Defining
                    result=zeros((N,N)).astype(float32)
                    data=copy.copy(W_main.real[i1,j1])

                    # creating memory on gpu
                    mf = mem_flags

                    # Result memory
                    result_gpu_memory = Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=result)

                    # Data Memory
                    data_gpu_memory = Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data)

                    # Running the program (kernel)
                    CL_pcohNUG.increase(queue,result.shape,None,result_gpu_memory,data_gpu_memory,
                                       int32(N),int32(M),int32(i1),int32(j1),double(x1),double(y1),
                                       double(x1_n),double(y1_n),double(X0_x),double(X0_y),double(sigma),
                                       double(R1))

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
                    y1=(M-i1)
                    x1_n=x1-X0_x
                    y1_n=y1-X0_y

                    R1=(x1_n**2)+(y1_n**2)


                    for i2 in range(0,N):
                        for j2 in range(0,N):

                            x2=j2-M
                            y2=(M-i2)

                            x2_n=x2-X0_x
                            y2_n=y2-X0_y

                            R2=x2_n**2+y2_n**2

                            rl=(R2-R1)**2

                            miu=exp(-rl/sigma)

                            W_main.real[i1,j1,i2,j2]=W_main.real[i1,j1,i2,j2]*miu

            user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")

        return W_main

    except Exception as error:
        user_interface.update_outputTextSameLine(str(error))
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


