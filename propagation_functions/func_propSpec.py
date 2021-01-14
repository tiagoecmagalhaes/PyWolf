# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Name:        FFT
# Purpose:     PyProPCL
#
# Author:      Tiago Magalhaes
#
# Created:     2017
# Copyright:   (c) Tiago Magalhaes 2017
# Licence:     IA
#-----------------------------------------------------------------------------
##
##
#==============================================================================
# Where do things come from?
#==============================================================================
from pyopencl import *
from pylab import *
import copy
#------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
#
#
#==============================================================================
# Propagation Spectrum
#==============================================================================

def propagation_spectrum(ui,N,debug):
    "Calculates the propagation spectrum"

    try:
        M = int(N/2)


        ## test-----------------------------------------------------------------
        """
        Ciiii_real=[]
        Ciiii_imag=[]
        for i in range(0,N):
            Ciiii_real.append(ui.CSDM_prop.matrix[i,i,i,i].real)
            Ciiii_imag.append(ui.CSDM_prop.matrix[i,i,i,i].imag)
        Ciiii_real=array(Ciiii_real) # array
        Ciiii_imag=array(Ciiii_imag) # array

        if True:
            figure()
            title("test")
            plot(sqrt(Ciiii_real**2+Ciiii_imag**2),linewidth=0.5,marker="o")
            grid()
            show()
        """

        ##----------------------------------------------------------------------

        Ciiii_real = []
        Ciiii_imag = []
        Ciiii      = []
        for i in range(M,N):
            Ciiii.append(ui.CSDM_prop.matrix[i,i,i,i])
            Ciiii_real.append(ui.CSDM_prop.matrix[i,i,i,i].real)
            Ciiii_imag.append(ui.CSDM_prop.matrix[i,i,i,i].imag)
        Ciiii_real = array(Ciiii_real) # array
        Ciiii_imag = array(Ciiii_imag) # array
        Ciiii      = array(Ciiii) # array

        figure()
        title("real")
        plot(Ciiii_real/Ciiii_real.max())
        grid()

        figure()
        title("imag")
        plot(Ciiii_imag)

        show()

        # defining arrays
        ui.CSDM_prop.Ciiii_real = Ciiii_real#/Ciiii_real.max() # normalizing
        ui.CSDM_prop.Ciiii_imag = Ciiii_imag#/Ciiii_imag.max() # normalizing

        if debug:
            figure()
            title("W_k")
            plot(ui.CSDM_source.omega_array,ui.CSDM_prop.Ciiii_real,linewidth=0.5,marker="o")
            grid()
            show()

        # angular frequency array
        ui.CSDM_prop.omega_array = copy.copy(ui.CSDM_source.omega_array)

        # far-field spectrum
        ui.CSDM_prop.spectrum  = ui.CSDM_source.spectrum*ui.CSDM_prop.Ciiii_real
        #ui.CSDM_prop.spectrum  = ui.CSDM_prop.spectrum.real#sqrt(ui.CSDM_prop.spectrum.real**2+ui.CSDM_prop.spectrum.imag**2)
        #ui.CSDM_prop.spectrum  = ui.CSDM_prop.spectrum/ui.CSDM_prop.spectrum.max()
        #ui.update_outputText("so far so good")



    except Exception as error:
        ui.update_outputText(error)




#------------------------------------------------------------------------------
#//////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------
