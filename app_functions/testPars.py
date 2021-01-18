#-------------------------------------------------------------------------------
# Name:        TestPars
# Purpose:     PyWolf's function to test input parameters
#
# Author:      Tiago E. C. Magalhaes
#
# Licence:     GNU GENERAL PUBLIC LICENSE Version 3
#-------------------------------------------------------------------------------


#===============================================================================
# Importing Packages
#===============================================================================
# NumPy
from numpy import pi

# Time
import time
from datetime import datetime

# os
import os

# PyQT5
from PyQt5 import QtCore, QtGui, QtWidgets

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# FUNCTION TEST PARAMETERS
#===============================================================================
def func_testPars(ui):

    #===========================================================================
    # Collecting parameters
    #===========================================================================
    # adding text to app

    # options
    nameTime_list = [ui.lineEdit_simName.text(),ui.give_time()]
    pyopencl_list = [ui.checkBox_pyopencl.isChecked(),ui.comboBox_platform.currentIndex(),ui.comboBox_device.currentIndex()]
    save_list     = [ui.checkBox_save.isChecked(),ui.saveDirName,ui.checkBox_saveSourceCSDA.isChecked(),ui.checkBox_savePropCSDA.isChecked()]
    debug_list    = [ui.checkBox_debug.isChecked()]
    matrix_list   = [ui.lineEdit_N.text(),ui.checkBox_FFT.isChecked(), ui.lineEdit_NZ.text()]
    ##schedule      = [ui.checkBox_schedule.isChecked(),ui.dateTimeEdit.text()]
    options_list  = [nameTime_list, pyopencl_list,save_list,debug_list,matrix_list]

    # propagation quantity
    propQ_list = [ui.comboBox_propQuant.currentIndex(),ui.comboBox_specPropModels.currentIndex(), ui.lineEdit_theta.text()]

    # spectrum parameters
    radio_list       = [ui.radioButton_1freq.isChecked(),ui.radioButton_quasi.isChecked(),ui.radioButton_poly.isChecked()]
    Cfreq_list       = [ui.lineEdit_centralFreq.text()]
    chosen_specModel = ui.comboBox_specType.currentIndex()
    specModel_list   = [chosen_specModel,ui.specModel_list[chosen_specModel][0], ui.specModel_list[chosen_specModel][1], ui.specModelsFunc[chosen_specModel]]
    specPars_list    = []
    for i in range(0,len(ui.specModelPar_list[chosen_specModel])):
        specPars_list.append(ui.specModel_lineEditParameters[i].text())
    spec_list = [radio_list,Cfreq_list,specModel_list,specPars_list]

    #---------------------------------------------------------------------------
    # Source Mode Parameters
    #---------------------------------------------------------------------------
    source_res      = ui.lineEdit_sourceRes.text()

    file_list       = [ui.checkBox_geoFromFile.isChecked(), ui.lineEdit_dirGeoMatrix.text(), ui.checkBox_CSDAFromFile.isChecked(), ui.lineEdit_dirCSDAmatrix.text()]

    #--> Coherence
    chosen_geometry = ui.comboBox_geometry.currentIndex()
    geoModel_list   = [ui.geometry_list[chosen_geometry][0],ui.geometry_list[chosen_geometry][1],ui.geometryModelsFunc[chosen_geometry]]
    geoPars_list    = []
    for i in range(0,len(ui.geometryPar_list[chosen_geometry])):
        geoPars_list.append(ui.geometry_lineEditParameters[i].text())
    chosen_cohModel = ui.comboBox_cohModel.currentIndex()
    cohModel_list   = [ui.cohModel_list[chosen_cohModel][0],ui.cohModel_list[chosen_cohModel][1]]
    cohPars_list    = []  # Coherence Model Parameters:
    for i in range(0,len(ui.cohModelPar_list[chosen_cohModel])):
        cohPars_list.append(ui.cohModel_lineEditParameters[i].text())

    #--> Custom Spectral Density
    useSpecDen              = ui.checkBox_specDen.isChecked()
    chosen_specDensityModel = ui.comboBox_specDenModel.currentIndex()
    specDensityModel_list   = [ui.specDenModel_list[chosen_specDensityModel][0],ui.specDenModel_list[chosen_specDensityModel][1]]
    specDensityPars_list    = []
    ## Spectral density Model Parameters
    for i in range(0,len(ui.specDenPar_list[chosen_specDensityModel])):
        specDensityPars_list.append(ui.specDen_lineEditParameters[i].text())

    source_list = [source_res,file_list,chosen_geometry,geoModel_list,geoPars_list,cohModel_list,cohPars_list,useSpecDen,specDensityModel_list,specDensityPars_list]
    #___________________________________________________________________________


    #---------------------------------------------------------------------------
    # Propagation System
    #---------------------------------------------------------------------------

    num_propPlanes = int(ui.spinBox_numPlanes.text())
    distances_list = []
    farfield_list  = []

    # PUPIL
    usePupil            = []   # [True/False,True/False,True/False]
    pupilGeo_list       = []   # [chosen_model_Plane1, chosen_model_Plane2, chosen_model_Plane3]
    pupilGeoPars_list   = []   # [chosen_modelPars_Plane1,chosen_modelPars_Plane2,chosen_modelPars_Plane3]

    # OPTICS
    useOptics           = [] # [True/False,True/False,True/False]
    optDevices_list     = [] # [chosen_model_Plane1, chosen_model_Plane2, chosen_model_Plane3]
    optDevicesPars_list = [] # [chosen_modelPars_Plane1,chosen_modelPars_Plane2,chosen_modelPars_Plane3]

    try:
        for numP in range(0,num_propPlanes):
            distances_list.append(ui.lineEdit_distances_list[numP].text())

            farfield_list.append(ui.checkBox_farfied_list[numP].isChecked())

            # PUPIL
            usePupil.append(ui.checkBox_pupil_list[numP].isChecked())
            chosen_pupilFunc = int(ui.comboBox_pupilGeom_list[numP].currentIndex())
            pupilGeo_list.append([chosen_pupilFunc,ui.pupilGeomFunc_list[numP][chosen_pupilFunc][0],ui.pupilGeomFunc_list[numP][chosen_pupilFunc][1], ui.pupilGeomFunc_list[numP][chosen_pupilFunc][2]])
            if usePupil[-1]:
                if type(ui.comboBox_pupilGeom_list[numP].currentIndex()) == int:
                    actual_pupilGeoPar = []
                    for i in range(0, len(ui.pupilGeomFuncPars_list[numP][pupilGeo_list[numP][0]])):
                        actual_pupilGeoPar.append(ui.pupilGeom_lineEditParameters[numP][i].text())
                    pupilGeoPars_list.append(actual_pupilGeoPar)

            # OPTICS
            useOptics.append(ui.checkBox_optics_list[numP].isChecked())
            chosen_optDeviceFunc = int(ui.comboBox_optDeviceFunc_list[numP].currentIndex())
            optDevices_list.append([chosen_optDeviceFunc,ui.optDeviceFunc_list[numP][chosen_optDeviceFunc][0],ui.optDeviceFunc_list[numP][chosen_optDeviceFunc][1], ui.optDeviceFunc_list[numP][chosen_optDeviceFunc][2]])
            if useOptics[-1]:
                if type(ui.comboBox_optDeviceFunc_list[numP].currentIndex()) == int:
                    actual_optDeviceFuncPar=[]
                    for i in range(0, len(ui.optDeviceFuncPars_list[numP][optDevices_list[numP][0]])):
                        actual_optDeviceFuncPar.append(ui.optDevicePars_lineEditParameters[numP][i].text())
                    optDevicesPars_list.append(actual_optDeviceFuncPar)

        # PROPAGATION PLANE LIST
        propPlanes_list = [num_propPlanes, distances_list,farfield_list,usePupil,pupilGeo_list,pupilGeoPars_list,useOptics,optDevices_list,optDevicesPars_list]

    #___________________________________________________________________________

    except Exception as error:
        ui.update_outputText(error+" in testPars"+"at Collecting Parameters")

    #----ALL PARAMETERS---------------------------------------------------------
    all_parameters_list = [options_list, propQ_list, spec_list, source_list, propPlanes_list]
    #___________________________________________________________________________


    #===========================================================================
    # Testing parameters
    #===========================================================================

    output_text = ""

    #---------------------------------------------------------------------------
    # Options
    #---------------------------------------------------------------------------
    if nameTime_list[0][0] == "":
        ui.update_outputText("[Error] Please, give a name to the simulation.")
        return([False,all_parameters_list])
    elif len(nameTime_list[0][0])>=20:
        ui.update_outputText("[Error] The name of the simulations is too long. It cannot contain more than 20 characters.")
        return([False,all_parameters_list])

    if options_list[1][0]:
        if type(options_list[1][1]) != int:
            ui.update_outputText("[Error] No platform has been selected.")
            return([False,all_parameters_list])
        elif type(options_list[1][2]) != int:
            ui.update_outputText("[Error] No Device has been selected.")
            return([False,all_parameters_list])

    ## time in folder
    time_now=datetime.now()
    minutes=None
    if int(time_now.minute)<10:
        minutes="0"+str(time_now.minute)
    else:
        minutes=str(time_now.minute)
    add_directory = None
    #___________________________________________________________________________


    #---------------------------------------------------------------------------
    # Removing last spaces
    #---------------------------------------------------------------------------
    sim_name = nameTime_list[0]
    if sim_name[-1]==" ":
        N = len(sim_name)
        last = False
        count = 0
        for i in range(N-1,0,-1):
            if sim_name[i] == " ":
                if not last:
                    count+=1
            else:
                last = True
        nameTime_list[0]= sim_name[:-count]
    #___________________________________________________________________________


    #---------------------------------------------------------------------------
    # Creating Directory
    #---------------------------------------------------------------------------
    ##try:
        ##add_directory="\\"+"results__"+str(time_now.day)+"-"+str(time_now.month)+"-"+str(time_now.year)+\
        ##"_"+str(time_now.hour)+"h"+minutes+"_"+nameTime_list[0]
    ##except:
        ##add_directory="\\"+"results__"+str(time_now.day)+"-"+str(time_now.month)+"-"+str(time_now.year)+\
        ##"_"+str(time_now.hour)+"h"+minutes
    #---------------------------------------------------------------------------

    if options_list[2][0]:
         options_list[2][1] = options_list[2][1]+add_directory
         try:
            os.makedirs(options_list[2][1])
            ui.update_outputText("Directory created in <"+str(options_list[2][1])+">")
         except:
            ui.update_outputText("[Error] Unable to create save directory <"+str(options_list[2][1])+">")
            return([False,all_parameters_list])

    try:
        N_temp = int(options_list[4][0])
        if N_temp < 0:
            ui.update_outputText("[Error] Parameter <N> must be positive.")
            return([False,all_parameters_list])
        else:
            try:
                if options_list[4][1]:
                    NZ = int(options_list[4][2])
                    if NZ <= N_temp:
                        ui.update_outputText("[Error] The total zero padding matrix must be greater than N. If possible, use powers of 2.")
                    else:
                        all_parameters_list[0][4][0] = N_temp
                        all_parameters_list[0][4][2] = NZ


            except:
                ui.update_outputText("[Error] Parameter <Total Matrix Size> must be an integer.")
                return([False,all_parameters_list])


    except:
        ui.update_outputText("[Error] Parameter <N> must be an integer.")
        return([False,all_parameters_list])

    #___________________________________________________________________________


    #---------------------------------------------------------------------------
    # Propagation Quantity and Spectrum Parameters
    #---------------------------------------------------------------------------
    # propagation of spectrum
    if propQ_list[0]==1:
        # 1 freq
        if spec_list[0][0] or spec_list[0][1]:
            ui.update_outputText("[Error] For the propagation of the spectrum of light, you must select polychromatic spectrum.")
            return([False,all_parameters_list])
        try:
            a = float(propQ_list[2])
            if abs(a)>pi:
                ui.update_outputText("[Error] For the propagation of the spectrum of light, the angle of propagation must be -Pi and Pi")
                return([False,all_parameters_list])
        except:
            ui.update_outputText("[Error] For the propagation of the spectrum of light, the angle of propagation must be -Pi and Pi")
            return([False,all_parameters_list])


    # degree of coherence
    if propQ_list[0]==0:
        if spec_list[0][0]:
            # angular frequency
            try:
                omega0 = float(spec_list[1][0])
                if omega0<0.0:
                    ui.update_outputText("[Error] The Central angular frequency must be positive.")
                    return([False,all_parameters_list])
                else:
                    all_parameters_list[2][1][0] = omega0
            except:
                ui.update_outputText("[Error] The Central angular frequency must be a float/int.")
                return([False,all_parameters_list])

    if spec_list[0][1] or spec_list[0][2]:
        for i in range(0,len(specPars_list)):
            if specPars_list[i]!= "":
                try:
                    a = float(specPars_list[i])
                    all_parameters_list[2][3][i]=a
                except:
                    ui.update_outputText("[Error] The parameters of the spectrum model must be float/int.")
                    return([False,all_parameters_list])
            else:
                ui.update_outputText("[Error] Please fill in the spectrum parameters.")
                return([False,all_parameters_list])
    #___________________________________________________________________________


    #---------------------------------------------------------------------------
    # Source Parameters
    #---------------------------------------------------------------------------
    sourceRes_temp = source_list[0]
    if sourceRes_temp != "":
        try:
            b = float(sourceRes_temp)
            if b<0:
                ui.update_outputText("[Error] The source spatial resolution must be positive.")
                return([False,all_parameters_list])
            else:
                all_parameters_list[3][0] = b
        except:
            ui.update_outputText("[Error] The source spatial resolution must be float/int.")
            return([False,all_parameters_list])
    else:
        ui.update_outputText("[Error] Please fill in the source spatial resolution.")
        return([False,all_parameters_list])

    #---------------------------------------------------------------------------
    # No geometry or CSDA is pre-loaded
    #---------------------------------------------------------------------------
    if not file_list[0] and not file_list[2]:
        ui.update_outputText("No geometry or CSDA is pre-loaded.")

        # testing geometrical model parameters
        for i in range(0,len(geoPars_list)):
            if geoPars_list[i]!= "":
                try:
                    a = float(geoPars_list[i])
                    all_parameters_list[3][4][i]=a
                except:
                    ui.update_outputText("[Error] The parameters of the source geometrical model must be float/int.")
                    return([False,all_parameters_list])
            else:
                ui.update_outputText("[Error] Please fill in the source geometrical model parameters.")
                return([False,all_parameters_list])

        # testing source coherence model parameters
        for i in range(0,len(cohPars_list)):
            if cohPars_list[i]!= "":
                try:
                    a = float(cohPars_list[i])
                    all_parameters_list[3][6][i]=a

                except:
                    ui.update_outputText("[Error] The parameters of the source coherence model must be float/int.")
                    return([False,all_parameters_list])
            else:
                ui.update_outputText("[Error] Please fill in the source coherence model parameters.")
                return([False,all_parameters_list])

        # testing custom spectral denisty parameters
        if useSpecDen:
            for i in range(0,len(cohPars_list)):
                if specDensityPars_list[i]!= "":
                    try:
                        a = float(specDensityPars_list[i])
                        all_parameters_list[3][9][i]=a

                    except:
                        ui.update_outputText("[Error] The parameters of the spectral density model must be float/int.")
                        return([False,all_parameters_list])
                else:
                    ui.update_outputText("[Error] Please fill in the source spectral density model parameters.")
                    return([False,all_parameters_list])
    #---------------------------------------------------------------------------
    #///////////////////////////////////////////////////////////////////////////
    #---------------------------------------------------------------------------


    elif file_list[0] and not file_list[2]:
        ##ui.update_outputText("Geometry pre-loaded.")

        # testing source coherence model parameters
        for i in range(0,len(cohPars_list)):
            if cohPars_list[i]!= "":
                try:
                    a = float(cohPars_list[i])
                    all_parameters_list[3][6][i]=a

                except:
                    ui.update_outputText("[Error] The parameters of the source coherence model must be float/int.")
                    return([False,all_parameters_list])
            else:
                ui.update_outputText("[Error] Please fill in the source coherence model parameters.")
                return([False,all_parameters_list])

    else:
        ui.update_outputText("CSDA is pre-loaded.")

    """
    elif file_list[0] and not file_list[2]:

        # testing source spectral density model parameters
        for i in range(0,len(specDensityPars_list)):
            if specDensityPars_list[i]!= "":
                try:
                    a = float(specDensityPars_list[i])
                    all_parameters_list[3][8][i]=a
                except:
                    ui.update_outputText("[Error] The parameters of the source spectral density model must be float/int.")
                    return([False,all_parameters_list])
            else:
                ui.update_outputText("[Error] Please fill in the source spectral density model parameters.")
                return([False,all_parameters_list])
    """
    #___________________________________________________________________________


    #---------------------------------------------------------------------------
    # Propagation Parameters
    #---------------------------------------------------------------------------

    for iP in range(0,num_propPlanes):
        # distance
        if distances_list[iP]!="":
            try:
                dist_temp = float(distances_list[iP])
                if dist_temp<0.0:
                    ui.update_outputText("[Error] The distance in Plane "+str(iP+1)+" must be positive.")
                    return([False,all_parameters_list])
                else:
                    all_parameters_list[4][1][iP] = dist_temp
            except:
                ui.update_outputText("[Error] The distance in Plane "+str(iP+1)+" must be a float/int.")
                return([False,all_parameters_list])
        else:
            ui.update_outputText("[Error] Please fill in the distance of Plane "+str(iP+1)+" .")
            return([False,all_parameters_list])

        if usePupil[iP]:
            # testing pupil model parameters
            for i in range(0,len(pupilGeoPars_list[iP])):

                if pupilGeoPars_list[iP][i]!= "":
                    try:
                        a = float(pupilGeoPars_list[iP][i])
                        all_parameters_list[4][5][iP][i]=a
                    except:
                        ui.update_outputText("[Error] The parameters of the pupil geometric model must be float/int.")
                        return([False,all_parameters_list])
                else:
                    ui.update_outputText("[Error] Please fill in the pupil geometric model parameters in Plane "+str(iP)+".")
                    return([False,all_parameters_list])

        # Optics
        if useOptics[iP]:
            for i in range(0,len(optDevicesPars_list[iP])):
                if optDevicesPars_list[iP][i]!= "":
                    try:
                        a = float(optDevicesPars_list[iP][i])
                        all_parameters_list[4][8][iP][i] = a
                    except:
                        ui.update_outputText("[Error] The parameters of the Optics model must be float/int.")
                        return([False,all_parameters_list])
                else:
                    ui.update_outputText("[Error] Please fill in the Optics model parameters.")
                    return([False,all_parameters_list])

    #___________________________________________________________________________

    # OK
    ui.update_outputText("All parameters are OK.")

    # return list = [All ok?, all parameters, output_info]
    return_list = [True,all_parameters_list]
    #print(return_list)
    return return_list

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================
