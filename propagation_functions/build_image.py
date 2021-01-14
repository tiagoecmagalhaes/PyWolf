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

from numpy import *
#------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------


def buildCSDMimage(ui,context,queue,W_temp,N,image_array,parallel,debug):

    ui.update_outputText("Starting function (image from file)...")

    # debug
    if debug:
        ui.update_outputText("N: "+str(N)+")")

    # parameters
    M = N/2

    CL_geom = None

    if False:#parallel:
        CL_geom=Program(context,"""

            __kernel void increase(__global float *res,
                                   const unsigned int N,
                                   const unsigned int i1,
                                   const unsigned int j1,
                                   const double image)
            {
                int row =  get_global_id(0);
                int col = get_global_id(1);

                if ( row == i1 && col == j1) {

                    res[col + N*row ] = (float) image;

                }

            }
        """).build()

        ui.update_outputText("PyOpenCL will be used. Starting Cycle...")
        ui.update_outputText("__")

        import copy

        for i1 in range(0,N):
            ui.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
            for j1 in range(0,N):

                x1 = j1-M
                y1 = M-i1

                # Defining
                result = ones((N,N)).astype(float32)

                # creating memory on gpu
                mf = mem_flags

                # Result memory
                result_gpu_memory = Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=result)

                # Running the program (kernel)
                CL_geom.increase(queue,result.shape,None,result_gpu_memory,int32(N),int32(i1),int32(j1),double(image_array[i1,j1]))

                #  Copying results to PCmemory
                enqueue_copy(queue,result,result_gpu_memory)

                # Copying results to matrices
                W_temp[i1,j1].real = W_temp[i1,j1].real*result

        ui.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")

    else:
        ui.update_outputText("PyOpenCL will NOT be used. Starting Cycle...")
        ui.update_outputText("__")

        for i1 in range(0,N):
            ui.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
            for j1 in range(0,N):
                    if image_array[i1,j1]==0:
                           W_temp[i1,j1] *= 0.0



        ui.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")

    if debug:
        temp_image = zeros((N,N)).astype(float32)
        for i in range(0,N):
            for j in range(0,N):
                temp_image[i,j] = W_temp[i,j,i,j].real

        figure()
        pcolormesh(temp_image)
        colorbar()
        show()

    return W_temp
