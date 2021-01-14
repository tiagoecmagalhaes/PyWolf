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

specDenModel_name = "Homogeneous"

specDenModel_parameters = []


def specDenModelFunc(user_interface,context,queue,W_main,N,parameters,parallel,debug):

    #user_interface.update_outputText("Homogeneous Spectral Density function applied!")

    return W_main
    #__________________________________________________________________________


