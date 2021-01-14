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
from scipy.special import jv

from numpy import count_nonzero
#------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------

cohModel_name = "Besinc"

cohModel_parameters = ["Alpha (a.u.):"]


def cohModelFunc(user_interface,context,queue,W_main,N,parameters,parallel,debug):

    user_interface.update_outputText("Starting Besinc model function...")

    alpha = float(parameters[0])

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
                                       const double a)
                {
                    int col =  get_global_id(0);
                    int row = get_global_id(1);

                    int y2 = -(row-M);
                    int x2 = (col-M);


                    double y22 = (double) y2;
                    double x22 = (double) x2;

                    double b1 = (double) x1-1*x2;
                    double b2 = (double) y1-1*y2;
                    double b  = (double) sqrt(b1*b1+b2*b2);
                    //double J1 = (double) 1 - pown(a*b,2)/8.0 + pown(a*b,4)/192.0 - pown(a*b,6)/9216.0 + pown(a*b,8)/737280.0 - pown(a*b,10)/88473600.0 + pown(a*b,12)/14863564800.0 ;

                    double c = (double) a*b;
                    double zero = (double) 0.0;
                    double sum = 0;


                   double x = c;

                   double ax,z;
                   double xx,y,ans,ans1,ans2;

                   if ((ax=fabs(x)) < 8.0) {
                      y=x*x;
                      ans1=x*(72362614232.0+y*(-7895059235.0+y*(242396853.1
                         +y*(-2972611.439+y*(15704.48260+y*(-30.16036606))))));
                      ans2=144725228442.0+y*(2300535178.0+y*(18583304.74
                         +y*(99447.43394+y*(376.9991397+y*1.0))));
                      ans=ans1/ans2;
                   } else {
                      z=8.0/ax;
                      y=z*z;
                      xx=ax-2.356194491;
                      ans1=1.0+y*(0.183105e-2+y*(-0.3516396496e-4
                         +y*(0.2457520174e-5+y*(-0.240337019e-6))));
                      ans2=0.04687499995+y*(-0.2002690873e-3
                         +y*(0.8449199096e-5+y*(-0.88228987e-6
                         +y*0.105787412e-6)));
                      ans=sqrt(0.636619772/ax)*(cos(xx)*ans1-z*sin(xx)*ans2);
                      if (x < 0.0) ans = -ans;
                   }

                   if (c>zero)
                   {
                   ans = 2*ans/c;
                   }
                   else{
                   ans = 1.0;
                   }





                    double data_const = (double) data[col + N*row ];

                    double final;

                    if (data_const>zero) {
                        final = (double) data_const*ans;
                    }
                    else {
                        final = zero;
                    }



                    res[col + N*row ]= (float) final;


                }
            """).build()
            #___________________________________________________________________

            user_interface.update_outputText("PyOpenCl will be used. Starting Cycle...")
            user_interface.update_outputText("__")

            for i1 in range(0,N):

                user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")

                for j1 in range(0,N):

                    if not count_nonzero(W_main.real[i1,j1])==0:

                        # Defining
                        result = zeros((N,N)).astype(float32)
                        data   = copy.copy(W_main[i1,j1].real)

                        # Radius of point P1
                        x1 = j1-M
                        y1 = M-i1

                        # creating memory on gpu
                        mf = mem_flags

                        # Result memory
                        result_gpu_memory = Buffer(context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=result)

                        # Data Memory
                        data_gpu_memory = Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data)

                        # Running the program (kernel)
                        CL_pcohGS.increase(queue,result.shape,None,result_gpu_memory,data_gpu_memory,
                                           int32(N),int32(M),int32(i1),int32(j1),double(x1),double(y1),
                                            double(alpha))

                        #  Copying results to PCmemory
                        enqueue_copy(queue,result,result_gpu_memory)

                        # Copying results to matrices
                        W_main.real[i1,j1]=W_main.real[i1,j1]*result


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

                            b = sqrt((x1-x2)**2+(y1-y2)**2)

                            arg1=alpha*b

                            if arg1==0:
                                y=1
                            else:
                                y=(2*jv(1,arg1)/arg1)

                            W_main.real[i1,j1,i2,j2]=W_main.real[i1,j1,i2,j2]*y



            user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")

    except Exception as error:
        user_interface.update_outputTextSameLine(str(error))


    return W_main
    #__________________________________________________________________________


