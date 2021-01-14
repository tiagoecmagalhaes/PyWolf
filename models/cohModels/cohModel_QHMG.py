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
import scipy.special
#------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------

cohModel_name = "Homogeneous Multi-Gaussian"

cohModel_parameters = ["Effective Coherence Length (a.u.):","M (a.u.)"]


def cohModelFunc(user_interface,context,queue,W_main,N,parameters,parallel,debug):

    user_interface.update_outputText("Starting Multi-Gaussian model function...")

    sigma = double(parameters[0])
    parM  = int(parameters[1])

    user_interface.update_outputText("sigma: "+str(sigma))

    user_interface.update_outputText("M: "+str(parM))


    ## Calculating constants
    C0 = 0
    for m in range(1,parM+1):
        C0 += ((-1)**(m-1))*scipy.special.binom(parM,m)/m

    user_interface.update_outputText("C0: "+str(C0))

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
                                       const double sigma,
                                       const unsigned int parM)
                {
                    int row =  get_global_id(0);
                    int col = get_global_id(1);

                    int x2 = col-M;
                    int y2 = M-row;

                    double y22=(double) y2;
                    double x22=(double) x2;

                    double x3=x22-x1;
                    double y3=y22-y1;

                    double r1x=x3*x3;
                    double r1y=y3*y3;

                    double rl=r1x+r1y;



                    double MG = 0;


                    double cc = -1;


                    int m;
                    for(m = 1; m <= parM; m++ ){

                        //------------------------------------------------------
                        // Binomial Coefficient
                        //------------------------------------------------------
                        int i;
                        double facM = 1;
                        for(i = 1; i <= parM; i++ ){
                            facM = facM * i;
                        }

                        int j;
                        double facm = 1;
                        for(j = 1; j <= m; j++ ){
                            facm = facm * j;
                        }

                        int k;
                        double facMm = 1;
                        for(k = 1; k <= (parM-m); k++ ){
                            facMm = facMm * k;
                        }

                        double BC = facM/(facm*facMm);
                        //______________________________________________________


                        double new = pow(cc, m-1) * BC * exp(-rl*rl/(2*m*sigma*sigma))/m;

                        MG = MG + new;
                    }

                    double data_const=(double) data[col + N*row ];

                    double final=data_const*MG;

                    res[col + N*row ]=(float) final;

                }
            """).build()
            #___________________________________________________________________

            user_interface.update_outputText("PyOpenCl will be used. Starting Cycle...")
            user_interface.update_outputText("__")

            for i1 in range(0,N):

                user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")

                for j1 in range(0,N):

                    if not count_nonzero(W_main.real[i1,j1])==0.0:

                        # Defining
                        result=zeros((N,N)).astype(float32)
                        data=copy.copy(W_main.real[i1,j1])

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
                                            double(sigma),int32(parM))

                        #  Copying results to PCmemory
                        enqueue_copy(queue,result,result_gpu_memory)

                        # Copying results to matrices
                        W_main.real[i1,j1]=W_main.real[i1,j1]*result/C0

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

                            rl = r1x + r1y


                            res = 0.0
                            cc  = double(-1)
                            for m in range(1,parM+1):

                                BC = scipy.special.binom(parM,m)

                                res = res + exp(-rl*rl/(2*m*sigma*sigma)) * BC * pow(cc,m-1)/double(m) #scipy.special.binom(parM,m)

                            W_main.real[i1,j1,i2,j2] = W_main.real[i1,j1,i2,j2] * res * double(1.0/C0)



            user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")

        return W_main

    except Exception as error:
        user_interface.update_outputTextSameLine(str(error))



    #__________________________________________________________________________


