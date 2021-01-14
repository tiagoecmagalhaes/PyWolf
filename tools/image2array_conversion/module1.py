#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Tiago
#
# Created:     23/03/2020
# Copyright:   (c) Tiago 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------


#=============================================================================#
# Import Stuff
#=============================================================================#
from PIL import *
from PIL import Image
from pylab import *
#from pandas import *

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
#_____________________________________________________________________________#

## reading image
imgCal = cv.imread("IA_200_s.bmp")

## transforming image into array
imgCal = np.array(imgCal, dtype=np.uint8)

## transforms image RGB into 1 Color (tones of grey)
grayCal = cv.cvtColor(imgCal,cv.COLOR_BGR2GRAY)

## image size in x,y-axis
Nx=len(grayCal[0])
Ny=len(grayCal)

save("IA_200_s.npy",grayCal)
