#-------------------------------------------------------------------------------
# Name:        StartSim
# Purpose:     PyWolf function to Start the Simulation of Partially Coherent Light Propagation
#
# Author:      Tiago E. C. Magalhaes
#
# Licence:     GNU GENERAL PUBLIC LICENSE Version 3
#-------------------------------------------------------------------------------


#===============================================================================
# Importing Packages
#===============================================================================
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QInputDialog, QFileDialog, QLabel, QHBoxLayout

# PyOpencl
from pyopencl import *

# sys, os, copy and time
import sys
import os
import copy
##import time

# NumPy
from numpy import count_nonzero
from numpy import sqrt
from numpy import complex64
from numpy import complex
from numpy import load

# Adding directories to import packages
current_dir = os.getcwd()
sys.path.append(current_dir+"\\plot_functions\\")
sys.path.append(current_dir+"\\propagation_functions\\")
sys.path.append(current_dir+"\\class\\")

# PyWolf packages
from windowPlot_image import *
from windowPlot_2DSDC import *
from windowPlot_SDC import *
from windowPlot_sourceSpectrum import *
from windowPlot_propSpectrum import *
from qfunction import *
from qFFT import *
from qFFT import *
from func_propSpec import *
from build_image import *
from class_CSDA import *

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Initial Paramters
#===============================================================================

# PyOpenCL
os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'

