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

specModel_name = "Lorentziam"

specModel_parameters = ['Central Frequency (a.u.): ','Gamma (a.u.): ']

import numpy
from numpy import pi
from numpy import sqrt
from numpy import exp
from numpy import sin
from numpy import array




def specFunc(ui,N,parameters,ds,CSDM=None):
    try:
        if CSDM != None:

            # parameters
            w0    = parameters[0]
            std   = parameters[1]

            # parameters
            w0    = parameters[0]
            std   = parameters[1]

            # creating omega array
            CSDM.ds = ds
            if ui.checkBox_FFT.isChecked():
                CSDM.d_omega = (2.0*pi*3e8*sqrt(2.0))/(CSDM.Nz*CSDM.ds*CSDM.theta)
            else:
                CSDM.d_omega = (2.0*pi*3e8*sqrt(2.0))/(CSDM.N*CSDM.ds*CSDM.theta)

            omega_array = []
            for i in range(0,CSDM.Nw):
                omega_array.append(i*CSDM.d_omega)
            omega_array = array(omega_array)

            # creating the spectrum
            spec = std**2/((omega_array-w0)**2+std**2)

            return([omega_array,spec])


        else:

            # parameters
            w0    = parameters[0]
            std   = parameters[1]

            # creating omega array
            numPlanes = int(ui.spinBox_numPlanes.text())
            if numPlanes > 1:
                ds = ui.dx_list[numPlanes-2]

            theta = float(ui.lineEdit_theta.text())

            if ui.checkBox_FFT.isChecked():
                Nz = float(ui.lineEdit_NZ.text())
                ui.d_omega = (2.0*pi*3e8*sqrt(2.0))/(Nz*ds*theta)
            else:
                N =  float(ui.lineEdit_N.text())
                ui.d_omega = (2.0*pi*3e8*sqrt(2.0))/(N*ds*theta)

            omega_array = []
            M = int(N/2)
            for i in range(0,M):
                omega_array.append(i*ui.d_omega)
            omega_array = array(omega_array)

            # creating the spectrum
            #spec = exp(-(omega_array-w0)**2/(2*(std)**2))
            spec = std**2/((omega_array-w0)**2+std**2)

            return([omega_array,spec])



    except Exception as error:
        ui.update_outputText(error)
