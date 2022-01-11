#-------------------------------------------------------------------------------
# Name:        Save & Load functions
# Purpose:     PyWolf
#
# Author:      Tiago E. C. Magalhaes
#
# Licence:     GNU GENERAL PUBLIC LICENSE Version 3
#-------------------------------------------------------------------------------



#===============================================================================
# Importing Packages
#===============================================================================
# NumPy
from numpy import save, load

# OS
import os

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Save Project File <.wolf>
#===============================================================================
def save_project_file2(ui,dirName):
    "Saves project into a <.wolf> file"
    try:
        ui.update_outputText(dirName)
        file = open(dirName,"w")

        # building file
        txt = ui.version+"\n"                                               # 1: Version
        txt+= ui.lineEdit_simName.text()+"\n"                               # 2: Project Name
        txt+= ui.give_time()+"\n"                                           # 3: Date/Time
        txt+= str(ui.checkBox_pyopencl.isChecked())+"\n"                    # 4: Use PyOpenCL
        if ui.list_platforms!=[]:
            txt+= str(ui.list_platforms[ui.comboBox_platform.currentIndex()])+"\n"  # 5: Platform
        else:
            txt+= "None\n"
        try:
            txt+=str(ui.list_platforms[ui.comboBox_platform.currentIndex()].get_devices()[ui.comboBox_device.currentIndex()])+"\n"  # 6: Device
        except:
            txt+="None\n"
        txt+= str(ui.checkBox_save.isChecked()) + "\n"                          # 7: Save Results
        txt+= str(ui.checkBox_saveSourceCSDA.isChecked()) + "\n"                # 8: Save Source CSDA
        txt+= str(ui.checkBox_savePropCSDA.isChecked()) + "\n"                  # 9: Save Prop CSDA
        txt+= str(ui.lineEdit_saveFiles.text()) + "\n"                          # 10: Save Directory
        txt+= str(ui.checkBox_debug.isChecked()) + "\n"                         # 11: Debug
        txt+= ui.lineEdit_N.text()+"\n"                                         # 12: Matrix Size
        txt+= str(ui.checkBox_FFT.isChecked())+ "\n"                            # 13: use FFT zero padding
        txt+= str(ui.lineEdit_NZ.text())  + "\n"                                # 14: zero padding total matrix size
        txt+= str(ui.comboBox_propQuant.currentIndex()) +"\n"                   # 15: Propagation quantity
        txt+= str(ui.comboBox_specPropModels.currentText()) +"\n"               # 16: Model
        txt+= ui.lineEdit_theta.text() + "\n"                                   # 17: Parameters
        if ui.radioButton_1freq.isChecked():
            txt+= ui.radioButton_1freq.text() + "\n" + "None"+"\n"+ ui.lineEdit_centralFreq.text() +"\n"                             # 18: Spectrum Type (ex: 1freq)
        elif not ui.radioButton_1freq.isChecked():
            txt+= ui.radioButton_poly.text() + "\n"                                            # 18: Spectrum Type (ex: Polychromatic)
            txt+= ui.specModel_list[ui.comboBox_specType.currentIndex()][0] +"\n"            # 19: Spectral Model

            txt+= "!"
            for i in range(0,len(ui.specModelPar_list[ui.comboBox_specType.currentIndex()])):
                txt+= str(ui.specModel_lineEditParameters[i].text()) + "\t"                        # 20: Parameters
            txt+= "\n"

        txt+= ui.lineEdit_sourceRes.text() + "\n"                                # 21: Spatial Resolution
        txt+= str(ui.checkBox_geoFromFile.isChecked()) + "\n"                    # 22: Load Geometry (bolean)
        txt+= ui.lineEdit_dirGeoMatrix.text() + "\n"                             # 23: Load Geometry Directory
        txt+= str(ui.checkBox_CSDAFromFile.isChecked()) + "\n"                   # 24: Load Source CSDA (bolean)
        txt+= ui.lineEdit_dirCSDAmatrix.text() + "\n"                            # 25: Load Source CSDA Directory
        txt+= ui.geometry_list[ui.comboBox_geometry.currentIndex()][0] + "\n"    # 26: Geometry Model

        # 27: Geometry Parameters
        txt+= "!"
        for i in range(0,len(ui.geometryPar_list[ui.comboBox_geometry.currentIndex()])):
            txt+= str(ui.geometry_lineEditParameters[i].text()) + "\t"
        txt+= "\n"

        # 28: Coherence Model
        txt+= ui.cohModel_list[ui.comboBox_cohModel.currentIndex()][0] + "\n"

        # 29: Coherence Parameters
        txt+= "!"
        for i in range(0,len(ui.cohModelPar_list[ui.comboBox_cohModel.currentIndex()])):
            txt+= ui.cohModel_lineEditParameters[i].text() + "\t"
        txt+= "\n"

        # 30: Use Custom Spectral Density?
        txt+= str(ui.checkBox_specDen.isChecked()) + "\n"

        # 31: Spectral Density Model
        txt+= ui.specModel_list[ui.comboBox_specDenModel.currentIndex()][0] + "\n"

        # 32: Spectral Density Parameters
        txt+= "!"
        for i in range(0,len(ui.specDenPar_list[ui.comboBox_specDenModel.currentIndex()])):
            txt+= ui.specDen_lineEditParameters[i].text() + "\t"
        txt+= "\n"

        # 33: number of planes
        Np = int(ui.spinBox_numPlanes.text()  )
        txt+= str(Np) + "\n"

         # 34: Distances
        txt+= "!"
        for i in range(0,Np):
            txt+= ui.lineEdit_distances_list[i].text() + "\t"
        txt+= "\n"

        # 35: Far-fields (bolean)
        txt+= "!"
        for i in range(0,Np):
            txt+= str(ui.checkBox_farfied_list[i].isChecked()) + "\t"
        txt+= "\n"

        # 36: Use Pupil (bolean)
        txt+= "!"
        for i in range(0,Np):
            txt+= str(ui.checkBox_pupil_list[i].isChecked()) + "\t"
        txt+= "\n"

        # 37: Pupil Model
        txt+= "!"
        for i in range(0,Np):
            if ui.checkBox_pupil_list[i].isChecked():
                txt+= str(ui.pupilGeomFunc_list[i][int(ui.comboBox_pupilGeom_list[i].currentIndex())][0]) + "\t"
            else:
                txt+= "None"+"\t"
        txt+= "\n"

        # 38: Pupil Parameters
        txt+= "%"
        for i in range(0,Np):
            if ui.checkBox_pupil_list[i].isChecked():
                for j in range(len(ui.pupilGeom_lineEditParameters[i])):
                    txt+= str(ui.pupilGeom_lineEditParameters[i][j].text()) + "\t"
                txt+="&"
            else:
                txt+= "None" + "&"
        txt+="\n"

        # 39: use Optics (bolean)
        txt+= "!"
        for i in range(0,Np):
            txt+= str(ui.checkBox_optics_list[i].isChecked()) + "\t"
        txt+= "\n"

        # 40: Optics model
        txt+= "!"
        for i in range(0,Np):
            if ui.checkBox_optics_list[i].isChecked():
                txt+= str(ui.optDeviceFunc_list[i][int(ui.comboBox_optDeviceFunc_list[i].currentIndex())][0]) + "\t"
            else:
                txt+= "None"+"&"
        txt+= "\n"

        # 41: optical device parameters
        txt+= "%"
        for i in range(0,Np):
            if ui.checkBox_optics_list[i].isChecked():
                for j in range(len(ui.optDevicePars_lineEditParameters[i])):
                    txt+= str(ui.optDevicePars_lineEditParameters[i][j].text()) + "\t"
                txt+="&"
            else:
                txt+= "None" + "\t"
        txt+="\n"

        # 42
        txt+="?"+str(ui.plainTextEdit.toPlainText())
        txt+="\n"

        # writing file
        file.write(txt)
        file.close()
        ui.update_outputText("[Info] Project has been saved in "+dirName)

    except Exception as error:
        pass #ui.update_outputText("[Error] "+str(error))


