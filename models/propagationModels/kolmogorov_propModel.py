#-------------------------------------------------------------------------------
# Name:        Turbulent medium - Propagation
# Purpose:     PyWolf functions
#
# Author:      TEC MAGALHAES
#
# Licence:     GNU GENERAL PUBLIC LICENSE Version 3
#-------------------------------------------------------------------------------


#===============================================================================
# Importing Packages
#===============================================================================
# PyOpenCL
from pyopencl import *

# NumPy
from numpy import zeros, exp, float32, int32, double, pi, sqrt, inf, longdouble

# Import Time
import time

#===============================================================================
#//////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Pre-requisites - Inputs
#===============================================================================
propModel_name = "Turbulent medium: Kolmogorov"

propModel_parameters = ["refractive index:", "Cn2 (constant):"]
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Propagation plane spatial resolution
#===============================================================================
def spatial_resolution(N, gen_pars, prop_pars):

    # general parameters
    R         = float(gen_pars[0]) # distance, 40e-6
    omega0    = float(gen_pars[1]) # angular frequency, 2271030833920332.5
    c         = float(gen_pars[2]) # speed of light
    sourceRes = float(gen_pars[3])

    # propagation parameters
    n0   = float(prop_pars[0])   # refractive index, 1.53

    # calculation
    dx = 2*pi*c*R/(n0*omega0*N*sourceRes)
    dx = 2*pi*c*R/(n0*omega0*N*sourceRes)

    return dx

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Propagation Model - Q function - source
#===============================================================================
def func_qfunctionA(user_interface, context, queue, W_main, N, dlp, gen_pars, prop_pars, parallel, debug):



    # printing
    user_interface.update_outputText("Using turbulent medium Kolmogorov model...")
    user_interface.update_outputText("Only spectral density results are valid!")

    # general parameters
    R      = float(gen_pars[0]) # distance, 40e-6
    omega0 = float(gen_pars[1]) # angular frequency, 2271030833920332.5
    c      = float(gen_pars[2]) # speed of light

    # propagation parameters
    n0   = float(prop_pars[0])   # refractive index, 1.53
    Cn2  = float(prop_pars[1])   # constant, 9.854e-4

    # calculated paramters
    k = n0*omega0/c


    wavelength = 2*pi*c/omega0

    Mt = 0.49 * (Cn2)**(6/5) * k**(12/5) * R**(6/5)
    print(Mt)


    C1 = n0*omega0/(2*R*3e8)


    if True:
        print("R: "+str(R))
        print("omega0: "+str(omega0))
        print("wavelength_0: "+str(2*pi*3e8/omega0))
        print("k: "+str(k))
        print("n0: "+str(n0))
        print("Cn2: "+str(Cn2))
        print("Mt: "+str(Mt))

    if C1 !=0.0:

        M = int(N/2)

        if debug:
            user_interface.update_outputText("C1: "+str(C1))
            user_interface.update_outputText("Spatial Resolution (m): "+str(dlp))

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
                                       const double r1_x,
                                       const double r1_y,
                                       const double C1,
                                       const double Mt,
                                       const double theta1)
                {
                    int row= get_global_id(0);
                    int col = get_global_id(1);

                    //=========================================================
                    // Point R2
                    //=========================================================

                    int x2= col-M;
                    int y2= M-row;

                    double x22 = (double) x2;
                    double y22 = (double) y2;

                    // points
                    double r2_x = x22*dlp;
                    double r2_y = y22*dlp;

                    double r2_mag = r2_x*r2_x + r2_y*r2_y;

                    double theta2 = C1*r2_mag;
                    //_________________________________________________________

                    double total_theta = theta1 + theta2;

                    double a = (double) data_real[row*N + col ];
                    double b = (double) data_imag[row*N + col ];


                    // turbulence parameter
                    double arg1 = (r1_x-r2_x)*(r1_x-r2_x)*Mt;
                    double arg2 = (r1_y-r2_y)*(r1_y-r2_y)*Mt;
                    double argT = arg1 + arg2;
                    double exp3 = exp(-argT);

                    double a2 = a*exp3; //* exp( 2*(r1_x*r2_x + r1_y*r2_y)*MR) ;
                    double b2 = b*exp3; //* exp( 2*(r1_x*r2_x + r1_y*r2_y)*MR ) ;

                    double sin_x = sin(total_theta);
                    double cos_x = cos(total_theta);

                    double real = a2*cos_x - b2*sin_x;
                    double imag = a2*sin_x + b2*cos_x;

                    res_real[row*N + col]  = (float) real;
                    res_imag[row*N + col]  = (float) imag;

                }
            """).build()


            for i1 in range(0,N):
                user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")

                for j1 in range(0,N):

                    # Q functions for object plane
                    y1=M-i1
                    x1=j1-M


                    r1_x=x1*dlp
                    r1_y=y1*dlp
                    r1_mag=(r1_x**2)+(r1_y**2)

                    theta1 = -C1*(r1_mag)


                    import copy

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
                    CL_qfunc.increase(queue,data_real.shape,None,result_real_gpu_memory,result_imag_gpu_memory,
                                       data_real_gpu_memory,data_imag_gpu_memory,
                                       int32(N),int32(M),int32(i1),int32(j1),double(dlp),double(r1_x),double(r1_y),
                                       double(C1),double(Mt),double(theta1))

                    # Copying Result to PC memory
                    enqueue_copy(queue,result_real,result_real_gpu_memory)
                    enqueue_copy(queue,result_imag,result_imag_gpu_memory)

                    # Copying to Main Matrix
                    W_main.real[i1,j1] = copy.copy(result_real)
                    W_main.imag[i1,j1] = copy.copy(result_imag)


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

                    r1_mag = r1x**2 + r1y**2 ## |r1_mag|^2


                    # free space + turbulence - r1
                    exp_1 = exp(-(1j*C1 ) *r1_mag )

                    for i2 in range(0,N):
                        for j2 in range(0,N):

                            ## Point R2 ##
                            x2 = j2-M
                            y2 = M-i2

                            r2x = x2*dlp
                            r2y = y2*dlp

                            r2_mag = r2x**2 + r2y**2


                            exp_2 = exp( (1j*C1 ) *r2_mag )


                            arg1 = (r1x-r2x)*(r1x-r2x)
                            arg2 = (r1y-r2y)*(r1y-r2y)
                            argT = (arg1+arg2)*Mt
                            exp3 = exp(-argT)

                            """
                            arg1 = (r1x-r2x)*(r1x-r2x)/abs_rho02
                            arg2 = (r1y-r2y)*(r1y-r2y)/abs_rho02
                            argT = arg1+arg2
                            exp3 = exp(-argT)
                            """
                            """
                            arg1   = 2*(r1x*r2x)/abs_rho02
                            exp_31 = exp(arg1)

                            if exp_31 == inf:
                                print(arg1, r1x, r2x)

                            arg2   = 2*(r1y*r2y)/abs_rho02
                            exp_32 = exp(arg2)
                            """
                            W_main[i1,j1,i2,j2]*=exp_1*exp_2*exp3#*exp_31*exp_32

        user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")
        return W_main

    else:
        user_interface.update_outputText("No need for q function multiplication: no phase values to add.")
        return W_main

#_______________________________________________________________________________


#===============================================================================
# Propagation Model - Q function - source
#===============================================================================

def func_qfunctionB(user_interface, context, queue, W_main, N, dlp, gen_pars, prop_pars, parallel, debug):
    ##res = func_qfunctionB(user_interface, context, queue, W_main, N, dlp, gen_pars, prop_pars, parallel, debug)
    return W_main

#_______________________________________________________________________________