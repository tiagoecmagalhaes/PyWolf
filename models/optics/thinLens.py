#-------------------------------------------------------------------------------
# Name:        Thin Lens
# Purpose:     PyWolf's Optics Models
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
from numpy import zeros, float32, int32, double, exp, copy

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Pre-requisites
#===============================================================================

optics_messages = ""

optics_name = "Thin Lens"

optics_parameters = ["focal length (m)"]

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Optics Model Function
#===============================================================================
def optics_function(user_interface,context,queue,W_main,N,dlp,w0,parameters,parallel,debug):


    user_interface.update_outputText("Starting thin lens function...")

    C1 = w0/(2*parameters[0]*3e8)

    if C1 !=0.0:

        M = int(N/2)

        if debug:
            user_interface.update_outputText("C1: "+str(C1))
            user_interface.update_outputText("dlp: "+str(dlp))

        CL_qfunc=None

        if parallel:

            user_interface.update_outputText("PyOpenCl will be used. Starting Cycle...")
            user_interface.update_outputText("__")

            # KERNEL: CODE EXECUTED ON THE GPU
            CL_qfunc=Program(context,"""
                __kernel void increase(__global float *res_real,
                                       __global float *res_imag,
                                       __global float *data_real,
                                       __global float *data_imag,
                                       const unsigned int N,
                                       const unsigned int M,
                                       const unsigned int i1,
                                       const unsigned int j1,
                                       const double dlp,
                                       const double C1,
                                       const double theta1)
                {
                    int row= get_global_id(0);
                    int col = get_global_id(1);

                    //=========================================================
                    // Point R2
                    //=========================================================
                    int y2=-(M-row);
                    int x2= col-M;

                    double x22 = (double) x2;
                    double y22 = (double) y2;

                    double r2_x = x22*dlp;
                    double r2_y = y22*dlp;

                    double r2_mag = r2_x*r2_x + r2_y*r2_y;

                    double theta2 = -C1*r2_mag;

                    double total_theta = theta1 + theta2;

                    //___Converting to real and imaginary__//

                    double a = (double) data_real[row*N + col ];
                    double b = (double) data_imag[row*N + col ];

                    double sin_x = sin(total_theta);
                    double cos_x = cos(total_theta);

                    double real = a*cos_x - b*sin_x;
                    double imag = a*sin_x + b*cos_x;

                    res_real[row*N + col] = (float) real;
                    res_imag[row*N + col]  = (float) imag;

                }
            """).build()


            for i1 in range(0,N):
                user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")

                for j1 in range(0,N):

                    # Q functions for object plane
                    x1=j1-M
                    y1=M-i1

                    r1_x=x1*dlp
                    r1_y=y1*dlp
                    r1_mag=(r1_x**2)+(r1_y**2)

                    theta1 = C1*(r1_mag)

                    # Data
                    data_real = W_main[i1,j1].real.copy()
                    data_imag = W_main[i1,j1].imag.copy()

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
                    CL_qfunc.increase(queue,data_real.shape,None,result_real_gpu_memory,result_imag_gpu_memory,
                                       data_real_gpu_memory,data_imag_gpu_memory,
                                       int32(N),int32(M),int32(i1),int32(j1),double(dlp),
                                       double(C1),double(theta1))

                    # Copying Result to PC memory
                    enqueue_copy(queue,result_real,result_real_gpu_memory)
                    enqueue_copy(queue,result_imag,result_imag_gpu_memory)

                    # Copying to Main Matrix
                    W_main.real[i1,j1] = result_real.copy()
                    W_main.imag[i1,j1] = result_imag.copy()


        else:
            user_interface.update_outputText("PyOpenCl will NOT be used. Starting Cycle...")
            user_interface.update_outputText("__")


            for i1 in range(0,N):
                # updateing text
                user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")

                for j1 in range(0,N):

                    # Q functions for object plane
                    x1=j1-M
                    y1=M-i1

                    r1x = x1*dlp
                    r1y = y1*dlp

                    r1_mag = r1x**2 + r1y**2

                    theta1 = C1*(r1_mag)

                    for i2 in range(0,N):
                        for j2 in range(0,N):

                            ## Point R2 ##
                            x2 = j2-M
                            y2 = M-i2

                            r2x = x2*dlp
                            r2y = y2*dlp

                            r2_mag = r2x**2 + r2y**2

                            theta2 = -C1*r2_mag

                            WP = theta1 + theta2

                            W_main[i1,j1,i2,j2]*=exp(1j*WP)

        user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")
        return W_main

    else:
        user_interface.update_outputText("No need for q function multiplication: no phase values to add.")
        return W_main

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================