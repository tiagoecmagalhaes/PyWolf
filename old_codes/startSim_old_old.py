#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Tiago
#
# Created:     28/01/2020
# Copyright:   (c) Tiago 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QInputDialog, QFileDialog, QLabel, QHBoxLayout
from pyopencl import *

current_dir = os.getcwd()
sys.path.insert(1, current_dir+"\plot")
from windowPlot import *

from pylab import *
from numpy import count_nonzero

import sys
import os
import copy

# -- <propFunc> directory
current_dir = os.getcwd()
sys.path.insert(0, current_dir+"\propFunc")
from qfunction import *
from qFFT import *
from qFFT import *
from func_propSpec import *

from class_CSDM import *

current_dir = os.getcwd()
sys.path.insert(1, current_dir+"\plot")

from windowPlot import *
from windowPlot_PI import *
from windowPlot_sourceSDC2D import *
from windowPlot_propSDC import *
from windowPlot_propSDC2D import *
from windowPlot_sourceSpectrum import *
from windowPlot_propSpectrum import *


W_source = None
W_temp = None

def func_startSim(ui,all_parameters):

    #===========================================================================
    # Separating Parameters
    #===========================================================================
    ui.update_outputText("Organizing Parameters...")

    # Name and Time
    sim_name = all_parameters[0][0][0]
    sim_time = all_parameters[0][0][1]

    # PyOpenCl
    sim_usePyOpenCL = all_parameters[0][1][0]
    platform_num    = None
    device_num      = None
    platform_name   = None
    device_name     = None
    if sim_usePyOpenCL:
        platform_num    = all_parameters[0][1][1]
        device_num      = all_parameters[0][1][2]
        platform_name   = None
        device_name     = None

    # saving properties
    toSave           = all_parameters[0][2][0]
    toSavesourcsCSDM = all_parameters[0][2][2]
    toSavePropCSDM   = all_parameters[0][2][3]
    save_dir = None
    if toSave:
        save_dir = all_parameters[0][2][1]

    # debug
    debug = all_parameters[0][3][0]

    # matrix size
    N     = int(all_parameters[0][4][0])
    M     = int(N/2)

    # propagation quantity
    propQuantity  = int(all_parameters[1][0])
    specPropModel = int(all_parameters[1][1])
    theta         = None
    if propQuantity == 1:
        theta = float(all_parameters[1][2])


    #---------------------------------------------------------------------------
    # Spectrum Parameters
    #---------------------------------------------------------------------------
    checkFreq_list     = all_parameters[2][0]
    monochromatic      = checkFreq_list[0]
    quasimonochromatic = checkFreq_list[1]
    polychromatic      = checkFreq_list[2]

    if monochromatic:
        Cfrequency = float(all_parameters[2][1][0])
    else:
        Cfrequency =float(all_parameters[2][3][0])



    chosen_specModel_num  = all_parameters[2][2][0]

    specModelName    = None
    specModelModule  = None
    specModelFunc    = None
    specModelPars    = None

    try:

        if polychromatic or quasimonochromatic:
            specModelName   = all_parameters[2][2][1]
            specModelModule = all_parameters[2][2][2]
            specModelFunc   = all_parameters[2][2][3]
            specModelPars   = all_parameters[2][3]

            ui.update_outputText(specModelName)
            ui.update_outputText(specModelFunc)
            ui.update_outputText(specModelPars)

    except Exception as error:
        ui.update_outputText(error)


    #sourceGeomModel = all_parameters[2]

    #___________________________________________________________________________


    #---------------------------------------------------------------------------
    # Source Parameters
    #---------------------------------------------------------------------------
    #source_list = [source_res,file_list,chosen_geometry,geoModel_list,geoPars_list,cohModel_list,cohPars_list]

    sourceRes = all_parameters[3][0]

    # source from file
    sourceFromFile = all_parameters[3][1][0]
    sourceFileDir  = all_parameters[3][1][1]

    # geometry function
    chosen_geometry = all_parameters[3][2]
    geomName        = all_parameters[3][3][0]
    geomModule      = all_parameters[3][3][1]
    geomFunc        = all_parameters[3][3][2]

    # geometry parameters
    geomPars = all_parameters[3][4]

    # coherence model chosen
    chosen_cohModelName =  all_parameters[3][5][0]
    chosen_cohModelFunc =  all_parameters[3][5][1]

    # coherence model parameters
    cohPars =  all_parameters[3][6]
    #___________________________________________________________________________


    #---------------------------------------------------------------------------
    # Propagation Parameters
    #---------------------------------------------------------------------------
    numPlanes               = all_parameters[4][0]
    distances_list          = all_parameters[4][1]
    farfield_list           = all_parameters[4][2]
    usePupil                = all_parameters[4][3]
    pupilGeo_list           = all_parameters[4][4]
    pupilGeoPars_list       = all_parameters[4][5]
    lens_list               = all_parameters[4][6]
    focalLen_list           = all_parameters[4][7]
    useAberration           = all_parameters[4][8]
    aberrationFunc_list     = all_parameters[4][9]
    aberrationFuncPars_list = all_parameters[4][10]
    #___________________________________________________________________________


    #---------------------------------------------------------------------------
    #///////////////////////////////////////////////////////////////////////////
    #---------------------------------------------------------------------------

    #===========================================================================
    # PyOpenCl
    #===========================================================================
    platform = None
    device   = None
    context  = None
    queue    = None

    if sim_usePyOpenCL:
        platform = ui.list_platforms[platform_num]
        device   = platform.get_devices()[device_num]
        context  = Context(devices=[device])
        queue    = CommandQueue(context,device=device)

        # printing
        out_txt = "Platform Chosen: "+str(ui.list_platforms[platform_num])
        print(out_txt)
        ui.update_outputText(out_txt)

        out_txt = "Device Chosen: "+str(device)
        print(out_txt)
        ui.update_outputText(out_txt)

    else:
        # output txt
        ui.update_outputText("PyOpenCL will not be used.")
    #---------------------------------------------------------------------------
    #///////////////////////////////////////////////////////////////////////////
    #---------------------------------------------------------------------------


    #===========================================================================
    # Propagation
    #===========================================================================

    # parameters
    W_source = None
    W_temp   = None

    # propagation algorithm
    start_prop = 0

    # what propagation algorithm to use
    if quasimonochromatic or monochromatic:
        start_prop = 1
    elif polychromatic:
        if specPropModel == 0:
            start_prop = 1


    if start_prop==1:

        #***********************************************************************
        # Creating or loading source geometry
        #***********************************************************************

        # creating CDSM object for source
        ui.CSDM_source    = CSDM(all_parameters,ui,True)

        # if File
        if sourceFromFile:
            ui.CSDM_source.matrix=load(sourceFileDir) # matrix

        # not from file
        else:
            ui.update_outputText("The cross-spectral density matrix is being created. Please wait...")
            # updating text

            W_temp = zeros((N,N,N,N)).astype(complex64)

            ui.CSDM_source.matrix = ui.geometryModelsFunc[chosen_geometry](ui,context,queue,W_temp,N,geomPars,sim_usePyOpenCL,debug)

            if debug:
                figure()
                title("W_source - Geometry - real values")
                pcolormesh(ui.CSDM_source.matrix[M,M].real)
                show()

            #geomFunc(ui,context,queue,W_temp,N,geomPars,sim_usePyOpenCL,debug)
            #print(W_temp[M,M,M].real)

            # updating text
            ui.update_outputText("The Source geometry of the cross-spectral density matrix has been created!")
        #_______________________________________________________________________


        #=======================================================================
        # Creating Source Coherence Model
        #=======================================================================
        try:
            ui.update_outputText("The Source coherence model will now be constructed...")

            W_temp = ui.CSDM_source.matrix

            if not sourceFromFile:
                ui.CSDM_source.matrix = chosen_cohModelFunc.cohModelFunc(ui,context,queue,W_temp,N,cohPars,sim_usePyOpenCL,debug)

                if debug:
                    figure()
                    title("W_source - CSDM - real values")
                    plot(sqrt(ui.CSDM_source.matrix[M,M,M].real**2+W_source[M,M,M].imag**2),marker="o")
                    grid()
                    show()

            ui.update_outputText("The cross-spectral density of the source has been completed!")

            # PLOTS
            #ui.canvas_plotSourceImage.plot_sourceImage(ui,W_source,N,"Source Image")

            #plot_sourceImage(ui,ui.tab_plotSourceImage,W_source,N)
            #ui.draw_sourceImage()
            #ui.tabWidget_plots.addTab(ui.tab_plotSourceImage, "Source Image")


            #*** Plotting ***
            # adding <TAB Source Image> to <TAB PLOT>
            ui.tabWidget_plots.addTab(ui.tab_plotSourceImage, "Source Image")
            ui.canvasSI = Canvas_sourceImage(ui,ui.CSDM_source.matrix,N)
            QtWidgets.qApp.processEvents()

            #*** Plotting ***
            # adding <TAB Source Image> to <TAB PLOT>
            ui.tabWidget_plots.addTab(ui.tab_plotSourceSDC2D, "Source 2D SDC")
            ui.canvasSourceSDC2d = Canvas_sourceSDC2D(ui,ui.CSDM_source.matrix,N)
            QtWidgets.qApp.processEvents()


        except Exception as error:
            ui.update_outputText(str(error))

        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # Plotting Source Spectrum
        #=======================================================================

        if polychromatic:
            try:
                #*** Plotting ***
                # adding <TAB Source Image> to <TAB PLOT>
                ui.canvasSourceSpec = Canvas_sourceSpec(ui,ui.CSDM_source,N)
                ui.tabWidget_plots.addTab(ui.tab_plotSourceSpec, "Source Spectrum")
                QtWidgets.qApp.processEvents()

            except Exception as error:
                ui.update_outputText(str(error))
        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # Propagating
        #=======================================================================
        try:
            # Propagation is similar for both degree of coherence and spectrum

            # Creating Propagation Matrix
            ui.CSDM_prop    = CSDM(all_parameters,ui)

            ui.CSDM_prop.matrix = copy.copy(ui.CSDM_source.matrix)

            # source spatial resolution
            ds = ui.CSDM_source.ds

            # first plane spatial resolution
            dx = 2*pi*3e8*distances_list[0]/(Cfrequency*N*sourceRes)

            for numPlane in range(0,numPlanes):

                #---------------------------------------------------------------
                # spatial resolution
                #---------------------------------------------------------------
                if numPlane != 0:
                    pass
                else:
                    ds = dx
                    dx = 2*pi*3e8*distances_list[numPlane]/(Cfrequency*N*ds)
                #_______________________________________________________________


                #---------------------------------------------------------------
                # Q functions
                #---------------------------------------------------------------
                if not farfield_list[numPlane]:
                    ui.update_outputText("Multiplying by Q functions...")
                    prop_parameters = [Cfrequency,distances_list[numPlane]]

                    if not farfield_list[numPlane]:
                        ui.CSDM_prop.matrix = func_qfunction(ui,context,queue,ui.CSDM_source.matrix,N,ds,prop_parameters,sim_usePyOpenCL,debug)
                    ui.update_outputText("Task Completed!")

                #else:
                    #W_temp = CSDM_source.matrix
                #_______________________________________________________________

                #---------------------------------------------------------------
                # FFTs
                #---------------------------------------------------------------
                ui.update_outputText("Performing 1st 2D Fourier transforms...")
                ui.update_outputText("___")
                for i1 in range(0,N):
                    ui.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
                    for j1 in range(0,N):
                        if count_nonzero(W_temp[i1,j1])==0:
                            pass
                        else:
                            ui.CSDM_prop.matrix[i1,j1]=func_fft2d(ui,ui.CSDM_prop.matrix[i1,j1],FTinverse=False)
                ui.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")
                ui.update_outputText("2D Fourier transforms completed!")
                #_______________________________________________________________


                #---------------------------------------------------------------
                # Transposing...
                #---------------------------------------------------------------
                ui.update_outputText("Transposing matrix...")
                ui.CSDM_prop.matrix=ui.CSDM_prop.matrix.transpose(2,3,0,1)
                ui.update_outputText("Transposing completed!")
                #_______________________________________________________________


                #---------------------------------------------------------------
                # FFTs
                #---------------------------------------------------------------
                ui.update_outputText("Performing 2nd 2D Fourier transforms...")
                ui.update_outputText("___")
                for i1 in range(0,N):
                    ui.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
                    for j1 in range(0,N):
                        if count_nonzero(W_temp[i1,j1])==0:
                            pass
                        else:
                            ui.CSDM_prop.matrix[i1,j1]=func_fft2d(ui,ui.CSDM_prop.matrix[i1,j1],FTinverse=True)
                ui.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")
                ui.update_outputText("2D Fourier transforms completed!")

                if debug:
                    figure()
                    title("CSDM - after 2D FFT ")
                    plot(sqrt(W_temp[M,M,M].real**2+W_source[M,M,M].imag**2),marker="o")
                    grid()
                    show()
                #_______________________________________________________________


                #---------------------------------------------------------------
                # Q functions
                #---------------------------------------------------------------
                prop_parameters = [Cfrequency,distances_list[numPlane]]

                if not farfield_list[numPlane]:
                    ui.update_outputText("Multiplying by Q functions...")
                    ui.CSDM_prop.matrix = func_qfunction(ui,context,queue,ui.CSDM_prop.matrix,N,dx,prop_parameters,sim_usePyOpenCL,debug)
                ui.update_outputText("Task Completed!")
                #_______________________________________________________________


                #---------------------------------------------------------------
                # Pupil Function
                #---------------------------------------------------------------
                if usePupil[numPlane]:
                    pass

                #_______________________________________________________________


                #---------------------------------------------------------------
                # Lens Function
                #---------------------------------------------------------------
                if lens_list[numPlane]:
                    pass

                #_______________________________________________________________

            # defining CSDM Propagation matrix
            #ui.CSDM_prop.matrix = W_temp

            if debug:
                figure()
                pcolormesh(W_temp[M,M].real)
                show()

            # output message text
            ui.update_outputText("**Propagation Completed**")


            # degree of coherence
            if propQuantity==0:

                # Building Propagation Image
                #

                # Building Propagation 2D SDC
                #

                # Building Propagation SDC
                #

                #---------------------------------------------------------------
                # Plotting
                #---------------------------------------------------------------
                try:
                    #--- Plotting Propagation Image ---
                    # adding <TAB Source Image> to <TAB PLOT>
                    ui.tabWidget_plots.addTab(ui.tab_plotPropImage, "Propagation Image")
                    ui.canvasPI = Canvas_propImage(ui,ui.CSDM_prop.matrix,N)
                    QtWidgets.qApp.processEvents()

                    #--- Plotting Propagation 2D SDC  ----
                    # adding <TAB Source Image> to <TAB PLOT>
                    ui.tabWidget_plots.addTab(ui.tab_plotPropSDC2D, "Propagation 2D SDC")
                    ui.canvasPropSDC2D = Canvas_propSDC2D(ui,ui.CSDM_prop.matrix,N)
                    QtWidgets.qApp.processEvents()

                    #--- Plotting Propagation SDC---
                    # adding <TAB Source Image> to <TAB PLOT>
                    ui.tabWidget_plots.addTab(ui.tab_plotPropSDC, "Propagation SDC")
                    ui.canvasPropSDC = Canvas_propSDC(ui,ui.CSDM_prop.matrix,N)
                    QtWidgets.qApp.processEvents()
                except Exception as error:
                    ui.update_outputText(str(error))
                #_______________________________________________________________


            # if spectrum propagation
            elif propQuantity==1:
                ui.update_outputText("Building Propagation Spectrum...")
                PropSpecRes = propagation_spectrum(ui)
                ui.update_outputText("Propagation Spectrum completed!")

                #=======================================================================
                # Plotting Source Spectrum
                #=======================================================================

                if polychromatic:
                    try:
                        #*** Plotting ***
                        # adding <TAB Source Image> to <TAB PLOT>
                        ui.canvaspropSpec = Canvas_propSpec(ui,ui.CSDM_prop,ui.CSDM_source,N)
                        ui.tabWidget_plots.addTab(ui.tab_plotSourceSpec, "Propagation Spectrum")
                        QtWidgets.qApp.processEvents()

                    except Exception as error:
                        ui.update_outputText(str(error))
                #-----------------------------------------------------------------------
                #///////////////////////////////////////////////////////////////////////
                #-----------------------------------------------------------------------



        except Exception as error:
            ui.update_outputText(str(error))
        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------

    else:
        ui.update_outputText("No propagation algorithm is configured for these conditions.")



    return W_temp
