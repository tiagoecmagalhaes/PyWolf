# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Name:        MainSim
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
##
##============================================================================
##############################################################################
# IMPORTING PACKAGES
##############################################################################
##============================================================================
from pyopencl import *
from Objects import *
from Plots import *

##_____________________________________________________________________________
##
##
def main(all_parameters):
    #platform,device,N,NW,distance,radiusPixels,cohState,cohModel,cohPar1,specModel,specPar1,specPar2,specPar3,specPar4):

    #==========================================================================
    # Defining Parameters
    #==========================================================================

    # Options
    savePar=all_parameters[9]
    ParVar=all_parameters[15]
    debug=all_parameters[18]
    FarField=all_parameters[19]

    # PyOpenCL
    platform_num=all_parameters[0]
    device_num=all_parameters[1]
    platform_name=all_parameters[16]
    device_name=all_parameters[17]

    # Simulation
    N=all_parameters[2]

    # Source
    sourceResolution=all_parameters[14]

    geometry=all_parameters[3]
    geomPar1=all_parameters[5]
    geomPar2=all_parameters[11]

    # Coherence
    cohState=all_parameters[6]
    cohModel=all_parameters[7]
    cohPar1=all_parameters[8]
    cohPar2=all_parameters[12]
    cohPar3=all_parameters[13]
    cohPar4=all_parameters[28]

    # Optical System
    optical_system=all_parameters[25]
    print("\n\n\n"+"optical_system:"+str(optical_system)+"\n\n\n")
    distance1=all_parameters[26]
    distance2=all_parameters[27]
    focal_length=all_parameters[30]
    pupilFunc=all_parameters[31]
    pupilPar1=all_parameters[32]
    pupilPar2=all_parameters[33]

    # Output Quantities:
    theta=None
    outQ=all_parameters[20]
    outQ_par1=None
    outQ_par2=None
    outQ_par3=None

    # Degree of Coherence:
    if outQ==0:
        outQ_par1=all_parameters[21]
        theta=None

    # Spectrum
    elif outQ==1:
        outQ_par1=all_parameters[21] # Spectrum Model
        theta=all_parameters[22]
        outQ_par2=all_parameters[23] # Spectrum Par1
        outQ_par3=all_parameters[24] # Spectrum Par2

    #__________________________________________________________________________


    # Context
    list_platforms=get_platforms()
    platform=list_platforms[platform_num]
    device=platform.get_devices()[device_num]
    context=Context(devices=[device])

    print("Platform Chosen: "+str(list_platforms[platform_num])+"\n")
    print("Device Chosen: "+str(device)+"\n")

    # Defining Queue
    queue=CommandQueue(context,device=device)

    ## Coherence Parameters ##
    cohState_choices=["incoh","File","p_coh"]
    cohModel_choices=["gaussian-beam","lambertian","gaussianBeam-voronoi","QH_gaussian","Lorentzian","Dirac Gaussian Schell","NU Gaussian","Young"]
    if cohModel!=None:
        coh_parameters=[cohState_choices[cohState],cohModel_choices[cohModel],cohPar1,cohPar2,cohPar3,cohPar4]
    else:
        coh_parameters=[cohState_choices[cohState],None,cohPar1,cohPar2,cohPar3,cohPar4]

    ## Source Parameters ##
    source_parameters=[distance1,sourceResolution,geometry,geomPar1,geomPar2]

    ## Platform Parameters ##
    opencl_parameters=[platform_name,device_name]

    ## Spec Parameters ##
    spec_parameters=[outQ,outQ_par1,outQ_par2,outQ_par3]

    ## Propagation Parameters ##
    prop_parameters=[optical_system,[distance1,distance2,focal_length],theta,[pupilFunc,pupilPar1,pupilPar2]]

    if outQ==0:
        print("---Coherence Parameters---")
        print(coh_parameters)
        print('----- " -----')

        global W_gauss
        W_gauss=W_Mono(context,queue,coh_parameters,spec_parameters,
                       source_parameters,prop_parameters,opencl_parameters,N,outQ,"test",
                       savePar)

        W_gauss.propagate_miu(prop_function2,savePar,parallel=ParVar,B_FarField=FarField,debug=debug)

        plot_miu(W_gauss,savePar)
        plot_miu_source(W_gauss,savePar)
        plot_image_source(W_gauss,savePar)
        plot_image_prop(W_gauss,savePar)
        show()

        print("All has been saved!")
        return W_gauss

    elif outQ==1:
        global W_gauss
        W_gauss=W_Mono(context,queue,coh_parameters,spec_parameters,
                       source_parameters,prop_parameters,opencl_parameters,N,outQ,"test",
                       savePar)

        W_gauss.propagate_miu(prop_function2,savePar,parallel=ParVar,B_FarField=FarField,debug=debug)
        plot_miu_source(W_gauss,savePar)
        plot_image_source(W_gauss,savePar)
        plot_image_prop(W_gauss,savePar)
        plot_miu(W_gauss,savePar)
        show()

        return W_gauss


if __name__ == '__main__':
    main(all_parameters)



