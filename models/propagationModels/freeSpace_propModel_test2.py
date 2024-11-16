#-------------------------------------------------------------------------------
# Name:        Free Space Propagation
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
from numpy import zeros, exp, float32, int32, double, pi, linspace
from numpy import *
from scipy.integrate import trapz

# Import Time
import time



#===============================================================================
#//////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Pre-requisites
#===============================================================================
propModel_name = "Test2"

propModel_parameters = []
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

    dx = 2*pi*c*R/(omega0*N*sourceRes)

    return dx


def trapezoidal_integration(func_values, step_size):
    """
    Perform trapezoidal integration on a list of function values.

    Parameters:
        func_values (list): A list of function values.
        step_size (float): The spacing between consecutive function values.

    Returns:
        float: The approximate integral using the trapezoidal rule.
    """
    n = len(func_values)
    integral = 0

    # Calculate the sum of the trapezoidal areas
    for i in range(1, n):
        integral += (func_values[i - 1] + func_values[i]) / 2

    # Multiply by the step size to get the final integral
    integral *= step_size

    return integral



def double_trapezoidal_integration(matrix, x_values, y_values):
    """
    Perform double trapezoidal integration on a 2D matrix representing f(x, y).

    Parameters:
        matrix (list of lists): A 2D matrix representing the function f(x, y).
        x_values (list): The array of x values corresponding to the matrix columns.
        y_values (list): The array of y values corresponding to the matrix rows.

    Returns:
        float: The approximate double integral using the trapezoidal rule.
    """
    num_x = x_values.shape[0]
    num_y = y_values.shape[0]

    # Step 1: Integrate along the x-axis for each y-value to get 1D array
    integrated_along_x = zeros((num_x), dtype="complex")
    for i in range(num_x):
        actual_real = trapezoidal_integration(matrix[i].real, abs(x_values[1] - x_values[0]) )
        actual_imag = trapezoidal_integration(matrix[i].imag, abs(x_values[1] - x_values[0]) )

        integrated_along_x[i] = actual_real + 1j*actual_imag


    # Step 2: Integrate along the y-ax.is using the result from Step 1
    result = trapezoidal_integration(integrated_along_x.real, abs(y_values[1] - y_values[0]) )+\
             1j*trapezoidal_integration(integrated_along_x.imag, abs(y_values[1] - y_values[0]) )

    return result



def integrar_matriz_2d_trapezio(matriz, dx, dy):
    # Integra ao longo do eixo w (último eixo)
    integral_x = trapz(matriz, dx=dx, axis=-1)
    # Integra ao longo do eixo z
    integral_y = trapz(integral_x, dx=dy, axis=-1)

    return integral_y

