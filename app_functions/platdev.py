#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Geral
#
# Created:     23/01/2020
# Copyright:   (c) Geral 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from pyopencl import *


def getPlatformsDevices():

    PLAT_NUM=0
    DEV_NUM=0

    platform_choices = {}               # Dictionary of Platforms
    list_platforms   = get_platforms()  # List of Platforms
    for i in range(0,len(list_platforms)):
        platform_choices[str(list_platforms[i])] = i


    #Devices:
    device_choices = [] # list of Dictionay of Devices
    for i in range(0,len(list_platforms)):
        device_choices.append({})

    for i in range(0,len(list_platforms)):
        list_devices=list_platforms[i].get_devices()
        for j in range(0,len(list_devices)):
            device_choices[i][str(list_devices[j])] = j

    toreturn = [platform_choices,list_platforms, device_choices]
    return toreturn

#print(device_choices)
