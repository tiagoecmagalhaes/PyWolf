#-------------------------------------------------------------------------------
# Name:        Gaussian
# Purpose:     PyWolf's Spectrum Profile Model
#
# Author:      Tiago E. C. Magalhaes
#
# Licence:     GNU GENERAL PUBLIC LICENSE Version 3
#-------------------------------------------------------------------------------


#===============================================================================
# Importing Packages
#===============================================================================
import numpy
from numpy import pi
from numpy import sqrt
from numpy import exp
from numpy import sin
from numpy import array
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Pre-requisites
#===============================================================================
specModel_name = "Gaussian"

specModel_parameters = ['Central Frequency: ','Standard Deviation: ']
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Spectrum Profile Model
#===============================================================================
def specFunc(ui,N,parameters,ds,CSDM=None):
    try:
        # if not a preview
        if CSDM != None:

            # parameters
            w0    = parameters[0]
            std   = parameters[1]

            # creating omega array
            CSDM.ds = ds
            if ui.checkBox_FFT.isChecked():
                CSDM.d_omega = (2.0*pi*3e8*sqrt(2.0))/(CSDM.Nz*CSDM.ds*sin(CSDM.theta))
            else:
                CSDM.d_omega = (2.0*pi*3e8*sqrt(2.0))/(CSDM.N*CSDM.ds*sin(CSDM.theta))

            omega_array = []
            for i in range(0,CSDM.Nw):
                omega_array.append(i*CSDM.d_omega)
            omega_array = array(omega_array)

            # creating the spectrum
            spec = exp(-(omega_array-w0)**2/(2*(std)**2))

            return([omega_array,spec])

        # if previewing
        else:


            # parameters
            w0    = parameters[0]
            std   = parameters[1]

            # creating omega array
            numPlanes = int(ui.spinBox_numPlanes.text())
            if numPlanes > 1:
                ds = ui.dx_list[numPlanes-2]

            theta = float(ui.lineEdit_theta.text())

            M = None
            if ui.checkBox_FFT.isChecked():
                Nz = float(ui.lineEdit_NZ.text())
                ui.d_omega = (2.0*pi*3e8*sqrt(2.0))/(Nz*ds*theta)

            else:
                N =  float(ui.lineEdit_N.text())
                ui.d_omega = (2.0*pi*3e8*sqrt(2.0))/(N*ds*theta)


            M = int(N/2)
            omega_array = []

            for i in range(0,M):
                omega_array.append(i*ui.d_omega)
            omega_array = array(omega_array)

            # creating the spectrum
            spec = exp(-(omega_array-w0)**2/(2*(std)**2))

            return([omega_array,spec])

    except Exception as error:
        ui.update_outputText(error)
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================