# Temporary
W_temp = None

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Initial Paramters
#===============================================================================

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
    toSaveSourceCSDA = all_parameters[0][2][2]
    toSavePropCSDA   = all_parameters[0][2][3]
    save_dir = None
    if toSave:
        save_dir = all_parameters[0][2][1]

    # debug
    debug = all_parameters[0][3][0]

    # matrix size
    N     = int(all_parameters[0][4][0])
    NZ    = int(all_parameters[0][4][2])
    M     = int(N/2)
    useFFTzeroPadding = int(all_parameters[0][4][1])
    FFTpad_list = [useFFTzeroPadding, NZ]
    NS = None
    if useFFTzeroPadding:
        NS = NZ
    else:
        NS = N

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
    GeoFromFile  = all_parameters[3][1][0]
    GeoFileDir   = all_parameters[3][1][1]
    CSDAFromFile = all_parameters[3][1][2]
    CSDAFileDir  = all_parameters[3][1][3]

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

    # use spectral density
    useSpecDen = all_parameters[3][7]

    # Spectral density model chosen
    chosen_specDensityModelName =  all_parameters[3][8][0]
    chosen_specDensityModelFunc =  all_parameters[3][8][1]

    # Spectral density model parameters
    specDensityPars =  all_parameters[3][9]
    #___________________________________________________________________________


    #---------------------------------------------------------------------------
    # Propagation Parameters
    #---------------------------------------------------------------------------

    # Gerneral propagation parameters
    numPlanes               = all_parameters[4][0]  # number of planes
    distances_list          = all_parameters[4][1]  # list of distances
    farfield_list           = all_parameters[4][2]  # far-field lists

    # Pupil
    usePupil                = all_parameters[4][3]
    pupilGeo_list           = all_parameters[4][4]
    pupilGeoPars_list       = all_parameters[4][5]
    pupilGeoFuncs           = [all_parameters[4][4][i][3] for i in range(0,len(all_parameters[4][4]))]

    # Optics
    useOptics                 = all_parameters[4][6]
    optDevices_list           = all_parameters[4][7]
    optDevicePars_list        = all_parameters[4][8]
    optDeviceFuncs            = [all_parameters[4][7][i][3] for i in range(0,len(all_parameters[4][7]))]
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
        ui.update_outputText(out_txt)

        out_txt = "Device Chosen: "+str(device)
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
        ui.CSDA_source    = CSDA(all_parameters,ui,True)

        # -- IF CSDA FROM FILE --
        if CSDAFromFile:
            ui.update_outputText("Loading the CSDA from file. Please wait...")
            ui.CSDA_source.matrix=load(CSDAFileDir) # matrix
            ui.update_outputText("Loading completed!")

            # testing matrix size
            N_temp = len(ui.CSDA_source.matrix)
            if N_temp != N:
                N = N_temp
                all_parameters[0][4][0] = N_temp
                ui.CSDA_source. N = N_temp
                ui.update_outputText("Matrix size was changed to N = "+str(N)+" so that it fits the uploaded CSDA.")


        #=======================================================================
        # CSDA NOT FROM FILE
        #=======================================================================
        else:

            #*******************************************************************
            # IF IMAGE FROM FILE
            #*******************************************************************
            if GeoFromFile:
                ui.update_outputText("Loading source geometry. Please wait...")


                # image matrix
                if GeoFileDir[-4:]==".npy":
                    image_matrix = load(GeoFileDir)


                elif GeoFileDir[-4:]==".bmp" or GeoFileDir[-4:]==".jpg" or GeoFileDir[-4:]==".png":
                    ##from PIL import Image

                    import cv2 as cv

                    ## reading image
                    imgCal = cv.imread(GeoFileDir)

                    ## transforming image into array
                    imgCal = array(imgCal, dtype=uint8)

                    ## transforms image RGB into 1 Color (tones of grey)
                    image_matrix = cv.cvtColor(imgCal,cv.COLOR_BGR2GRAY)


                # testing matrix size
                N_temp = len(image_matrix)
                if N_temp != N:
                    N = N_temp
                    all_parameters[0][4][0] = N_temp
                    ui.CSDA_source.N = N_temp
                    ui.update_outputText("Matrix size was changed to N = "+str(N)+" so that it fits the uploaded image array.")
                ## creating Temporary 4D matrix
                W_temp = ones((N,N,N,N)).astype(complex64)


                ui.update_outputText("Source geometry loaded with size "+str(len(image_matrix))+" x "+str(len(image_matrix[0]))+" .")

                # building image
                ui.CSDA_source.matrix = buildCSDAimage(ui,context,queue,W_temp,N,image_matrix,sim_usePyOpenCL,debug)
                ui.update_outputText("Source geometry completed!")
            #___________________________________________________________________


            #*******************************************************************
            # IF IMAGE FROM FILE
            #*******************************************************************
            else:
                # creating Temporary 4D matrix
                W_temp = zeros((N,N,N,N)).astype(complex64)

                ui.update_outputText("The source geometry is being created. Please wait...")
                # updating text

                try:
                    ui.CSDA_source.matrix = ui.geometryModelsFunc[chosen_geometry](ui,context,queue,W_temp,N,geomPars,sim_usePyOpenCL,debug)
                except Exception as error:
                    ui.update_outputText("[Error] "+str(error))

                if debug:
                    figure()
                    title("W_source - Geometry - real values")
                    pcolormesh(ui.CSDA_source.matrix[M,M].real)
                    show()

                #geomFunc(ui,context,queue,W_temp,N,geomPars,sim_usePyOpenCL,debug)
                #print(W_temp[M,M,M].real)

                # updating text
                ui.update_outputText("The Source geometry of the cross-spectral density matrix has been created!")
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Creating Source Coherence Model
        #=======================================================================
        if not CSDAFromFile:
            try:
                if not CSDAFromFile:
                    ui.update_outputText("The Source coherence model will now be constructed...")
                    ##ui.update_outputText(str(cohPars))
                    ui.CSDA_source.matrix = chosen_cohModelFunc.cohModelFunc(ui,context,queue,ui.CSDA_source.matrix,N,cohPars,sim_usePyOpenCL,debug)


                    #ui.CSDA_source.matrix = W_temp

                    if debug:
                        figure()
                        title("W_source - CSDA - real values")
                        plot(sqrt(ui.CSDA_source.matrix[M,M,M].real**2+ui.CSDA_source.matrix[M,M,M].imag**2),marker="o")
                        grid()
                        show()

                    ui.update_outputText("The cross-spectral density of the source has been completed!")

            except Exception as error:
                ui.update_outputText(str(error)+" in <startSim>: creating source coherence model.")

        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # Creating Source Spectral Density Model
        #=======================================================================
        if not CSDAFromFile:
            try:
                if not CSDAFromFile:
                    if useSpecDen:
                        ui.update_outputText("The spectral density model will now be constructed: "+str(chosen_specDensityModelName))
                        ui.CSDA_source.matrix = chosen_specDensityModelFunc.specDenModelFunc(ui,context,queue,ui.CSDA_source.matrix,N,specDensityPars,sim_usePyOpenCL,debug)

                        #ui.CSDA_source.matrix = W_temp

                        if debug:
                            figure()
                            title("W_source - after spectral density")
                            plot(sqrt(ui.CSDA_source.matrix[M,M,M].real**2+ui.CSDA_source.matrix[M,M,M].imag**2),marker="o")
                            grid()
                            show()

                        ui.update_outputText("Spectral density of the source completed!")
                    else:
                        ui.update_outputText("Custom Spectral density model not selected.")

            except Exception as error:
                ui.update_outputText(str(error)+" in <startSim>: creating source spectral density model.")
        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # Creating Source Image
        #=======================================================================
        try:
            # creating image source
            ui.CSDA_source.image = zeros((N,N))
            for i in range(0,N):
                for j in range(0,N):
                    ui.CSDA_source.image[i,j] = ui.CSDA_source.matrix[i,j,i,j].real
        except Exception as error:
            ui.update_outputText(str(error)+" in <startSim>: creating source image.")
        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # Plot source functions
        #=======================================================================
        try:
            ui.update_outputText("Plotting Graphs...")
            # adding <TAB Source Image> to <TAB PLOT>
            ui.canvasSI = Canvas_Image(ui,ui.CSDA_source.image,N,sourceRes,title="Source Image")
            ui.tabWidget_plots.addTab(ui.list_of_tabs[-1], "Source Image")
            #QtWidgets.qApp.processEvents()

            # adding <TAB Source Image> to <TAB PLOT>
            ui.canvasSourceSDC2d = Canvas_2DSDC(ui,ui.CSDA_source.matrix,N,sourceRes,title = "Source 2D SDC")
            ui.tabWidget_plots.addTab(ui.list_of_tabs[-1], "Source 2D SDC")
            #QtWidgets.qApp.processEvents()

            # adding source SDC tab with plot
            ui.canvasSourceSDC = Canvas_SDC(ui,ui.CSDA_source.matrix,N,sourceRes, title = "Source SDC")
            ui.tabWidget_plots.addTab(ui.list_of_tabs[-1], "Source SDC")
            ui.update_outputText("Completed!")

        except Exception as error:
            ui.update_outputText(str(error)+" in <startSim>: plotting source functions.")

        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # Plotting Source Spectrum
        #=======================================================================
        if polychromatic:
            if True:
                try:
                    #*** Plotting ***
                    # adding <TAB Source Image> to <TAB PLOT>
                    ui.canvasSourceSpec = Canvas_sourceSpec(ui,ui.CSDA_source,N)
                    ui.tabWidget_plots.addTab(ui.list_of_tabs[-1], "Source Spectrum")
                    QtWidgets.qApp.processEvents()
                    ui.source_spec_plot = True

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
            ui.CSDA_prop    = CSDA(all_parameters,ui)
            import copy
            ui.CSDA_prop.matrix = copy.copy(ui.CSDA_source.matrix)

            # speed of light
            c = 2.99792458e8

            # source spatial resolution
            ds = ui.CSDA_source.ds



            # first plane spatial resolution
            dx = None
            if useFFTzeroPadding:
                ui.update_outputText("FFT zero padding will be used.")
                dx = 2*pi*3e8*distances_list[0]/(Cfrequency*NZ*sourceRes)
                ui.update_outputText("Spatial Resolution in Plane 1 (m): "+str(dx))
            else:
                ui.update_outputText("FFT zero padding will NOT be used.")
                dx = 2*pi*3e8*distances_list[0]/(Cfrequency*N*sourceRes)
                ui.update_outputText("Spatial Resolution in Plane 1 (m): "+str(dx))


            #===================================================================
            # PROPAGATION
            #===================================================================
            for numPlane in range(0,numPlanes):

                ui.update_outputText("Propagation for Plane "+str(numPlane+1)+" initiating...")

                #---------------------------------------------------------------
                # spatial resolution
                #---------------------------------------------------------------
                if numPlane == 0:
                    pass
                else:
                    ds = dx
                    if useFFTzeroPadding:
                        dx = 2*pi*3e8*distances_list[numPlane]/(Cfrequency*NZ*dx)
                        ui.update_outputText("Plane "+str(numPlane+1)+" spatial resolution: "+str(dx))
                    else:
                        dx = 2*pi*3e8*distances_list[numPlane]/(Cfrequency*N*dx)
                        ui.update_outputText("Plane "+str(numPlane+1)+" spatial resolution: "+str(dx))

                C1 = Cfrequency/(2*distances_list[numPlane]*c)
                #_______________________________________________________________


                #---------------------------------------------------------------
                # Q functions
                #---------------------------------------------------------------
                # gathering parameters
                prop_parameters = [C1]

                if not farfield_list[numPlane]:
                    ui.update_outputText("Multiplying by Q functions...")


                    # q function
                    ui.CSDA_prop.matrix = func_qfunction(ui,context,queue,ui.CSDA_prop.matrix,N,ds,prop_parameters,sim_usePyOpenCL,debug)

                    # messages
                    ui.update_outputText("Task Completed!")
                else:
                    ui.update_outputText("Far-field approximation used. No need to multiply by the q function.")

                #_______________________________________________________________


                #---------------------------------------------------------------
                # 1st FFTs
                #---------------------------------------------------------------
                ui.update_outputText("Performing 1st 2D Fourier transforms...")
                ui.update_outputText("___")
                for i1 in range(0,N):
                    ui.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
                    for j1 in range(0,N):
                        if count_nonzero(ui.CSDA_prop.matrix[i1,j1].real)==0:
                            pass
                        else:
                            ui.CSDA_prop.matrix[i1,j1] = func_fft2d(ui,ui.CSDA_prop.matrix[i1,j1],False,FFTpad_list)
                ui.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")
                ui.update_outputText("2D Fourier transforms completed!")
                #_______________________________________________________________


                #---------------------------------------------------------------
                # Transposing...
                #---------------------------------------------------------------
                ui.update_outputText("Transposing matrix...")
                ui.CSDA_prop.matrix = ui.CSDA_prop.matrix.transpose(2,3,0,1)
                ui.update_outputText("Transposing completed!")
                #_______________________________________________________________


                #---------------------------------------------------------------
                # 2nd FFTs
                #---------------------------------------------------------------

                ui.update_outputText("Performing 2nd 2D Fourier transforms...")
                ui.update_outputText("___")
                for i1 in range(0,N):
                    ui.update_outputTextSameLine(str(round(i1*100./N,1))+"% concluded ("+str(i1)+"/"+str(N-1)+").")
                    for j1 in range(0,N):
                        if count_nonzero(ui.CSDA_prop.matrix[i1,j1])==0:
                            pass
                        else:
                            ui.CSDA_prop.matrix[i1,j1]=func_fft2d(ui,ui.CSDA_prop.matrix[i1,j1],True,FFTpad_list)
                ui.update_outputTextSameLine("\r"+str(round(100.0,1))+"% concluded")
                ui.update_outputText("2D Fourier transforms completed!")

                if debug:
                    figure()
                    title("CSDA - after 2D FFT ")
                    plot(sqrt(ui.CSDA_prop.matrix[M,M,M].real**2+ui.CSDA_prop.matrix[M,M,M].imag**2),marker="o")
                    grid()
                    show()
                #_______________________________________________________________


                #---------------------------------------------------------------
                # Transposing...
                #---------------------------------------------------------------
                if propQuantity==0:
                    ui.update_outputText("Transposing matrix...")
                    ui.CSDA_prop.matrix = ui.CSDA_prop.matrix.transpose(2,3,0,1)
                    ui.update_outputText("Transposing completed!")

                #_______________________________________________________________


                #---------------------------------------------------------------
                # Q functions and Optics function
                #---------------------------------------------------------------
                ui.update_outputText("Multiplying by Q functions...")

                # q function
                ui.CSDA_prop.matrix = func_qfunction(ui,context,queue,ui.CSDA_prop.matrix,N,dx,prop_parameters,sim_usePyOpenCL,debug)

                ui.update_outputText("Task Completed!")
                #_______________________________________________________________


                #---------------------------------------------------------------
                # Pupil Function
                #---------------------------------------------------------------
                if usePupil[numPlane]:
                    ui.update_outputText("Applying pupil function...")
                    ui.CSDA_prop.matrix = pupilGeoFuncs[numPlane](ui,context,queue,ui.CSDA_prop.matrix,N,pupilGeoPars_list[numPlane],sim_usePyOpenCL,debug)
                    ui.update_outputText("Pupil function completed!")
                #_______________________________________________________________


                #---------------------------------------------------------------
                # Optical Device Function
                #---------------------------------------------------------------
                if useOptics[numPlane]:
                    ui.update_outputText("Applying optical device function...")
                    ui.CSDA_prop.matrix = optDeviceFuncs[numPlane](ui,context,queue,ui.CSDA_prop.matrix,N,dx,Cfrequency,optDevicePars_list[numPlane],sim_usePyOpenCL,debug)
                    ui.update_outputText("Optical device function completed!")
                #_______________________________________________________________


                ui.update_outputText("Propagation for Plane "+str(numPlane+1)+" completed!")
            #===================================================================
            #//////////////////////////////////////////////////////////////////
            #===================================================================


            #=======================================================================
            # Creating Propagation Image
            #=======================================================================
            # creating image source
            ui.CSDA_prop.image = zeros((N,N))
            for i in range(0,N):
                for j in range(0,N):
                    ui.CSDA_prop.image[i,j] = ui.CSDA_prop.matrix[i,j,i,j].real
            #-----------------------------------------------------------------------
            #///////////////////////////////////////////////////////////////////////
            #-----------------------------------------------------------------------


            if debug:
                figure()
                pcolormesh(W_temp[M,M].real)
                show()

            # output message text
            ui.update_outputText("**Propagation Completed**")

            # Simulation Completed
            ui.sim = True

            # Deleting Temporary Matrix
            W_temp = None
            del W_temp

            #=======================================================================
            # Degree of Coherence and Intensity Propagation
            #=======================================================================
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

                    ui.canvasPI = Canvas_Image(ui,ui.CSDA_prop.image,N,ui.dx_list[-1],title="Propagation Image")
                    ui.tabWidget_plots.addTab(ui.list_of_tabs[-1], "Propagation Image")
                    #QtWidgets.qApp.processEvents()

                    #--- Plotting Propagation 2D SDC  ----
                    # adding <TAB Source Image> to <TAB PLOT>
                    ui.canvasProp2D_SDC = Canvas_2DSDC(ui,ui.CSDA_prop.matrix,N,ui.dx_list[-1],title="Propagation 2D SDC")
                    ui.tabWidget_plots.addTab(ui.list_of_tabs[-1], "Propagation 2D SDC")
                    #QtWidgets.qApp.processEvents()

                    #--- Plotting Propagation SDC---
                    # adding <TAB Source Image> to <TAB PLOT>
                    ui.canvasPropSDC = Canvas_SDC(ui,ui.CSDA_prop.matrix,N,ui.dx_list[-1], title = "Propagation SDC")
                    ui.tabWidget_plots.addTab(ui.list_of_tabs[-1], "Propagation SDC")
                    #QtWidgets.qApp.processEvents()

                except Exception as error:
                    ui.update_outputText(str(error))
                #-----------------------------------------------------------------------
                #///////////////////////////////////////////////////////////////////////
                #-----------------------------------------------------------------------


            #=======================================================================
            # Spectrum Propagation
            #=======================================================================
            elif propQuantity==1:
                try:
                    ui.update_outputText("Building Propagation Spectrum...")
                    PropSpecRes = propagation_spectrum(ui,N,debug)
                    ui.update_outputText("Propagation Spectrum completed!")

                    ## Plotting
                    if polychromatic:
                            #*** Plotting ***
                            # adding <TAB Source Image> to <TAB PLOT>
                            ui.canvaspropSpec = Canvas_propSpec(ui,ui.CSDA_prop,ui.CSDA_source,N)
                            ui.tabWidget_plots.addTab(ui.list_of_tabs[-1], "Propagation Spectrum")
                            QtWidgets.qApp.processEvents()

                            #--- Plotting Propagation Image ---
                            # adding <TAB Source Image> to <TAB PLOT>
                            ui.canvasPI = Canvas_Image(ui,ui.CSDA_prop.image,N,ui.dx_list[-1],title="Propagation Image")
                            ui.tabWidget_plots.addTab(ui.list_of_tabs[-1], "Propagation Image")
                            #QtWidgets.qApp.processEvents()

                            #--- Plotting Propagation 2D SDC  ----
                            # adding <TAB Source Image> to <TAB PLOT>
                            ui.canvasProp2D_SDC = Canvas_2DSDC(ui,ui.CSDA_prop.matrix,N,ui.dx_list[-1],title="Propagation 2D SDC")
                            ui.tabWidget_plots.addTab(ui.list_of_tabs[-1], "Propagation 2D SDC")
                            #QtWidgets.qApp.processEvents()

                            #--- Plotting Propagation SDC---
                            # adding <TAB Source Image> to <TAB PLOT>
                            ui.canvasPropSDC = Canvas_SDC(ui,ui.CSDA_prop.matrix,N,ui.dx_list[-1], title = "Propagation SDC")
                            ui.tabWidget_plots.addTab(ui.list_of_tabs[-1], "Propagation SDC")
                            #QtWidgets.qApp.processEvents()

                except Exception as error:
                    ui.update_outputText(str(error))
            #-----------------------------------------------------------------------
            #///////////////////////////////////////////////////////////////////////
            #-----------------------------------------------------------------------


            #=======================================================================
            # Saving Things
            #=======================================================================
            try:
                if toSave:

                    ## creating folder
                    import os
                    time_now=datetime.datetime.now()
                    minutes=None
                    if int(time_now.minute)<10:
                        minutes="0"+str(time_now.minute)
                    else:
                        minutes=str(time_now.minute)

                    directory_txt=save_dir#+"\\results__"+str(time_now.day)+"-"+str(time_now.month)+"-"+str(time_now.year)+\
                        #"__"+str(time_now.hour)+"h"+minutes
                    os.makedirs(directory_txt)

                    ui.save_results_file(directory_txt,propQuantity)

                    """
                    with open(directory_txt+"\\notes.txt", 'w') as yourFile:
                        yourFile.write(str(ui.plainTextEdit.toPlainText())) ## notes
                        save(directory_txt+"\\CSDA_prop_image",ui.CSDA_prop.image)
                        save(directory_txt+"\\CSDA_source_image",ui.CSDA_source.image)
                        save(directory_txt+"\\CSDA_source_image",ui.CSDA_source.image)
                        ui.save_project_file(directory_txt)
                    """

                ## saving CSDA source
                if toSaveSourceCSDA:
                    save(directory_txt+"\\CSDA_source", ui.CSDA_source.matrix)

                ## saving CSDA prop
                if toSavePropCSDA:
                    save(directory_txt+"\\CSDA_prop", ui.CSDA_prop.matrix)

            except Exception as error:
                ui.update_outputText("[Error] "+str(error)+" at <startSim> in saving results.")
            #-----------------------------------------------------------------------
            #///////////////////////////////////////////////////////////////////////
            #-----------------------------------------------------------------------

        except Exception as error:
            ui.update_outputText("[Error] "+str(error)+" at <startSim> in Propagation.")
    else:
        ui.update_outputText("No propagation algorithm is configured for these conditions.")

    return True
#-------------------------------------------------------------------------------
#///////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------