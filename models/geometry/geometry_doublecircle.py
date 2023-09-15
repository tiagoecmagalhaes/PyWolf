#-------------------------------------------------------------------------------
# Name:        Two Circles
# Purpose:     PyWolf's Source Geometry Model
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
from numpy import zeros, sqrt, float32, int32, double, copy

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Pre-requisites
#===============================================================================
geometry_name = "Two Circles"

geometry_parameters = ["Right Circle Radius (a.u.)","Left Circle Radius (a.u.)","x-offset (a.u.)","y-offset (a.u.)"]
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Source Geometry Model Function
#===============================================================================
def geomFunc(user_interface,context,queue,W_main,N,parameters,parallel,debug):

    user_interface.update_outputText("Starting geometric function (two circles)...")

    # radius
    radius_right = parameters[0]
    radius_left  = parameters[1]
    x_offset     = parameters[2]
    y_offset     = parameters[3]

    if debug:
        # text
        user_interface.update_outputText("(Radius Left: "+str(radius_left)+")")
        user_interface.update_outputText("(Radius Right: "+str(radius_right)+")")
        user_interface.update_outputText("(x-offset: "+str(x_offset)+")")
        user_interface.update_outputText("(y-offset: "+str(y_offset)+")")

    # parameters
    M = N/2

    CL_geom = None

    if parallel:
        CL_geom=Program(context,"""
            __kernel void increase(__global float *res,
                                   const unsigned int N,
                                   const unsigned int M,
                                   const unsigned int i1,
                                   const unsigned int j1,
                                   const double radius_left,
                                   const double radius_right,
                                   const double x0,
                                   const double y0)
            {
                int row =  get_global_id(0);
                int col = get_global_id(1);

                int x=col-M;
                int y=(M-row);

                double y2=(double) y;
                double x2=(double) x;

                double r2_right = sqrt((x2-x0)*(x2-x0)+(y2-y0)*(y2-y0));

                double r2_left = sqrt((x2+x0)*(x2+x0)+(y2+y0)*(y2+y0));

                if (radius_left>=r2_left || radius_right>=r2_right){
                    res[col + N*row ]= 1.0;
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

                r1_right  = sqrt((x1-x_offset)**2+(y1-y_offset)**2)
                r1_left   = sqrt((x1+x_offset)**2+(y1+y_offset)**2)

                if radius_right>=r1_right or radius_left>=r1_left:

                    # Data
                    data_real = W_main[i1,j1].real.copy()

                    # creating memory on gpu
                    mf = mem_flags

                    # Result memory -> amplitude and phase conjugation
                    result_real=zeros((N,N)).astype(float32)
                    result_real_gpu_memory = Buffer(context, mf.WRITE_ONLY, size=result_real.nbytes)

                    # Running the program (kernel)
                    CL_geom.increase(queue,data_real.shape,None,result_real_gpu_memory,
                                     int32(N),int32(M),int32(i1), int32(j1),double(radius_left),
                                     double(radius_right),double(x_offset),double(y_offset))

                    # Copying Result to PC memory
                    enqueue_copy(queue,result_real,result_real_gpu_memory)

                    # Copying to Main Matrix
                    W_main.real[i1,j1] = result_real.copy()



        user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")

    else:
        user_interface.update_outputText("PyOpenCL will NOT be used. Starting Cycle...")
        user_interface.update_outputText("__")
        for i1 in range(0,N):
            user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
            for j1 in range(0,N):
                x1=j1-M
                y1=M-i1

                r1_right  = sqrt((x1-x_offset)**2+(y1-y_offset)**2)
                r1_left   = sqrt((x1+x_offset)**2+(y1+y_offset)**2)

                if radius_right>=r1_right or radius_left>=r1_left:

                    for i2 in range(0,N):
                        for j2 in range(0,N):

                            x2=j2-M
                            y2=M-i2

                            r2=sqrt(y2**2+x2**2)

                            r2_right = sqrt((x2-x_offset)**2+(y2-y_offset)**2)
                            r2_left  = sqrt((x2+x_offset)**2+(y2+y_offset)**2)

                            if radius_right>=r2_right or radius_left>=r2_left:
                                W_main.real[i1,j1,i2,j2]=1.0


        user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")

    return W_main
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================