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
import copy

from numpy import count_nonzero
#------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------

cohModel_name = "Incoherent Voronoi"

cohModel_parameters = ["Random? (0-1)","Number of points:"]


def cohModelFunc(user_interface,context,queue,W_main,N,parameters,parallel,debug):

    user_interface.update_outputText("Starting Gaussian-Schell model function...")

    sigma = float(parameters[0])



    import numpy as np
    from scipy.spatial import cKDTree
    from random import randint

    voronoi_points = []#np.random.rand(n_voronoi, 2)
    #r=voronoi_points*N
    if geom=="Circle":
        for i in range(int(n_voronoi)):
            key=False
            while key==False:
                actual=[0,0]
                actual[0]=randint(0, N)
                actual[1]=randint(0, N)
                new_radius=sqrt(float(actual[0]-N/2)**2+float(actual[1]-N/2)**2)
                print(new_radius,geomPar1)
                if actual not in voronoi_points and new_radius<=geomPar1:
                    voronoi_points.append(actual)
                    key=True
            #r[i][0]=int(r[i][0])
            #r[i][1]=int(r[i][1])
        voronoi_points=array(voronoi_points)
        voronoi_points=voronoi_points.astype(int32)

    elif geom=="Rectangle":
        for i in range(int(n_voronoi)):
            key=False
            while key==False:
                actual=[0,0]
                actual[0]=randint((N/2-geomPar1), (N/2+geomPar1))
                actual[1]=randint((N/2-geomPar2), (N/2+geomPar2))
                if actual not in voronoi_points:
                    voronoi_points.append(actual)
                    key=True
            #r[i][0]=int(r[i][0])
            #r[i][1]=int(r[i][1])
        voronoi_points=array(voronoi_points)
        voronoi_points=voronoi_points.astype(int32)
    elif geom=="No Shape":
        for i in range(int(n_voronoi)):
            key=False
            while key==False:
                actual=[0,0]
                actual[0]=randint(0, N)
                actual[1]=randint(0, N)
                if actual not in voronoi_points:
                    voronoi_points.append(actual)
                    key=True
            #r[i][0]=int(r[i][0])
            #r[i][1]=int(r[i][1])
        voronoi_points=array(voronoi_points)
        voronoi_points=voronoi_points.astype(int32)

    test_points=[]
    for i in range(0,N):
        for j in range(0,N):
            test_points.append([i,j])
    test_points=array(test_points).astype(int32)

    voronoi_kdtree = cKDTree(voronoi_points)

    test_point_dist, test_point_regions = voronoi_kdtree.query(test_points, k=1)

    print(test_point_regions)




















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
                                       const double sigma)
                {
                    int row =  get_global_id(0);
                    int col = get_global_id(1);

                    int y2=-(row-M);
                    int x2=(col-M);

                    double y22=(double) y2;
                    double x22=(double) x2;

                    double x3=x22-x1;
                    double y3=y22-y1;
                    double r1x=x3*x3;
                    double r1y=y3*y3;
                    double rl=r1x+r1y;

                    double arg_miu= -rl/sigma;
                    double data_const=(double) data[col + N*row ];

                    double exp2=exp(arg_miu);
                    double final=data_const*exp2;

                    res[col + N*row ]=(float) final;

                }
            """).build()
            #___________________________________________________________________

            user_interface.update_outputText("PyOpenCl will be used. Starting Cycle...")
            user_interface.update_outputText("__")

            for i1 in range(0,N):

                user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")

                for j1 in range(0,N):

                    if not count_nonzero(W_main[i1,j1])==0:

                        # Defining
                        result=zeros((N,N)).astype(float32)
                        data=copy.copy(W_main[i1,j1].real)

                        # Radius of point P1
                        x1=j1-M
                        y1=M-i1

                        # creating memory on gpu
                        mf = mem_flags

                        # Result memory
                        result_gpu_memory = Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=result)

                        # Data Memory
                        data_gpu_memory = Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data)

                        # Running the program (kernel)
                        CL_pcohGS.increase(queue,result.shape,None,result_gpu_memory,data_gpu_memory,
                                           int32(N),int32(M),int32(i1),int32(j1),double(x1),double(y1),
                                            double(sigma))

                        #  Copying results to PCmemory
                        enqueue_copy(queue,result,result_gpu_memory)

                        # Copying results to matrices
                        W_main.real[i1][j1]=result

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

                            x3=x2-x1
                            y3=y2-y1
                            r1x=x3**2
                            r1y=y3**2
                            rl=r1x+r1y

                            W_main.real[i1,j1,i2,j2]=W_main.real[i1,j1,i2,j2]*exp(-rl/sigma)



            user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")

    except Exception as error:
        user_interface.update_outputTextSameLine(str(error))


    return W_main
    #__________________________________________________________________________


