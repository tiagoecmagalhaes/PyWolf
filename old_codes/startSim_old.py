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

current_dir = os.getcwd()
sys.path.insert(0, current_dir+"\propFunc")
from qfunction import *
from qFFT import *

from class_CSDM import *

current_dir = os.getcwd()
sys.path.insert(1, current_dir+"\plot")

from windowPlot import *
from windowPlot_PI import *
from windowPlot_sourceSDC2D import *
from windowPlot_propSDC import *
from windowPlot_propSDC2D import *
from windowPlot_sourceSpectrum import *


W_source = None
W_temp = None

def func_startSim(user_interface,all_parameters):

    #===========================================================================
    # Separating Parameters
    #===========================================================================
    user_interface.update_outputText("Organizing Parameters...")

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
    propQuantity   = int(all_parameters[1][0])
    frequencyIndep = int(all_parameters[1][1])


    #---------------------------------------------------------------------------
    # Spectrum Parameters
    #---------------------------------------------------------------------------
    checkFreq_list     = all_parameters[2][0]
    monochromatic      = checkFreq_list[0]
    quasimonochromatic = checkFreq_list[1]
    polychromatic      = checkFreq_list[2]

    Cfrequency       = all_parameters[2][1][0]
    chosen_specModel = all_parameters[2][2]

    specModelName    = None
    specModelFunc    = None
    specModelPars    = None
    if polychromatic or quasimonochromatic:
        specModelName = all_parameters[2][3][chosen_specModel][0]
        specModelFunc = all_parameters[2][3][chosen_specModel][1]
        specModelPars = all_parameters[2][4]

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
    geomFunc        = user_interface.geometryModelsFunc[chosen_geometry]

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
        platform = user_interface.list_platforms[platform_num]
        device   = platform.get_devices()[device_num]
        context  = Context(devices=[device])
        queue    = CommandQueue(context,device=device)

        # printing
        out_txt = "Platform Chosen: "+str(user_interface.list_platforms[platform_num])
        print(out_txt)
        user_interface.update_outputText(out_txt)

        out_txt = "Device Chosen: "+str(device)
        print(out_txt)
        user_interface.update_outputText(out_txt)

    else:
        # output txt
        user_interface.update_outputText("PyOpenCL will not be used.")
    #---------------------------------------------------------------------------
    #///////////////////////////////////////////////////////////////////////////
    #---------------------------------------------------------------------------


    #===========================================================================
    # Monochromatic or Quasimonochromatic Case
    #===========================================================================

    # parameters
    W_source = None
    W_temp   = None


    if quasimonochromatic or monochromatic:
        #***********************************************************************
        # Creating or laoding source geometry
        #***********************************************************************

        if sourceFromFile:
            W_source=load(sourceFileDir)
        else:
            user_interface.update_outputText("The cross-spectral density matrix is being created. Please wait...")
            # updating text

            W_source   = zeros((N,N,N,N)).astype(complex64)

            W_temp = user_interface.geometryModelsFunc[chosen_geometry](user_interface,context,queue,W_source,N,geomPars,sim_usePyOpenCL,debug)

            if debug:
                figure()
                title("W_source - Geometry - real values")
                pcolormesh(W_source[M,M].real)
                show()

            #geomFunc(user_interface,context,queue,W_temp,N,geomPars,sim_usePyOpenCL,debug)
            print(W_temp[M,M,M].real)

            # updating text
            user_interface.update_outputText("The Source geometry of the cross-spectral density matrix has been created!")
        #_______________________________________________________________________


        #=======================================================================
        # Creating Source Coherence Model
        #=======================================================================
        try:
            user_interface.update_outputText("The Source coherence model will now be constructed...")

            if not sourceFromFile:

                source_CSDM = CSDM()
                W_source = chosen_cohModelFunc.cohModelFunc(user_interface,context,queue,W_temp,N,cohPars,sim_usePyOpenCL,debug)

                if debug:
                    figure()
                    title("W_source - CSDM - real values")
                    plot(sqrt(W_source[M,M,M].real**2+W_source[M,M,M].imag**2),marker="o")
                    grid()
                    show()

            user_interface.update_outputText("The cross-spectral density of the source has been completed!")

            # PLOTS
            #user_interface.canvas_plotSourceImage.plot_sourceImage(user_interface,W_source,N,"Source Image")

            #plot_sourceImage(user_interface,user_interface.tab_plotSourceImage,W_source,N)
            #user_interface.draw_sourceImage()
            #user_interface.tabWidget_plots.addTab(user_interface.tab_plotSourceImage, "Source Image")


            #*** Plotting ***
            # adding <TAB Source Image> to <TAB PLOT>
            user_interface.tabWidget_plots.addTab(user_interface.tab_plotSourceImage, "Source Image")
            user_interface.canvasSI = Canvas_sourceImage(user_interface,W_source,N)
            QtWidgets.qApp.processEvents()

            #*** Plotting ***
            # adding <TAB Source Image> to <TAB PLOT>
            user_interface.tabWidget_plots.addTab(user_interface.tab_plotSourceSDC2D, "Source 2D SDC")
            user_interface.canvasSourceSDC2d = Canvas_sourceSDC2D(user_interface,W_source,N)
            QtWidgets.qApp.processEvents()


        except Exception as error:
            user_interface.update_outputText(str(error))

        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        if True:
            try:
                #*** Plotting ***
                # adding <TAB Source Image> to <TAB PLOT>
                user_interface.canvasSourceSpec = Canvas_sourceSpec(user_interface,W_source,N)
                user_interface.tabWidget_plots.addTab(user_interface.tab_plotSourceSpec, "Source Spectrum")
                QtWidgets.qApp.processEvents()

            except Exception as error:
                user_interface.update_outputText(str(error))

        #=======================================================================
        # Propagating
        #=======================================================================

        try:
            # degree of coherence
            if propQuantity==0:
                # source spatial resolution
                ds = sourceRes

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
                    if farfield_list[numPlane]:
                        user_interface.update_outputText("Multiplying by Q functions...")
                        prop_parameters = [Cfrequency,distances_list[numPlane]]

                        if not farfield_list[numPlane]:
                            W_temp = func_qfunction(user_interface,context,queue,W_source,N,ds,prop_parameters,sim_usePyOpenCL,debug)
                        user_interface.update_outputText("Task Completed!")

                    else:
                        W_temp = W_source
                    #_______________________________________________________________

                    #---------------------------------------------------------------
                    # FFTs
                    #---------------------------------------------------------------
                    user_interface.update_outputText("Performing 2D Fourier transforms...")
                    user_interface.update_outputText("___")
                    for i1 in range(0,N):
                        user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
                        for j1 in range(0,N):
                            if count_nonzero(W_temp[i1,j1])==0:
                                pass
                            else:
                                W_temp[i1,j1]=func_fft2d(user_interface,W_temp[i1,j1],FTinverse=False)
                    user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")
                    user_interface.update_outputText("2D Fourier transforms completed!")
                    #_______________________________________________________________


                    #---------------------------------------------------------------
                    # Transposing...
                    #---------------------------------------------------------------
                    user_interface.update_outputText("Transposing matrix...")
                    W_temp=W_temp.transpose(2,3,0,1)
                    user_interface.update_outputText("Transposing completed!")
                    #_______________________________________________________________


                    #---------------------------------------------------------------
                    # FFTs
                    #---------------------------------------------------------------
                    user_interface.update_outputText("Performing second 2D Fourier transforms...")
                    user_interface.update_outputText("___")
                    for i1 in range(0,N):
                        user_interface.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
                        for j1 in range(0,N):
                            if count_nonzero(W_temp[i1,j1])==0:
                                pass
                            else:
                                W_temp[i1,j1]=func_fft2d(user_interface,W_temp[i1,j1],FTinverse=True)
                    user_interface.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")
                    user_interface.update_outputText("2D Fourier transforms completed!")

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
                    user_interface.update_outputText("Multiplying by Q functions...")
                    prop_parameters = [Cfrequency,distances_list[numPlane]]

                    if not farfield_list[numPlane]:
                        W_temp = func_qfunction(user_interface,context,queue,W_temp,N,dx,prop_parameters,sim_usePyOpenCL,debug)
                    user_interface.update_outputText("Task Completed!")
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

                if debug:
                    figure()
                    pcolormesh(W_temp[M,M].real)
                    show()

                user_interface.update_outputText("**Propagation Completed**")

                #---------------------------------------------------------------
                # Plotting
                #---------------------------------------------------------------
                #*** Plotting ***
                # adding <TAB Source Image> to <TAB PLOT>
                user_interface.tabWidget_plots.addTab(user_interface.tab_plotPropImage, "Propagation Image")
                user_interface.canvasPI = Canvas_propImage(user_interface,W_temp,N)
                QtWidgets.qApp.processEvents()


                #*** Plotting ***
                # adding <TAB Source Image> to <TAB PLOT>
                user_interface.tabWidget_plots.addTab(user_interface.tab_plotPropSDC2D, "Propagation 2D SDC")
                user_interface.canvasPropSDC2D = Canvas_propSDC2D(user_interface,W_temp,N)
                QtWidgets.qApp.processEvents()


                try:
                    #*** Plotting ***
                    # adding <TAB Source Image> to <TAB PLOT>
                    user_interface.tabWidget_plots.addTab(user_interface.tab_plotPropSDC, "Propagation SDC")
                    user_interface.canvasPropSDC = Canvas_propSDC(user_interface,W_temp,N)
                    QtWidgets.qApp.processEvents()
                except Exception as error:
                    user_interface.update_outputText(str(error))
                #_______________________________________________________________



        except Exception as error:
            user_interface.update_outputText(str(error))
        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


    return W_temp