def integrar_matriz_4d_trapezio(matriz, dx, dy):
    # Integra ao longo do eixo w (último eixo)
    integral_x = trapz(matriz, dx=dx, axis=-1)
    # Integra ao longo do eixo z
    integral_y = trapz(integral_x, dx=dy, axis=-1)

    return integral_y

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Propagation Model - Q function - source
#===============================================================================
def func_qfunctionA(user_interface, context, queue, W_main, N, dlp, gen_pars, prop_pars, parallel, debug):

    import copy

    # temp
    WW = zeros((W_main.shape[0],W_main.shape[1],W_main.shape[2],W_main.shape[3]), dtype="complex64")


    # printing
    user_interface.update_outputText("Using free-space propagation model...")

    # general parameters
    R      = gen_pars[0] # distance
    omega0 = gen_pars[1] # angular frequency
    c      = gen_pars[2] # speed of light

    dlp = 9.9e7
    dx = 9.9e-5


    C1 = omega0/(2*R*3e8)

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
                                       const double dlp,
                                       const double dx,
                                       const double r1xx,
                                       const double r1yy,
                                       const double r2xx,
                                       const double r2yy,
                                       const double r1y,
                                       const double C1)
                {
                    int row = get_global_id(0);
                    int col = get_global_id(1);
                    int col2 = get_global_id(2);


                    //=========================================================
                    // Point R1
                    //=========================================================

                    int x1= col2-M;

                    double x11 = (double) x1;

                    double r1x = x11*dlp;

                    double r1_mag = r1x*r1x + r1y*r1y;

                    double theta1 = -C1*r1_mag;
                    //_________________________________________________________



                    //=========================================================
                    // Point R2
                    //=========================================================

                    int x2= col-M;
                    int y2= M-row;

                    double x22 = (double) x2;
                    double y22 = (double) y2;

                    double r2_x = x22*dlp;
                    double r2_y = y22*dlp;

                    double r2_mag = r2_x*r2_x + r2_y*r2_y;

                    double theta2 = C1*r2_mag;
                    //_________________________________________________________

                    double total_theta = theta1 + theta2 -2*C1*r1xx*r1x - 2*C1*r1yy*r1y + 2*C1*r2xx*r2_x + 2*C1*r2yy*r2_y;

                    double a = (double) data_real[N*N*col2 + row*N + col];
                    double b = (double) data_imag[N*N*col2 + row*N + col];

                    double sin_x = sin(total_theta);
                    double cos_x = cos(total_theta);

                    double real = a*cos_x - b*sin_x;
                    double imag = a*sin_x + b*cos_x;

                    res_real[N*N*col2 + row*N + col] = (float) real;
                    res_imag[N*N*col2 + row*N + col]  = (float) imag;

                }
            """).build()

            for ii1 in range(0,N):
                user_interface.update_outputTextSameLine(str(round(ii1*100./N,1))+"% concluded ("+str(ii1)+"/"+str(N-1)+").")

                for jj1 in range(0,N):


                    xx1=jj1-M
                    yy1=M-ii1

                    r1xx = xx1*dx
                    r1yy = yy1*dx

                    for ii2 in range(0,N):
                        for jj2 in range(0,N):


                            xx2=jj2-M
                            yy2=M-ii2

                            r2xx = xx2*dx
                            r2yy = yy2*dx


                            # SUM
                            integral = 0 + 0*1j


                            for i1 in range(0, N):

                                y1=M-i1
                                r1y = y1*dlp


                                # Data
                                data_real=copy.copy(W_main[i1].real)
                                data_imag=copy.copy(W_main[i1].imag)

                                # creating memory on gpu
                                mf = mem_flags

                                data_real_gpu_memory = Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data_real)
                                data_imag_gpu_memory = Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data_imag)

                                # Result memory -> amplitude and phase conjugation
                                result_real=zeros((N,N,N)).astype(float32)
                                result_real_gpu_memory = Buffer(context, mf.WRITE_ONLY, size=result_real.nbytes)
                                result_imag=zeros((N,N,N)).astype(float32)
                                result_imag_gpu_memory = Buffer(context, mf.WRITE_ONLY, size=result_imag.nbytes)

                                # Running the program (kernel)
                                CL_qfunc.increase(queue,data_real.shape,None,result_real_gpu_memory,result_imag_gpu_memory,
                                                   data_real_gpu_memory,data_imag_gpu_memory,
                                                   int32(N),int32(M),int32(i1),double(dlp),double(dx),
                                                   double(r1xx),double(r1yy),double(r2xx),double(r2yy),double(r1y),
                                                   double(C1))

                                # Copying Result to PC memory
                                enqueue_copy(queue,result_real,result_real_gpu_memory)
                                enqueue_copy(queue,result_imag,result_imag_gpu_memory)

                                # Copying to Main Matrix
                                WW.real[ii1,jj1,ii2,jj2] = sum(result_real)
                                WW.imag[ii1,jj1,ii2,jj2] = sum(result_imag)


        else:
            user_interface.update_outputText("PyOpenCl will NOT be used. Starting Cycle...")
            user_interface.update_outputText("__")



            x_array = linspace(-M,M-1,N)*dx
            y_array = x_array.copy()


            import copy


            print("000000")
            for ii1 in range(0,N):
                # updateing text
                user_interface.update_outputTextSameLine(str(round(ii1*100./N,1))+"% concluded ("+str(ii1)+"/"+str(N-1)+").")

                for jj1 in range(0,N):


                    xx1=jj1-M
                    yy1=M-ii1

                    r1xx = xx1*dx
                    r1yy = yy1*dx

                    for ii2 in range(0,N):
                        for jj2 in range(0,N):


                            xx2=jj2-M
                            yy2=M-ii2

                            r2xx = xx2*dx
                            r2yy = yy2*dx


                            # SUM
                            integral = 0 + 0*1j

                            for i1 in range(0,N):

                                for j1 in range(0,N):

                                    # Q functions for object plane
                                    x1=j1-M
                                    y1=M-i1

                                    r1x = x1*dlp
                                    r1y = y1*dlp

                                    r1_mag = r1x**2 + r1y**2

                                    theta1 = -C1*(r1_mag)

                                    for i2 in range(0,N):
                                        for j2 in range(0,N):

                                            ## Point R2 ##
                                            x2 = j2-M
                                            y2 = M-i2

                                            r2x = x2*dlp
                                            r2y = y2*dlp

                                            r2_mag = r2x**2 + r2y**2

                                            ##actual = W_main[i1,j1,i2,j2]*exp(1j*(theta1 + (C1*r2_mag)))* exp(-2j*C1*r1xx*r1x - 2j*C1*r1y*r1yy) *exp(2j*C1*r2x*r2xx + 2j*C1*r2y*r2yy)  #*cos(2*C1*x_array[jj1]*r1x+2*C1*y_array[ii1]*r1y)

                                            integral += W_main[i1,j1,i2,j2]*exp(1j*(theta1 + (C1*r2_mag)))* exp(-2j*C1*r1xx*r1x - 2j*C1*r1y*r1yy) *exp(2j*C1*r2x*r2xx + 2j*C1*r2y*r2yy)


                            WW[ii1,jj1,ii2,jj2] = integral




        user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")
        return WW

    else:
        user_interface.update_outputText("No need for q function multiplication: no phase values to add.")
        return W_main
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================



#===============================================================================
# Propagation Model - Q function - propagation plane
#===============================================================================


def func_qfunctionB(user_interface, context, queue, W_main, N, dlp, gen_pars, prop_pars, parallel, debug):
    res = func_qfunctionA(user_interface, context, queue, W_main, N, dlp, gen_pars, prop_pars, parallel, debug)
    return res

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================
