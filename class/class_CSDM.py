#-------------------------------------------------------------------------------
# Name:        Class CDSA
# Purpose:     PyWolf
#
# Author:      Tiago E. C. Magalhaes
#
# Created:     28/02/2020
# Copyright:   (c) Geral 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from numpy import sqrt
from numpy import pi
from numpy import array


class CSDM:

    def __init__(self,all_parameters,ui,source=True):
        #-----------------------------------------------------------------------
        # Source Parameters
        #-----------------------------------------------------------------------

        # saving info
        self.all_paramters = all_parameters
        self.ui = ui

        #source_list = [source_res,file_list,chosen_geometry,geoModel_list,geoPars_list,cohModel_list,cohPars_list]
        self.N  = int(all_parameters[0][4][0])
        self.useZeroPadd = int(all_parameters[0][4][1])
        self.Nz  = int(all_parameters[0][4][2])
        self.ds = all_parameters[3][0]
        self.NS = None
        if self.useZeroPadd:
            self.NS = self.Nz
        else:
            self.NS = self.N

        # main matrix
        self.matrix = None

        # source from file
        self.sourceFromFile = all_parameters[3][1][0]
        self.sourceFileDir  = all_parameters[3][1][1]

        # geometry function
        self.geometry = all_parameters[3][2]

        # geometry parameters
        self.geomPars = all_parameters[3][4]

        # coherence model chosen
        self.cohModelName =  all_parameters[3][5][0]
        self.cohModelFunc =  all_parameters[3][5][1]

        # coherence model parameters
        self.cohPars =  all_parameters[3][6]

        # other
        self.Ciiii_real  = None
        self.Ciiii_imag  = None
        #_______________________________________________________________________


        #-----------------------------------------------------------------------
        # Spectrum Parameters
        #-----------------------------------------------------------------------
        checkFreq_list     = all_parameters[2][0]
        monochromatic      = checkFreq_list[0]
        quasimonochromatic = checkFreq_list[1]
        polychromatic      = checkFreq_list[2]

        if monochromatic:
            self.Cfrequency = all_parameters[2][1][0]

        if polychromatic or quasimonochromatic:

            self.theta            = float(all_parameters[1][2])
            self.chosen_specModel = all_parameters[2][2][0]
            self.specModelName    = all_parameters[2][2][1]
            self.specModelDir     = all_parameters[2][2][2]
            self.specModelFunc    = all_parameters[2][2][3]
            self.specModelPars    = all_parameters[2][3]

            self.Nw = int(self.N/2)

            # create angular frequency array
            if source:
                self.create_source_spectrum()
                ui.update_outputText("Source Spectrum has been created.")

        #self.sourceGeomModel = all_parameters[2]
        #_______________________________________________________________________

    def create_source_spectrum(self):
        res = self.specModelFunc(self.ui,self.N,self.specModelPars,self.ds,self)
        self.omega_array = res[0]
        self.spectrum    = res[1]

    def export_CSDM(self):
        pass







