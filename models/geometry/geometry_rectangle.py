#-------------------------------------------------------------------------------
# Name:        Rectangle
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
from numpy import zeros, float32, int32, copy

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Pre-requisites
#===============================================================================
geometry_name = "Rectangle"

geometry_parameters = ["width (a.u.)", "height (a.u.)"]
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Source Geometry Model Function
#===============================================================================
def geomFunc(user_interface,context,queue,W_main,N,parameters,parallel,debug):

    user_interface.update_outputText("Starting geometric function (rectangle)...")

    # radius
    width  = parameters[0]
    height = parameters[1]
    wn = 0
    wp = 0
    hn = 0
    hp = 0
    if width%2==0:
        wn = int(width/2)-1
        wp = int(width/2)
    else:
        wn = int(width/2)
        wp = int(width/2)

    if height%2==0:
        hn = int(height/2)-1
        hp = int(height/2)
    else:
        hn = int(height/2)
        hp = int(height/2)


    hh = int(height/2)

    if debug:
        user_interface.update_outputText("width: "+str(width)+"\nheight: "+str(height))

    # parameters
    M = int(N/2)

    CL_geom = None

    if parallel:
        CL_geom=Program(context,"""
            __kernel void increase(__global float *res,
                                   const unsigned int N,
                                   const unsigned int M,
                                   const unsigned int i1,
                                   const unsigned int j1,
                                   const signed int wn,
                                   const signed int wp,
                                   const signed int hn,
                                   const signed int hp)
            {
                int row =  get_global_id(0);
                int col = get_global_id(1);

                int x=col-M;
                int y=M-row;

                if ( x<=wp && y<=hp && x>=wn && y>=hn-1){
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

                if x1<=wp and y1<=hp and y1>=-hn and x1>=-wn:

                    # Data
                    data_real = W_main[i1,j1].real.copy()

                    # creating memory on gpu
                    mf = mem_flags

                    # Result memory -> amplitude and phase conjugation
                    result_real=zeros((N,N)).astype(float32)
                    result_real_gpu_memory = Buffer(context, mf.WRITE_ONLY, size=result_real.nbytes)

                    # Running the program (kernel)
                    CL_geom.increase(queue,data_real.shape,None,result_real_gpu_memory,
                                     int32(N), int32(M), int32(i1), int32(j1), int32(-wn), int32(wp), int32(-hn), int32(hp))

                    # Copying Result to PC memory
                    enqueue_copy(queue,result_real,result_real_gpu_memory)

                    # Copying to Main Matrix
                    W_main.real[i1,j1] =  result_real.copy()

        user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")

    else:
        user_interface.update_outputText("PyOpenCL will NOT be used. Starting Cycle...")
        user_interface.update_outputText("__")
        for i1 in range(0,N):
            user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
            for j1 in range(0,N):
                x1=j1-M
                y1=M-i1

                if x1<=wp and y1<=hp and y1>=-hn and x1>=-wn:

                    for i2 in range(0,N):
                        for j2 in range(0,N):
                            x2=j2-M
                            y2=M-i2
                            if x2<=wp and y2<=hp and y2>=-hn and x2>=-wn:
                                W_main.real[i1,j1,i2,j2]=1.0


        user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")

    return W_main
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================