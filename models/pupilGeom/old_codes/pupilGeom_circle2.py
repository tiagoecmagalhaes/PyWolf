#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Tiago
#
# Created:     24/01/2020
# Copyright:   (c) Tiago 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------


#==============================================================================
# Where do things come from?
#==============================================================================
from pyopencl import *
from pylab import *
#------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------


pupilGeom_name = "Circle2"

pupilGeom_parameters = ["radius (m)","b"]


def geomFunc(user_interface,context,queue,W_main,N,parameters,parallel,debug):

    user_interface.update_outputText("Starting geometric function...")

    # radius
    radius = parameters[0]

    # text
    user_interface.update_outputText("(radius: "+str(radius)+")")
    print("(radius: "+str(radius)+")")


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
                                   const double radius)
            {
                int row =  get_global_id(0);
                int col = get_global_id(1);

                int x=col-M;
                int y=(M-row);

                double y2=(double) y;
                double x2=(double) x;

                double r2=sqrt(x2*x2+y2*y2);

                if (r2<=radius){
                    res[col + N*row ]=1.0;
                }
            }
        """).build()

        user_interface.update_outputText("PyOpenCL will be used. Starting Cycle...")
        user_interface.update_outputText("__")
        for i1 in range(0,N):
            user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
            print(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
            for j1 in range(0,N):

                # Radius of point P1
                x1=j1-M
                y1=M-i1
                r1=sqrt(y1**2+x1**2)

                if r1<=float(radius):

                    # Defining
                    result=zeros((N,N)).astype(float32)

                    # creating memory on gpu
                    mf = mem_flags

                    # Result memory
                    result_gpu_memory = Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=result)

                    # Running the program (kernel)
                    CL_geom.increase(queue,result.shape,None,result_gpu_memory,int32(N),int32(M),int32(i1),
                                     int32(j1),double(radius))

                    #  Copying results to PCmemory
                    enqueue_copy(queue,result,result_gpu_memory)

                    # Copying results to matrices
                    W_main[i1][j1].real=result
        user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")

    else:
        user_interface.update_outputText("PyOpenCL will NOT be used. Starting Cycle...")
        user_interface.update_outputText("__")
        print("PyOpenCL will NOT be used!")
        for i1 in range(0,N):
            user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
            print(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
            for j1 in range(0,N):
                x1=j1-M
                y1=M-i1
                r1=sqrt(y1**2+x1**2)

                if r1<=float(radius):
                    for i2 in range(0,N):
                        for j2 in range(0,N):
                            x2=j2-M
                            y2=M-i2
                            r2=sqrt(y2**2+x2**2)


                            if r2<=float(radius):
                                W_main.real[i1,j1,i2,j2]=1.0
        user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")

    return W_main