#-------------------------------------------------------------------------------
#///////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------


#===============================================================================
# Load Project File <.wolf>
#===============================================================================

def load_project_file2(ui,dirProj):
    try:
        # opening File
        new_file = open(dirProj,"r")

        # Reading File
        text = new_file.read()
        Nt   = len(text)

        # checking version
        if text[0:11] != ui.version[0:11]:
            ui.update_outputText(text[0:11])
            ui.update_outputText("[Error] The version of PyWolf of this project is different from the current version.")
            return False
        elif text[0:12] != ui.version[0:12]:
            ui.update_outputText("[Info] This project was made with version "+text[0:12]+ " of PyWolf and the version you are using currently is " + ui.version[0:13] + ". It should still work.")


        #-----------------------------------------------------------------------
        # Loading Parameters
        #-----------------------------------------------------------------------
        one_state = False
        double_state = False

        one_list = []

        sub_list = []
        two_list = []

        ui.final_list = []

        actual  = ""
        count_n = 0
        i       = 12
        while count_n < 41:
            while i<=Nt:
            ##for i in range(12,Nt):
                if text[i]=="!":
                    one_list = []
                    one_state = True

                elif text[i]=="%":
                    sub_list = []
                    two_list = []
                    double_state = True

                elif text[i] == "\t":
                    # case !
                    if one_state == True:
                        one_list.append(actual)
                        actual = ""

                    # case %
                    elif double_state == True:
                        sub_list.append(actual)
                        actual=""

                elif text[i]=="&":
                    two_list.append(sub_list)
                    sub_list = []
                    actual = ""

                elif count_n==41: # text[i]=="?"
                    ui.final_list.append(text[i+1:-1])
                    break

                elif text[i]=="\n":
                    count_n +=1

                    if one_state == True:
                        ui.final_list.append(one_list)
                        one_list  = []
                        one_state = False
                        actual    = ""

                    elif double_state == True:
                        ui.final_list.append(two_list)
                        double_state = False
                        sub_list = []
                        two_list = []
                        actual   = ""

                    else:
                        ui.final_list.append(actual)
                        actual = ""
                else:
                    actual+= text[i]
                i+=1
        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #-----------------------------------------------------------------------
        # Setting Values
        #-----------------------------------------------------------------------
        ## name
        ui.lineEdit_simName.setText(ui.final_list[1])

        ## use PyOpenCL
        if ui.final_list[3] == "True":
            ui.checkBox_pyopencl.setChecked(True)
        else:
            ui.checkBox_pyopencl.setChecked(False)

        ## Platform
        actual = ""
        count = 0
        for i in range(0,len(ui.final_list[4])):
            if ui.final_list[4][i]=="'":
                count+=1
            if count <2:
                actual+=ui.final_list[4][i]
        for i in range(0,ui.comboBox_platform.count()):
            if ui.comboBox_platform.itemText(i)[0:len(actual)] == actual:
                ui.comboBox_platform.setCurrentIndex(i)

        ## Device
        actual = ""
        count = 0
        for i in range(0,len(ui.final_list[5])):
            if ui.final_list[5][i]=="'":
                count+=1
            if count<4:
                actual+=ui.final_list[5][i]
        #ui.update_outputText(actual)
        for i in range(0,ui.comboBox_device.count()):
            if ui.comboBox_device.itemText(i)[0:len(actual)] == actual:
                ui.comboBox_device.setCurrentIndex(i)

        ## Save Results
        if ui.final_list[6] == "True":
            ui.checkBox_save.setChecked(True)
        else:
            ui.checkBox_save.setChecked(False)

        ## Save Source CSDA
        if ui.final_list[7] == "True":
            ui.checkBox_saveSourceCSDA.setChecked(True)
        else:
            ui.checkBox_saveSourceCSDA.setChecked(False)

        ## Save Prop CSDA
        if ui.final_list[8] == "True":
            ui.checkBox_savePropCSDA.setChecked(True)
        else:
            ui.checkBox_savePropCSDA.setChecked(False)

        ## Save Directory
        ui.lineEdit_saveFiles.setText(ui.final_list[9])

        ## Debug
        if ui.final_list[10] == "True":
            ui.checkBox_debug.setChecked(True)
        else:
            ui.checkBox_debug.setChecked(False)

        ## N
        ui.lineEdit_N.setText(ui.final_list[11])

        ## FFT Zero Padding
        if ui.final_list[12] == "True":
            ui.checkBox_FFT.setChecked(True)
        else:
            ui.checkBox_FFT.setChecked(False)

        ## NZ
        if ui.final_list[12] == "True":
            ui.lineEdit_NZ.setText(ui.final_list[13])

        ## Propagation Quantity
        ui.comboBox_propQuant.setCurrentIndex(int(ui.final_list[14]))

        ## Propagation Model
        for i in range(0,ui.comboBox_specPropModels.count()):
            if ui.comboBox_specPropModels.itemText(i) == ui.final_list[15]:
                ui.comboBox_specPropModels.setCurrentIndex(i)

        ## Propagation Model Parameter
        ui.lineEdit_theta.setText(ui.final_list[16])

        ## Spectrum Type
        if ui.radioButton_1freq.text() == ui.final_list[17]:
            ui.radioButton_1freq.setChecked(True)
        elif ui.radioButton_poly.text() == ui.final_list[17]:
            ui.radioButton_poly.setChecked(True)
        elif ui.radioButton_quasi.text() == ui.final_list[17]:
            ui.radioButton_quasi.setChecked(True)

        ## Spectrum Model
        specModel_num = 0
        if ui.final_list[17] != ui.radioButton_1freq.text():
            for i in range(0,ui.comboBox_specPropModels.count()):
                if ui.comboBox_specPropModels.itemText(i) == ui.final_list[18]:
                    ui.comboBox_specPropModels.setCurrentIndex(i)
                    specModel_num = i

        ## Spectrum Parameters
        if not ui.radioButton_1freq.isChecked():
            list_specPars = list(ui.final_list[19])
            for i in range(0,len(ui.specModel_lineEditParameters)):
                ui.specModel_lineEditParameters[i].setText(list_specPars[i])
        else:
            ui.lineEdit_centralFreq.setText(ui.final_list[19])

        ## Source Spatial Resolution
        ui.lineEdit_sourceRes.setText(ui.final_list[20])

        ## Load Source geometry (boolean)
        if ui.final_list[21] == "True":
            ui.checkBox_geoFromFile.setChecked(True)
        else:
            ui.checkBox_geoFromFile.setChecked(False)

        ## Source geometry File directory
        if ui.final_list[21] == "True":
            ui.lineEdit_dirGeoMatrix.setText(ui.final_list[22])

        ## Load CSDA geometry (boolean)
        if ui.final_list[23] == "True":
            ui.checkBox_CSDAFromFile.setChecked(True)
        else:
            ui.checkBox_CSDAFromFile.setChecked(False)

        ## Load Source CSDA
        if ui.final_list[23] == "True":
            ui.lineEdit_dirCSDAmatrix.setText(ui.final_list[24])

        ## Source Geometry Model
        geoModel_num = 0
        for i in range(0,ui.comboBox_geometry.count()):
            if ui.comboBox_geometry.itemText(i) == ui.final_list[25]:
                ui.comboBox_geometry.setCurrentIndex(i)
                geoModel_num = i

        ## Source Geometry Parameters
        list_geoPars = list(ui.final_list[26])
        for i in range(0,len(ui.geometry_lineEditParameters)):
            ui.geometry_lineEditParameters[i].setText(list_geoPars[i])

        ## Coherence Model
        cohModel_num = 0
        for i in range(0,ui.comboBox_cohModel.count()):
            if ui.comboBox_cohModel.itemText(i) == ui.final_list[27]:
                ui.comboBox_cohModel.setCurrentIndex(i)
                cohModel_num = i

        ## Coherence Model Parameters
        list_cohPars = list(ui.final_list[28])
        for i in range(0,len(ui.cohModel_lineEditParameters)):
            ui.cohModel_lineEditParameters[i].setText(list_cohPars[i])

        ## Use Custom Spectral Density
        if ui.final_list[29] == "True":
            ui.checkBox_specDen.setChecked(True)

        ## Spctral Density Model
        specModel_num = 0
        for i in range(0,ui.comboBox_specDenModel.count()):
            if ui.comboBox_specDenModel.itemText(i) == ui.final_list[30]:
                ui.comboBox_specDenModel.setCurrentIndex(i)
                specModel_num = i

        ## Spectral Density Model Parameters
        list_specDenPars = list(ui.final_list[31])
        for i in range(0,len(ui.specDen_lineEditParameters)):
            ui.specDen_lineEditParameters[i].setText(list_specDenPars[i])

        ## Number of propagation planes
        iP =int(ui.final_list[32])
        ui.spinBox_numPlanes.setValue(iP)

        ## for each plane
        list_distances = list(ui.final_list[33])
        list_farfields = list(ui.final_list[34])
        list_usePupil  = list(ui.final_list[35])
        list_useOptics  = list(ui.final_list[38])

        for iP in range(0,iP):

            ## distances
            ui.lineEdit_distances_list[iP].setText(ui.final_list[33][iP])

            ## far-fields
            if list_farfields[iP] == "True":
                ui.checkBox_farfied_list[iP].setChecked(True)
            else:
                ui.checkBox_farfied_list[iP].setChecked(False)

            ## use Pupil
            if list_usePupil[iP] == "True":
                ui.checkBox_pupil_list[iP].setChecked(True)
            else:
                ui.checkBox_pupil_list[iP].setChecked(False)

            ## Pupil Geometry
            pupilModel_list = []
            if list_usePupil[iP] == "True":
                for i in range(0,ui.comboBox_pupilGeom_list[iP].count()):
                    if ui.comboBox_pupilGeom_list[iP].itemText(i) == ui.final_list[36][iP]:
                        ui.comboBox_pupilGeom_list[iP].setCurrentIndex(i)
                        pupilModel_list.append(i)

            ## Pupil Parameters
            if list_usePupil[iP] == "True":
                for i in range(0,len(ui.pupilGeom_lineEditParameters[iP])):
                    ui.pupilGeom_lineEditParameters[iP][i].setText(ui.final_list[37][iP][i])

            ## use Optics
            if list_useOptics[iP] == "True":
                ui.checkBox_optics_list[iP].setChecked(True)
            else:
                ui.checkBox_optics_list[iP].setChecked(False)

            ## Optics Model Model
            opticsModel_list = []
            if list_useOptics[iP] == "True":
                for i in range(0,ui.comboBox_optDeviceFunc_list[iP].count()):
                    if ui.comboBox_optDeviceFunc_list[iP].itemText(i) == ui.final_list[39][iP]:
                        ui.comboBox_optDeviceFunc_list[iP].setCurrentIndex(i)
                        opticsModel_list.append(i)

            ## Optics Model Parameters
            if list_useOptics[iP] == "True":
                for i in range(0,len(ui.optDevicePars_lineEditParameters[iP])):
                    ui.optDevicePars_lineEditParameters[iP][i].setText(ui.final_list[40][iP][i])

        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------

        ## Comments
        ui.plainTextEdit.setPlainText(str(ui.final_list[-1]))

        ui.update_outputText("Project loaded!")

    except Exception as error:
        ui.update_outputText("[Error] "+str(error))

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Save results
#===============================================================================
def save_results_file2(ui,dirName,spec=False):
    try:
        # Source image
        # save(dirName+"\\source_image",ui.CSDA_source.image) # windows only
        save(os.path.join(dirName,"source_image"), ui.CSDA_source.image)
        ui.update_outputText("[Info] Source image saved in "+str(dirName)+"/CSDA_source_image.npy")

        # Propagated image
        #save(dirName+"\\prop_image",ui.CSDA_prop.image) # windows only
        save(os.path.join(dirName,"prop_image"),ui.CSDA_prop.image)
        ui.update_outputText("[Info] Propagation image saved in "+str(dirName)+"/CSDA_prop_image.npy")

        # Source SDC
        #save(dirName+"\\sourceSDC_mag",ui.canvasSourceSDC.propSDC_mag) # windows only
        save(os.path.join(dirName,"sourceSDC_mag"), ui.canvasSourceSDC.propSDC_mag)
        ui.update_outputText("[Info] Source 2D SDC magnitude saved in "+str(dirName)+"/source2dSDC_mag.npy")
        # save(dirName+"\\sourceSDC_phase",ui.canvasSourceSDC.propSDC_phase) # windows only
        save(os.path.join(dirName,"sourceSDC_phase"),ui.canvasSourceSDC.propSDC_phase)
        ui.update_outputText("[Info] Source SDC Phase saved in "+str(dirName)+"/CSDA_source2dSDC_phase.npy")

        # Propagated SDC
        #save(dirName+"\\propSDC_mag",ui.canvasPropSDC.propSDC_mag) # windows only
        save(os.path.join(dirName,"propSDC_mag"), ui.canvasPropSDC.propSDC_mag)
        ui.update_outputText("[Info] Source 2D SDC magnitude saved in "+str(dirName)+"/source2dSDC_mag.npy")
        #save(dirName+"\\sourceSDC_phase",ui.canvasPropSDC.propSDC_phase) # windows only
        save(os.path.join(dirName,"sourceSDC_phase"), ui.canvasPropSDC.propSDC_phase)
        ui.update_outputText("[Info] Source SDC Phase saved in "+str(dirName)+"/CSDA_source2dSDC_phase.npy")

        # Source 2D SDC
        #save(dirName+"\\source2dSDC_mag",ui.canvasSourceSDC2d.SDC2D_mag) # windows only
        save(os.path.join(dirName,"source2dSDC_mag"),ui.canvasSourceSDC2d.SDC2D_mag)
        ui.update_outputText("[Info] Source 2D SDC magnitude saved in "+str(dirName)+"/source2dSDC_mag.npy")
        #save(dirName+"\\source2dSDC_phase",ui.canvasSourceSDC2d.SDC2D_phase) # windows only
        save(os.path.join(dirName,"source2dSDC_phase"),ui.canvasSourceSDC2d.SDC2D_phase)
        ui.update_outputText("[Info] Source 2D SDC Phase saved in "+str(dirName)+"/CSDA_source2dSDC_phase.npy")

        # Propagated 2D SDC
        #save(dirName+"\\prop2dSDC_real",ui.canvasProp2D_SDC.SDC2D_real) # windows only
        save(os.path.join(dirName,"prop2dSDC_real"), ui.canvasProp2D_SDC.SDC2D_real)
        ui.update_outputText("[Info] Propagation 2D SDC real saved in "+str(dirName)+"/CSDA_propSDC2D_real.npy")
        #save(dirName+"\\prop2dSDC_imag",ui.canvasProp2D_SDC.SDC2D_imag) # windows only
        save(os.path.join(dirName,"prop2dSDC_imag"),ui.canvasProp2D_SDC.SDC2D_imag)
        ui.update_outputText("[Info] Propagation 2D SDC imaginary saved in "+str(dirName)+"/CSDA_propSDC2D_imag.npy")
        #save(dirName+"\\prop2dSDC_mag",ui.canvasProp2D_SDC.SDC2D_mag) # windows only
        save(os.path.join(dirName,"prop2dSDC_mag"), ui.canvasProp2D_SDC.SDC2D_mag)
        ui.update_outputText("[Info] Propagation 2D SDC magnitude saved in "+str(dirName)+"/CSDA_propSDC2D_mag.npy")
        #save(dirName+"\\prop2dSDC_phase",ui.canvasProp2D_SDC.SDC2D_phase) # windows only
        save(os.path.join(dirName,"prop2dSDC_phase"), ui.canvasProp2D_SDC.SDC2D_phase)
        ui.update_outputText("[Info] Propagation 2D SDC Phase saved in "+str(dirName)+"/CSDA_propSDC2D_phase.npy")

        # SDC source x-array
        #save(dirName+"\\x_array_source",ui.canvasSourceSDC.b_array) # windows only
        save(os.path.join(dirName,"x_array_source"),ui.canvasSourceSDC.b_array)
        ui.update_outputText("[Info] Propagation x-array saved in "+str(dirName)+"/x_array_source.npy")

        # SDC prop x-array
        #save(dirName+"\\x_array_prop",ui.canvasPropSDC.b_array) # windows only
        save(os.path.join(dirName,"x_array_prop"), ui.canvasPropSDC.b_array)
        ui.update_outputText("[Info] Propagation x-array saved in "+str(dirName)+"\\x_array_prop.npy")

        # SDC Source points
        try:
            #ui.update_outputText(dirName+"/SourceSDCpoints.txt")
            #file1    = open(dirName+"\\SourceSDCpoints.txt","w") # windows only
            file1    = open(os.path.join(dirName,"SourceSDCpoints.txt"),"w") # windows only
            temp_txt = "P_1x: "+str(ui.canvasSourceSDC.P1x)+"\n"+"P_1y: "+str(ui.canvasSourceSDC.P1y)+"\n"+"P_2x: "+str(ui.canvasSourceSDC.P2x)+"\n"
            file1.write(temp_txt)
            file1.close()
            ui.update_outputText("[Info] SDC source points saved in "+str(dirName)+"/SourceSDCpoints.txt")
        except Exception as error:
            ui.update_outputText(str(error))

        # SDC Propagation points
        try:
            #file1    = open(dirName+"\\PropagationSDCpoints.txt","w") # windows only
            file1    = open(os.path.join(dirName,"PropagationSDCpoints.txt"),"w")
            temp_txt = "P_1x: "+str(ui.canvasPropSDC.P1x)+"\n"+"P_1y: "+str(ui.canvasPropSDC.P1y)+"\n"+"P_2x: "+str(ui.canvasPropSDC.P2x)+"\n"
            file1.write(temp_txt)
            file1.close()
            ui.update_outputText("[Info] SDC propagation points saved in "+str(dirName)+"\\PropSDCpoints.txt")
        except Exception as error:
            ui.update_outputText(str(error))

        # SDC 2D Source points
        try:
            #file1    = open(dirName+"\\Source2dSDCpoints.txt","w") # windows only
            file1    = open(os.path.join(dirName,"Source2dSDCpoints.txt"),"w")
            temp_txt = "P_1x: "+str(ui.canvasSourceSDC2d.P1x)+"\n"+"P_1y: "+str(ui.canvasSourceSDC.P1y)
            file1.write(temp_txt)
            file1.close()
            ui.update_outputText("[Info] 2D SDC source points saved in "+str(dirName)+"\\Source2dSDCpoints.txt")
        except Exception as error:
            ui.update_outputText(str(error))

        # SDC 2D Propagation points
        try:
            ##file1    = open(dirName+"\\Prop2dSDCpoints.txt","w") # windows only
            file1    = open(os.path.join(dirName,"Prop2dSDCpoints.txt"),"w")
            temp_txt = "P_1x: "+str(ui.canvasProp2D_SDC.P1x)+"\n"+"P_1y: "+str(ui.canvasProp2D_SDC.P1y)
            file1.write(temp_txt)
            file1.close()
            ui.update_outputText("[Info] 2D SDC propagation points saved in "+str(dirName)+"\\Prop2dSDCpoints.txt")
        except Exception as error:
            ui.update_outputText(str(error))

        # save project file
        ##save_project_file2(ui,dirName+"\\"+str(ui.lineEdit_simName.text()+".wolf")) # windows only
        save_project_file2(ui,os.path.join(dirName,str(ui.lineEdit_simName.text()+".wolf")))

        # saving notes
        with open(os.path.join(dirName,"notes.txt"), 'w') as yourFile:
            yourFile.write(str(ui.plainTextEdit.toPlainText())) ## notes

        # Spectrum
        if spec:

            # Source Spectrum
            ##save(dirName+"\\sourceSpectrum",ui.CSDA_source.spectrum) # windows only
            save(os.path.join(dirName,"sourceSpectrum"), ui.CSDA_source.spectrum)
            ui.update_outputText("[Info] Source Spectrum saved in "+str(dirName)+"/sourceSpectrum.npy")

            # Propagation Spectrum
            ##save(dirName+"\\propSpectrum",ui.CSDA_prop.spectrum) # windows only
            save(os.path.join(dirName,"propSpectrum"), ui.CSDA_prop.spectrum)
            ui.update_outputText("[Info] Propagation Spectrum saved in "+str(dirName)+"/propSpectrum.npy")

            # Angular Frequency Array
            ##save(dirName+"\\omega_array",ui.CSDA_prop.omega_array) # windows only
            save(os.path.join(dirName,"omega_array"), ui.CSDA_prop.omega_array)
            ui.update_outputText("[Info] Angular frequency array saved in "+str(dirName)+"/omega_array.npy")

            # Ciii Array
            ##save(dirName+"\\C4ir",ui.CSDA_prop.Ciiii_real) # windows only
            save(os.path.join(dirName,"C4ir"), ui.CSDA_prop.Ciiii_real)
            ui.update_outputText("[Info]C4ir array saved in "+str(dirName)+"/C4ir.npy")

        # Save log file
        #file_log    = open(dirName+"\\log.txt","w") # windows only
        file_log    = open(os.path.join(dirName,"log.txt"),"w")
        file_log.write(ui.log_txt)
        file_log.close()
        ui.log_txt = "" # empty log

    except Exception as error:
        ui.update_outputText("[Error] "+str(error))

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================