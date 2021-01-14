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


geometry_name = "Source Plane"

geometry_parameters = []

def geomFunc(user_interface,context,queue,W_main,N,parameters,parallel,debug):

    user_interface.update_outputText("Starting geometric function...")

    # text
    user_interface.update_outputText("This Geometry Model does not require PyOpenCL")

    # parameters
    M = N/2

    user_interface.update_outputText("Starting Cycle...")
    user_interface.update_outputText("__")

    for i1 in range(0,N):
        user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
        for j1 in range(0,N):
            W_main.real[i1,j1] = W_main.real[i1,j1]+1.0

    return W_main
