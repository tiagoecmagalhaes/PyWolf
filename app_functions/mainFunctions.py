#-------------------------------------------------------------------------------
# Name:        Main Functions
# Purpose:     PyWolf functions
#
# Author:      TEC MAGALHAES
#
# Licence:     GNU GENERAL PUBLIC LICENSE Version 3
#-------------------------------------------------------------------------------


#===============================================================================
# Importing Packages
#===============================================================================

# PyQT5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QInputDialog, QFileDialog, QLabel, QHBoxLayout

# PyOpenCL, os, psutil, glob
import pyopencl
import os
import psutil
import glob

# NumPy, functools, decimal
import numpy, functools
from decimal import Decimal

# Time
##from datetime import datetime

# PyWolf packages
from windowPlot_image  import *
from palettes import *
from fonts import *
from color import *
from platdev import *
from testPars import *
from startSim import *

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#-------------------------------------------------------------------------------
def update_devices2(ui):
    "Updates OpenCL devices"
    # -- Platform and Device Combo Boxes --#
    global current_platform
    current_platform = ui.comboBox_platform.currentIndex()
    ui.comboBox_device.clear()
    for k in ui.device_choices[current_platform].items():
        ui.comboBox_device.addItem(k[0],ui.device_choices[current_platform][k[0]])

    if ui.comboBox_device.count()==0:
        new="\n[info] There is currently no device for that selected platform."
        ui.textBrowser.append(str(new))
        ui.textBrowser.update()
#_______________________________________________________________________________


#-------------------------------------------------------------------------------
def update_outputText2(ui,text):
    "Updates the Output Message box in the application"
    ui.textBrowser.append("\n"+ui.give_time()+"  | >> "+str(text))
    ui.textBrowser.update()
    ui.textBrowser.moveCursor(QtGui.QTextCursor.End)
    QtWidgets.qApp.processEvents()
#_______________________________________________________________________________


#-------------------------------------------------------------------------------
def update_outputTextSameLine2(ui,text):
    "Updates the Output Message box in the application in the same previous line"
    cursor = ui.textBrowser.textCursor()
    cursor.movePosition(QtGui.QTextCursor.End)
    cursor.select(QtGui.QTextCursor.LineUnderCursor)
    cursor.removeSelectedText()
    cursor.movePosition(QtGui.QTextCursor.StartOfLine)
    cursor.insertText(str(text))
    QtWidgets.qApp.processEvents()
#_______________________________________________________________________________


#-------------------------------------------------------------------------------
def give_time2(ui):
    "returns the currente date and time"
    ui.nowTime = datetime.now()
    day_time = ui.nowTime.strftime("%d/%m/%Y %H:%M:%S")
    new_txt = "["+str(day_time)+"]"
    return new_txt
#_______________________________________________________________________________


#-------------------------------------------------------------------------------
def show_citation2(ui):
    mydialog = QDialog()
    mydialog.setModal(True)
    mydialog.exec()
#_______________________________________________________________________________


#-------------------------------------------------------------------------------
def openFileNameDialog_saveDir2(ui):
    "choose save directory"
    download_path = ui.lineEdit_saveFiles.text()
    #options = QFileDialog.Options()
    #options |= QFileDialog.DontUseNativeDialog
    filename = None
    try:
        ui.dirName = QFileDialog.getExistingDirectory(None,"Save Directory",download_path) # ,,options=options
        ui.lineEdit_saveFiles.clear()
        ui.lineEdit_saveFiles.setText(ui.dirName)
    except:
        update_outputText("Something went wrong when choosing saving directory.")
#_______________________________________________________________________________


#-------------------------------------------------------------------------------
def openFileNameDialog_openGeo2(ui):
    "choose save directory"
    geo_path = ui.lineEdit_saveFiles.text()
    #options = QFileDialog.Options()
    #options |= QFileDialog.DontUseNativeDialog
    filename = None
    try:
        geo_path = QFileDialog.getOpenFileName(None,"Open Numpy Array File",ui.current_dir+"\\source_images", "NPY Files (*.NPY *.jpg *.bmp *.png)")
        ui.dirSourceGeo = geo_path[0]
        ui.lineEdit_dirGeoMatrix.setText(str(ui.dirSourceGeo))
    except:
        update_outputText("Something went wrong when choosing saving directory.")
#_______________________________________________________________________________


#-------------------------------------------------------------------------------
def openFileNameDialog_openCSDA2(ui):
    "Open Numpy Array File"
    CSDA_path = ui.lineEdit_saveFiles.text()
    filename = None
    try:
        CSDA_path = QFileDialog.getOpenFileName(None,"Open Numpy Array File","", "NPY Files (*.NPY)") # ,,options=options
        ui.dirSourceCSDA = CSDA_path[0]
        ui.lineEdit_dirCSDAmatrix.setText(str(ui.dirSourceCSDA))

    except:
        update_outputText("Something went wrong when choosing saving directory.")
#_______________________________________________________________________________


#-------------------------------------------------------------------------------
def showRAM2(ui):
    "Shows the ammount of RAM in the output Message Box"
    ram_info  = psutil.virtual_memory()
    total_ram = ram_info[0]
    avail_ram = ram_info[1]
    perc_ram  = ram_info[2]
    #new_txt=ui.bar+"\n RAM info\n"+ui.bar+"\n Total Ram: "+str(round(float(total_ram)/1073741824.0,1))+" GB\n Available Ram: "+str(round(float(avail_ram)/1073741824.0,1))+" GB ("+str(100-perc_ram)+" %)\n"+ui.bar+"\n"
    new_txt = "Total Ram: "+str(round(float(total_ram)/1073741824.0,1))+" GB"
    ui.update_outputText(new_txt)
    new_txt = "Available Ram: "+str(round(float(avail_ram)/1073741824.0,1))+" GB ("+str(100-perc_ram)+" %)"
    ui.update_outputText(new_txt)
#_______________________________________________________________________________


#-------------------------------------------------------------------------------
def addTime2(ui):
    "Updates Time and writes on message box"
    now = datetime.now()
    day_time = now.strftime("%d/%m/%Y %H:%M:%S")
    log_txt+="\n["+day_time+"]\n"
    new_txt = "\n\n["+str(dt_string)+"]"
    ui.update_outputText(new_txt)
#_______________________________________________________________________________


#-------------------------------------------------------------------------------
def add_labelsText2(ui,label,text):
    "Sets text to labsls"
    _translate = QtCore.QCoreApplication.translate
    label.setText(_translate("MainWindow", text))
#_______________________________________________________________________________


#-------------------------------------------------------------------------------
def clear_LabelText2(ui,label):
    label.clear()
#_______________________________________________________________________________


#-------------------------------------------------------------------------------
def update_titleProject2(ui):
    "Updates Title of Project"
    _translate = QtCore.QCoreApplication.translate
    ui.groupBox_project.setTitle(_translate("MainWindow", ui.lineEdit_simName.text()))
#_______________________________________________________________________________


#===============================================================================
# SPECTRUM MODEL
#===============================================================================

#*******************************************************************************
def search_specModel2(ui):
    "Seachs for spectrum models"
    spec_dir=ui.current_dir+"\\models\\specModels\\"
    os.chdir(spec_dir)
    sys.path.append(spec_dir)
    # cleaning combo box of spectrum models
    ui.comboBox_specType.clear()
    new_file=None
    count=0
    for file_dir in glob.glob("*.py"):
        new_file = __import__(str(file_dir[:-3]))
        ui.specModel_list.append([new_file.specModel_name,new_file])
        ui.specModelPar_list.append(new_file.specModel_parameters)
        ui.comboBox_specType.addItem(ui.specModel_list[-1][0])
        ui.specModelsFunc.append(new_file.specFunc)
        count+=1
    if count!=0:
        ui.updateSpecModelPars()
    else:
        temp_txt = "No Spectrum models were found in folder <specModels>"
        ui.update_outputText(temp_txt)
#*******************************************************************************

#*******************************************************************************
def updateSpecModelPars2(ui):
    "Updates spectrum model parameters from when Polychromatic is selected"
    for i in range(0,len(ui.specModelPar_list)):
        current_specModel = ui.comboBox_specType.currentText()
        for i in range(0,len(ui.specModel_list)):
            if current_specModel == ui.specModel_list[i][0]:
                # clearing
                for lab in ui.specModel_labelParameters:
                    ui.clear_LabelText(lab)
                    lab.deleteLater()
                for edits in ui.specModel_lineEditParameters:
                    edits.deleteLater()
                # clearing label parameters
                ui.specModel_labelParameters = []
                ui.specModel_lineEditParameters = []
                Npars = len(ui.specModelPar_list[i])
                # clearing buttons
                ui.pushButton_showSpec.deleteLater()
                # for each parameter:
                for j in range(0,Npars):
                    # adding label for each parameter
                    ui.specModel_labelParameters.append(QtWidgets.QLabel(ui.scrollAreaWidgetContents_spectrumModel))
                    ui.specModel_labelParameters[-1].setPalette(palette_parSection)
                    ui.specModel_labelParameters[-1].setFont(font_normalLabel)
                    ui.specModel_labelParameters[-1].setObjectName(ui.specModelPar_list[i][j])
                    ui.gridLayout_specModel.addWidget(ui.specModel_labelParameters[-1], 1+j, 0, 1, 1)
                    # adding line edit entries
                    ui.specModel_lineEditParameters.append(QtWidgets.QLineEdit(ui.scrollAreaWidgetContents_numPlanes))
                    ui.specModel_lineEditParameters[-1].setFont(font_normalLabel)
                    ui.specModel_lineEditParameters[-1].setObjectName("lineEdit_"+ui.specModelPar_list[i][j])
                    ui.specModel_lineEditParameters[-1].setStyleSheet('background: '+colortxt_textEdit)
                    ui.gridLayout_specModel.addWidget(ui.specModel_lineEditParameters[-1], 1+j, 1, 1, 1)
                    # setting size
                    ui.specModel_lineEditParameters[-1].setMaximumWidth(size_entries(ui))
                    # Text in APP
                    ui.add_labelsText(ui.specModel_labelParameters[-1],ui.specModelPar_list[i][j]+":")

                # button show source spectrum
                ui.pushButton_showSpec = QtWidgets.QPushButton(ui.scrollAreaWidgetContents_spectrumModel)
                ui.pushButton_showSpec.setFont(font_button)
                ui.pushButton_showSpec.setObjectName("pushButton_showSpec")
                ui.pushButton_showSpec.setText("Show Source Spectrum")
                ui.pushButton_showSpec.setMinimumWidth(ui.rect.width()/8)
                ui.pushButton_showSpec.clicked.connect(ui.show_source_spectrum)
                ui.gridLayout_specModel.addWidget(ui.pushButton_showSpec, 1+Npars, 0, 1, 2)
#_______________________________________________________________________________


#-------------------------------------------------------------------------------
def update_specPars2(ui):
    "Updates spectrum parameters when selecting spectrum type"
    if ui.radioButton_poly.isChecked():
        # Spectrum Model
        ui.scrollArea_spectrumModel.setWidget(ui.scrollAreaWidgetContents_spectrumModel)
        ui.gridLayout_7.addWidget(ui.scrollArea_spectrumModel,39, 0, 1, 2)
        # remove label central frequency
        ui.gridLayout_7.removeWidget(ui.label_centralFreq)
        ui.label_centralFreq.setParent(None)
        # remove line edit central frequency
        ui.gridLayout_7.removeWidget(ui.lineEdit_centralFreq)
        ui.lineEdit_centralFreq.setParent(None)

    elif ui.radioButton_quasi.isChecked():
        # Spectrum Model
        ui.scrollArea_spectrumModel.setWidget(ui.scrollAreaWidgetContents_spectrumModel)
        ui.gridLayout_7.addWidget(ui.scrollArea_spectrumModel,39, 0, 1, 2)
        # remove label central frequency
        ui.gridLayout_7.removeWidget(ui.label_centralFreq)
        ui.label_centralFreq.setParent(None)
        # remove line edit central frequency
        ui.gridLayout_7.removeWidget(ui.lineEdit_centralFreq)
        ui.lineEdit_centralFreq.setParent(None)

    elif ui.radioButton_1freq.isChecked():
        ui.gridLayout_7.removeWidget(ui.scrollArea_spectrumModel)
        ui.scrollArea_spectrumModel.setParent(None)
        # add label central frequency
        ui.gridLayout_7.addWidget(ui.label_centralFreq, 38, 0, 1, 1)
        #add line edit central frequency
        ui.gridLayout_7.addWidget(ui.lineEdit_centralFreq, 38, 1, 1, 1)
        # setting label for frequency
        _translate = QtCore.QCoreApplication.translate
        ui.label_centralFreq.setText(_translate("MainWindow", "Angular Frequency (rad/s):"))
    else:
        # remove label central frequency
        ui.gridLayout_7.removeWidget(ui.label_centralFreq)
        ui.label_centralFreq.setParent(None)
        # remove line edit central frequency
        ui.gridLayout_7.removeWidget(ui.lineEdit_centralFreq)
        ui.lineEdit_centralFreq.setParent(None)
        ui.gridLayout_7.removeWidget(ui.scrollArea_spectrumModel)
        ui.scrollArea_spectrumModel.setParent(None)
#*******************************************************************************

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# GEOMETRY MODEL
#===============================================================================

#*******************************************************************************
def search_geometry2(ui):
    "searchs for geometry models <*.py> in a given directory"
    geometry_dir=ui.current_dir+"\\models\\geometry\\"
    os.chdir(geometry_dir)
    sys.path.append(geometry_dir)
    # cleaning combo box of spectrum models
    ui.comboBox_geometry.clear()
    new_file=None
    count=0
    for file_dir in glob.glob("*.py"):
        new_file = __import__(str(file_dir[:-3]))
        ui.geometry_list.append([new_file.geometry_name,new_file])
        ui.geometryPar_list.append(new_file.geometry_parameters)
        ui.comboBox_geometry.addItem(ui.geometry_list[-1][0])
        ui.geometryModelsFunc.append(new_file.geomFunc)
        ui.list_filesGeom.append(new_file)
        count+=1
    if count!=0:
        ui.updateGeometryPars()
    else:
        temp_txt = "No Geometry models were found in folder <geometry>"
        ui.update_outputText(temp_txt)
#*******************************************************************************
#*
#*
#*******************************************************************************
def updateGeometryPars2(ui):
    "Updates Geometry Model Parameters"
    try:
        for i in range(0,len(ui.geometryPar_list)):
            current_geometry = ui.comboBox_geometry.currentText()
            for i in range(0,len(ui.geometry_list)):
                if current_geometry == ui.geometry_list[i][0]:
                    # clearing
                    for lab in ui.geometry_labelParameters:
                        ui.clear_LabelText(lab)
                        lab.deleteLater()
                    for edits in ui.geometry_lineEditParameters:
                        edits.deleteLater()
                    # clearing label parameters
                    ui.geometry_labelParameters = []
                    ui.geometry_lineEditParameters = []
                    # for each parameter:

                    for j in range(0,len(ui.geometryPar_list[i])):
                        # adding label for each parameter
                        ui.geometry_labelParameters.append(QtWidgets.QLabel(ui.scrollAreaWidgetContents_geometry))
                        ui.geometry_labelParameters[-1].setPalette(palette_parSection)
                        ui.geometry_labelParameters[-1].setFont(font_normalLabel)
                        ui.geometry_labelParameters[-1].setObjectName(ui.geometryPar_list[i][j])
                        ui.gridLayout_geometry.addWidget(ui.geometry_labelParameters[-1], 1+j, 0, 1, 1)

                        # adding line edit entries
                        ui.geometry_lineEditParameters.append(QtWidgets.QLineEdit(ui.scrollAreaWidgetContents_geometry))
                        ui.geometry_lineEditParameters[-1].setFont(font_normalLabel)
                        ui.geometry_lineEditParameters[-1].setObjectName("lineEdit_"+ui.geometryPar_list[i][j])
                        ui.geometry_lineEditParameters[-1].setStyleSheet('background: '+colortxt_textEdit)
                        ui.gridLayout_geometry.addWidget(ui.geometry_lineEditParameters[-1], 1+j, 1, 1, 1)
                        # setting size
                        ui.geometry_lineEditParameters[-1].setMaximumWidth(size_entries(ui))
                        # Text in APP
                        ui.add_labelsText(ui.geometry_labelParameters[-1],ui.geometryPar_list[i][j]+":")
                        ui.geometry_lineEditParameters[0].setText("11")
    except Exception as error:
        ui.update_outputText("[Error] "+str(error))
#*******************************************************************************

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Coherence Model
#===============================================================================

#*******************************************************************************
def search_cohModel2(ui):
    "Searches for coherence model functions <*.py> in a given directory"
    coh_dir=ui.current_dir+"\\models\\cohModels\\"
    os.chdir(coh_dir)
    sys.path.append(coh_dir)
    # cleaning combo box of spectrum models
    ui.comboBox_cohModel.clear()
    new_file=None
    count=0
    for file_dir in glob.glob("*.py"):
        new_file = __import__(str(file_dir[:-3]))
        ui.cohModel_list.append([new_file.cohModel_name,new_file])
        ui.cohModelPar_list.append(new_file.cohModel_parameters)
        ui.comboBox_cohModel.addItem(ui.cohModel_list[-1][0])
        count+=1
    if count!=0:
        ui.updateCohModelPars()
    else:
        temp_txt = "No Coherence models were found in folder <cohModels>"
        ui.update_outputText(temp_txt)
#_______________________________________________________________________________
#*
#*
#*******************************************************************************
def updateCohModelPars2(ui):
    "Updates Coherence Model paramters"
    for j in range(0,len(ui.cohModelPar_list)):
        current_cohModel = ui.comboBox_cohModel.currentText()
        for i in range(0,len(ui.cohModel_list)):
            if current_cohModel == ui.cohModel_list[i][0]:
                # clearing
                for lab in ui.cohModel_labelParameters:
                    ui.clear_LabelText(lab)
                    lab.deleteLater()
                for edits in ui.cohModel_lineEditParameters:
                    edits.deleteLater()
                # clearing label parameters
                ui.cohModel_labelParameters = []
                ui.cohModel_lineEditParameters = []
                # for each parameter:
                for j in range(0,len(ui.cohModelPar_list[i])):
                    # adding label for each parameter
                    ui.cohModel_labelParameters.append(QtWidgets.QLabel(ui.scrollAreaWidgetContents_cohModel))
                    ui.cohModel_labelParameters[-1].setPalette(palette_parSection)
                    ui.cohModel_labelParameters[-1].setFont(font_normalLabel)
                    ui.cohModel_labelParameters[-1].setObjectName(ui.cohModelPar_list[i][j])
                    ui.gridLayout_cohModel.addWidget(ui.cohModel_labelParameters[-1], 1+j, 0, 1, 1)
                    # adding line edit entries
                    ui.cohModel_lineEditParameters.append(QtWidgets.QLineEdit(ui.scrollAreaWidgetContents_cohModel))
                    ui.cohModel_lineEditParameters[-1].setFont(font_normalLabel)
                    ui.cohModel_lineEditParameters[-1].setObjectName("lineEdit_"+ui.cohModelPar_list[i][j])
                    ui.cohModel_lineEditParameters[-1].setStyleSheet('background: '+colortxt_textEdit)
                    ui.gridLayout_cohModel.addWidget(ui.cohModel_lineEditParameters[-1], 1+j, 1, 1, 1)
                    # setting size
                    ui.cohModel_lineEditParameters[-1].setMaximumWidth(size_entries(ui))
                    # Text in APP
                    ui.add_labelsText(ui.cohModel_labelParameters[-1],ui.cohModelPar_list[i][j]+":")
#*******************************************************************************

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# SPECTRAL DENSITY MODEL
#===============================================================================

#*******************************************************************************
def update_specDenArea2(ui):
    "Updates Spectral Density Area"
    try:
        if ui.checkBox_specDen.isChecked():
            ui.scrollArea_SpecDensity.setWidget(ui.scrollAreaWidgetContents_SpecDensity)
            ui.gridLayout_7.addWidget(ui.scrollArea_SpecDensity,56, 0, 1, 2)
        else:
            ui.gridLayout_7.removeWidget(ui.scrollArea_SpecDensity)
            ui.scrollArea_SpecDensity.setParent(None)
    except Exception as Error:
        print(Error)
#*******************************************************************************

#*******************************************************************************
def search_specDenModels2(ui):
    "Searches Spectral Density models <*.py> in a given directory"
    specDen_dir=ui.current_dir+"\\models\\specDensity\\"
    os.chdir(specDen_dir)
    sys.path.append(specDen_dir)
    # cleaning combo box of spectral density models models
    ui.comboBox_specDenModel.clear()
    new_file=None
    count=0
    for file_dir in glob.glob("*.py"):
        new_file = __import__(str(file_dir[:-3]))
        ui.specDenModel_list.append([new_file.specDenModel_name,new_file])
        ui.specDenPar_list.append(new_file.specDenModel_parameters)
        ui.comboBox_specDenModel.addItem(ui.specDenModel_list[-1][0])
        count+=1
    if count!=0:
        ui.updateSpecDenPars()
    else:
        temp_txt = "No spectral density models were found in folder <specDensity>"
        ui.update_outputText(temp_txt)
#*******************************************************************************

#*******************************************************************************
def updateSpecDenPars2(ui):
    "Updates Spectral Density model parameters"
    for j in range(0,len(ui.specDenPar_list)):
        current_specDenModel = ui.comboBox_specDenModel.currentText()
        for i in range(0,len(ui.specDenModel_list)):
            if current_specDenModel == ui.specDenModel_list[i][0]:
                # clearing
                for lab in ui.specDenModel_labelParameters:
                    ui.clear_LabelText(lab)
                    lab.deleteLater()
                for edits in ui.specDen_lineEditParameters:
                    edits.deleteLater()
                # clearing label parameters
                ui.specDenModel_labelParameters = []
                ui.specDen_lineEditParameters = []
                # for each parameter:
                for j in range(0,len(ui.specDenPar_list[i])):
                    # adding label for each parameter
                    ui.specDenModel_labelParameters.append(QtWidgets.QLabel(ui.scrollAreaWidgetContents_SpecDensity))
                    ui.specDenModel_labelParameters[-1].setPalette(palette_parSection)
                    ui.specDenModel_labelParameters[-1].setFont(font_normalLabel)
                    ui.specDenModel_labelParameters[-1].setObjectName(ui.specDenPar_list[i][j])
                    ui.gridLayout_SpecDensity.addWidget(ui.specDenModel_labelParameters[-1], 4+j, 0, 1, 1)
                    # adding line edit entries
                    ui.specDen_lineEditParameters.append(QtWidgets.QLineEdit(ui.scrollAreaWidgetContents_SpecDensity))
                    ui.specDen_lineEditParameters[-1].setFont(font_normalLabel)
                    ui.specDen_lineEditParameters[-1].setObjectName("lineEdit_"+ui.specDenPar_list[i][j])
                    ui.specDen_lineEditParameters[-1].setStyleSheet('background: '+colortxt_textEdit)
                    ui.gridLayout_SpecDensity.addWidget(ui.specDen_lineEditParameters[-1], 4+j, 1, 1, 1)
                    # setting size
                    ui.specDen_lineEditParameters[-1].setMaximumWidth(size_entries(ui))
                    # Text in APP
                    ui.add_labelsText(ui.specDenModel_labelParameters[-1],ui.specDenPar_list[i][j]+":")
#*******************************************************************************

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
#*******************************************************************************
# PROPAGATION PLANES
#*******************************************************************************
#===============================================================================


#*******************************************************************************
def update_numPlanes2(ui):
    "Updates number of propagation planes"
    current_numPlanes = ui.spinBox_numPlanes.value()  # number of planes
    if current_numPlanes==1:                          # if current Np = 1
        if ui.tabWidget_propsystem.count()==2:
            ui.tabWidget_propsystem.removeTab(1)

        elif ui.tabWidget_propsystem.count()==3:
            ui.tabWidget_propsystem.removeTab(2)
            ui.tabWidget_propsystem.removeTab(1)

    elif current_numPlanes==2:
        if ui.tabWidget_propsystem.count()==1:
            ui.tabWidget_propsystem.addTab(ui.tab_planes_list[ui.tabWidget_propsystem.count()],"Plane 2")
        elif ui.tabWidget_propsystem.count()==3:
            ui.tabWidget_propsystem.removeTab(2)

    elif current_numPlanes==3:
        if ui.tabWidget_propsystem.count()==1:
            ui.tabWidget_propsystem.addTab(ui.tab_planes_list[1],"Plane 2")
            ui.tabWidget_propsystem.addTab(ui.tab_planes_list[2],"Plane 3")
        elif ui.tabWidget_propsystem.count()==2:
            ui.tabWidget_propsystem.addTab(ui.tab_planes_list[2],"Plane 3")
#*******************************************************************************

#*******************************************************************************
def updatePropPlanePars2(ui):
    "Updates Propagation Planes labels, lineedits, models and parameters"
    # for later...
    _translate = QtCore.QCoreApplication.translate

    current_numPlanes = 3#int(ui.spinBox_numPlanes.text())
    # adding labels, lineEdits, checkboxs and comboBoxes
    for iP in range(0,ui.max_numPlanes):
        # tab
        ui.tab_planes_list.append(QtWidgets.QWidget())
        ui.tab_planes_list[-1].setPalette(palette_tabPlane)
        ui.tab_planes_list[-1].setObjectName("tab_plane"+str(iP+1))

        # Tab grid layout
        ui.gridLayoutTab_list.append(QtWidgets.QGridLayout(ui.tab_planes_list[-1]))
        ui.tab_planes_list[-1].setObjectName("gridLayout_"+str(iP+1))

        # scroll area
        ui.scrollArea_propPlanes_list.append(QtWidgets.QScrollArea(ui.tab_planes_list[-1]))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ui.scrollArea_propPlanes_list[-1].sizePolicy().hasHeightForWidth())
        ui.scrollArea_propPlanes_list[-1].setSizePolicy(sizePolicy)
        ui.scrollArea_propPlanes_list[-1].setMinimumSize(QtCore.QSize(0, 300))
        ui.scrollArea_propPlanes_list[-1].setPalette(palette_scrollAreaPlane1)
        ui.scrollArea_propPlanes_list[-1].setWidgetResizable(True)
        ui.scrollArea_propPlanes_list[-1].setObjectName("scrollArea_plane"+str(iP+1))

        # scrollArea Widget Contents
        ui.scrollAreaWidgetContents_propPlanes_list.append(QtWidgets.QWidget())
        ui.scrollAreaWidgetContents_propPlanes_list[-1].setGeometry(QtCore.QRect(0, 0, 393, 198))
        ui.scrollAreaWidgetContents_propPlanes_list[-1].setObjectName("scrollAreaWidgetContents_plane"+str(iP+1))

        # gridLayout
        ui.gridLayout_propPlanes_list.append(QtWidgets.QGridLayout(ui.scrollAreaWidgetContents_propPlanes_list[-1]))
        ui.gridLayout_propPlanes_list[-1].setObjectName("gridLayoutPropPlane_"+str(iP+1))

        # Putting together everything
        ui.scrollArea_propPlanes_list[-1].setWidget(ui.scrollAreaWidgetContents_propPlanes_list[-1])
        #ui.formTab_layouts_list[-1].setWidget(0, QtWidgets.QFormLayout.SpanningRole, ui.scrollArea_propPlanes_list[-1])
        ui.gridLayoutTab_list[-1].addWidget(ui.scrollArea_propPlanes_list[-1], 0, 0, 1, 1)
        ui.tabWidget_propsystem.addTab(ui.tab_planes_list[-1], "Plane "+str(iP+1))

        # adding label distance
        ui.label_distances_list.append(QtWidgets.QLabel(ui.scrollAreaWidgetContents_propPlanes_list[-1]))
        ui.label_distances_list[-1].setPalette(palette_parSection)
        ui.label_distances_list[-1].setFont(font_normalLabel)
        ui.label_distances_list[-1].setObjectName("label_distance"+str(iP+1))
        ui.gridLayout_propPlanes_list[-1].addWidget(ui.label_distances_list[-1], 2, 0, 1, 1)
        ui.label_distances_list[-1].setText(_translate("MainWindow", "Distance (m):"))

        # adding lineEdit distance
        ui.lineEdit_distances_list.append(QtWidgets.QLineEdit(ui.scrollAreaWidgetContents_propPlanes_list[-1]))
        ui.lineEdit_distances_list[-1].setText("100")
        ui.lineEdit_distances_list[-1].setObjectName("lineEdit_distance"+str(iP+1))
        ui.lineEdit_distances_list[-1].setStyleSheet('background: '+colortxt_textEdit)
        ui.gridLayout_propPlanes_list[-1].addWidget(ui.lineEdit_distances_list[-1], 2, 1, 1, 1)
        ui.lineEdit_distances_list[-1].setMaximumWidth(size_entries(ui))
        ui.lineEdit_distances_list[-1].textChanged.connect(ui.updateSpaceRes)

        # text browser with spatial resolution
        ui.textBrowser_spatialRes_list.append(QtWidgets.QTextBrowser(ui.scrollAreaWidgetContents_propPlanes_list[-1]))
        ui.textBrowser_spatialRes_list[-1].setPalette(palette_outputText)
        ui.textBrowser_spatialRes_list[-1].setMinimumHeight(ui.rect.height()/16)
        ui.textBrowser_spatialRes_list[-1].setFont(font_outText)
        ui.textBrowser_spatialRes_list[-1].setObjectName("textBrowser_plane"+str(iP))
        ui.gridLayout_propPlanes_list[-1].addWidget(ui.textBrowser_spatialRes_list[-1], 3, 0, 1, 3)
        ui.textBrowser_spatialRes_list[-1].append("Spatial Resolution in Plane "+str(iP+1)+":")

        # adding CheckBox farfield
        ui.checkBox_farfied_list.append(QtWidgets.QCheckBox(ui.scrollAreaWidgetContents_propPlanes_list[-1]))
        ui.checkBox_farfied_list[-1].setFont(font_normalLabel)
        ui.checkBox_farfied_list[-1].setChecked(True)
        ui.checkBox_farfied_list[-1].setPalette(palette_parSection)
        ui.checkBox_farfied_list[-1].setObjectName("checkBox_farfield"+str(iP+1))
        ui.gridLayout_propPlanes_list[-1].addWidget(ui.checkBox_farfied_list[-1], 5, 0, 1, 1)
        ui.checkBox_farfied_list[-1].setText(_translate("MainWindow", "Far-field"))

        #***********************************************************************
        # PUPIL
        #***********************************************************************
        # adding CheckBox Pupil
        ui.checkBox_pupil_list.append(QtWidgets.QCheckBox(ui.scrollAreaWidgetContents_propPlanes_list[-1]))
        ui.checkBox_pupil_list[-1].setFont(font_normalLabel)
        ui.checkBox_pupil_list[-1].setPalette(palette_parSection)
        ui.checkBox_pupil_list[-1].setObjectName("checkBox_pupil"+str(iP+1))
        ui.gridLayout_propPlanes_list[-1].addWidget(ui.checkBox_pupil_list[-1], 6, 0, 1, 1)
        ui.checkBox_pupil_list[-1].setText(_translate("MainWindow", "Pupil"))
        ui.checkBox_pupil_list[-1].stateChanged.connect(ui.updatePupilArea)

        # scroll area for Pupil function and parameters
        ui.scrollArea_pupil_list.append(QtWidgets.QScrollArea(ui.scrollAreaWidgetContents_propPlanes_list[-1]))
        ui.scrollArea_pupil_list[-1].setWidgetResizable(True)
        ui.scrollArea_pupil_list[-1].setObjectName("ScrollArea_pupil"+str(iP))
        ui.scrollArea_pupil_list[-1].setMinimumHeight(ui.rect.height()/12.)
        ui.scrollAreaWidgetContents_pupil_list.append(QtWidgets.QWidget())
        ui.scrollAreaWidgetContents_pupil_list[-1].setGeometry(QtCore.QRect(0, 0, 421, 85))
        ui.scrollAreaWidgetContents_pupil_list[-1].setObjectName("scrollAreaWidgetContents_geometry")
        ui.gridLayout_pupil_list.append(QtWidgets.QGridLayout(ui.scrollAreaWidgetContents_pupil_list[-1]))
        ui.gridLayout_pupil_list[-1].setObjectName("gridLayout_pupil"+str(iP))
        ui.scrollArea_pupil_list[-1].setWidget(ui.scrollAreaWidgetContents_pupil_list[-1])
        ui.gridLayout_propPlanes_list[-1].addWidget(ui.scrollArea_pupil_list[-1], 7, 0, 1, 3)

        # adding label pupilGeom
        ui.label_pupilGeom_list.append(QtWidgets.QLabel(ui.scrollAreaWidgetContents_pupil_list[-1]))
        ui.label_pupilGeom_list[-1].setPalette(palette_parSection)
        ui.label_pupilGeom_list[-1].setFont(font_normalLabel)
        ui.label_pupilGeom_list[-1].setObjectName("label_pupilGeom"+str(iP+1))
        ui.gridLayout_pupil_list[-1].addWidget(ui.label_pupilGeom_list[-1], 0, 0, 1, 1)
        ui.label_pupilGeom_list[-1].setText(_translate("MainWindow", "Pupil Geometry:"))

        # combo box pupil function
        ui.comboBox_pupilGeom_list.append(QtWidgets.QComboBox(ui.scrollAreaWidgetContents_pupil_list[-1]))
        ui.comboBox_pupilGeom_list[-1].setObjectName("comboBox_pupilFunc"+str(iP+1))
        ui.gridLayout_pupil_list[-1].addWidget(ui.comboBox_pupilGeom_list[-1], 0, 1, 1, 1)
        # setting size
        ui.comboBox_pupilGeom_list[-1].setMaximumWidth(ui.minwidth_combo)
        ui.comboBox_pupilGeom_list[-1].setStyleSheet('''*
        QComboBox QAbstractItemView
            {
            min-width: '''+str(ui.maxWidthView_combo)+'''px;
            }
        ''')
        #ui.comboBox_pupilGeom_list[-1].currentIndexChanged.connect(ui.updatePupilGeomPars)
        ui.comboBox_pupilGeom_list[-1].currentIndexChanged.connect(functools.partial(ui.updatePupilGeomPars,iP))
        #***********************************************************************
        #///////////////////////////////////////////////////////////////////////
        #***********************************************************************

        #***********************************************************************
        # OPTICS
        #***********************************************************************

        # adding checkbox for optics
        ui.checkBox_optics_list.append(QtWidgets.QCheckBox(ui.scrollAreaWidgetContents_propPlanes_list[-1]))
        ui.checkBox_optics_list[-1].setPalette(palette_parSection)
        ui.checkBox_optics_list[-1].setFont(font_normalLabel)
        ui.checkBox_optics_list[-1].setObjectName("checkBox_optics_"+str(iP+1))
        ui.gridLayout_propPlanes_list[-1].addWidget(ui.checkBox_optics_list[-1], 9, 0, 1, 1)
        ui.checkBox_optics_list[-1].setText(_translate("MainWindow", "Optics"))
        ui.checkBox_optics_list[-1].stateChanged.connect(ui.update_opticsArea)

        # scroll area for Optics parameters
        ui.scrollArea_optics_list.append(QtWidgets.QScrollArea(ui.scrollAreaWidgetContents_propPlanes_list[-1]))
        ui.scrollArea_optics_list[-1].setWidgetResizable(True)
        ui.scrollArea_optics_list[-1].setObjectName("ScrollArea_optics"+str(iP))
        ui.scrollArea_optics_list[-1].setMinimumHeight(ui.rect.height()/8.)
        ui.scrollAreaWidgetContents_optics_list.append(QtWidgets.QWidget())
        ui.scrollAreaWidgetContents_optics_list[-1].setGeometry(QtCore.QRect(0, 0, 421, 85))
        ui.scrollAreaWidgetContents_optics_list[-1].setObjectName("scrollAreaWidgetContents_optics")
        ui.gridLayout_optics_list.append(QtWidgets.QGridLayout(ui.scrollAreaWidgetContents_optics_list[-1]))
        ui.gridLayout_optics_list[-1].setObjectName("gridLayout_optics"+str(iP))
        ui.scrollArea_optics_list[-1].setWidget(ui.scrollAreaWidgetContents_optics_list[-1])
        ui.gridLayout_propPlanes_list[-1].addWidget(ui.scrollArea_optics_list[-1], 11, 0, 1, 3)

        # adding label Optical Device
        ui.label_optDeviceFunc_list.append(QtWidgets.QLabel(ui.scrollAreaWidgetContents_optics_list[-1]))
        ui.label_optDeviceFunc_list[-1].setPalette(palette_parSection)
        ui.label_optDeviceFunc_list[-1].setFont(font_normalLabel)
        ui.label_optDeviceFunc_list[-1].setObjectName("label_optDevice"+str(iP+1))
        ui.gridLayout_optics_list[-1].addWidget(ui.label_optDeviceFunc_list[-1], 13, 0, 1, 1)
        ui.label_optDeviceFunc_list[-1].setText(_translate("MainWindow", "Optical Device Function:"))

        # combo box Optical Device Function
        ui.comboBox_optDeviceFunc_list.append(QtWidgets.QComboBox(ui.scrollAreaWidgetContents_optics_list[-1]))
        ui.comboBox_optDeviceFunc_list[-1].setObjectName("comboBox_optDevice"+str(iP+1))
        ui.gridLayout_optics_list[-1].addWidget(ui.comboBox_optDeviceFunc_list[-1], 13, 1, 1, 1)
        # setting size
        ui.comboBox_optDeviceFunc_list[-1].setMaximumWidth(size_entries(ui))
        ui.comboBox_optDeviceFunc_list[-1].setStyleSheet('''*
        QComboBox QAbstractItemView
            {
            min-width: '''+str(ui.maxWidthView_combo)+'''px;
            }
        ''')
        ##ui.comboBox_optDeviceFunc_list[-1].addItem("None",0)
        ui.comboBox_optDeviceFunc_list[-1].currentIndexChanged.connect(functools.partial(ui.updateOpticsFuncPars,iP))

        #***********************************************************************
        #///////////////////////////////////////////////////////////////////////
        #***********************************************************************

        # adding tabwiget
        ui.tabWidget_propsystem.setTabText(ui.tabWidget_propsystem.indexOf(ui.tab_planes_list[-1]), _translate("MainWindow", "Plane "+str(iP+1)))

    # add all to gridlayout 7
    ui.gridLayout_7.addWidget(ui.tabWidget_propsystem, 65, 0, 1, 2)

#*******************************************************************************

#===============================================================================
# Pupil Functions
#===============================================================================

#*******************************************************************************
def updatePupilArea2(ui):
    "Updates pupil scroll area"
    for i in range(0,ui.max_numPlanes):
        if ui.checkBox_pupil_list[i].checkState():
            ui.scrollArea_pupil_list[i].setWidget(ui.scrollAreaWidgetContents_pupil_list[i])
            ui.gridLayout_propPlanes_list[i].addWidget(ui.scrollArea_pupil_list[i], 7, 0, 1, 3)
        else:
            ui.gridLayout_propPlanes_list[i].removeWidget(ui.scrollArea_pupil_list[i])
            ui.scrollArea_pupil_list[i].setParent(None)
#*******************************************************************************

#*******************************************************************************
def searchPupilGeom2(ui):
    "Search for Pupil geometry functions <*.py>"
    try:
        pupilGeom_dir = ui.current_dir+"\\models\\pupilGeom\\"
        os.chdir(pupilGeom_dir)
        sys.path.append(pupilGeom_dir)
        # cleaning combo box of Pupil Geometric Functions
        for i in range(0,ui.max_numPlanes):
            ui.comboBox_pupilGeom_list[i].clear()

        # for each propagation plane
        for i in range(0,ui.max_numPlanes):
            new_file=None
            count=0
            for file_dir in glob.glob("*.py"):
                new_file = __import__(str(file_dir[:-3]))
                ui.pupilGeomFunc_list[i].append([new_file.pupilGeom_name,new_file,new_file.geomFunc])
                ui.pupilGeomFuncPars_list[i].append(new_file.pupilGeom_parameters)
                ui.comboBox_pupilGeom_list[i].addItem(ui.pupilGeomFunc_list[i][-1][0],i+1)
                count+=1
            if count!=0:
                #ui.updatePupilGeomPars()
                pass
            else:
                temp_txt = "No Pupil Geometric Models were found in folder <pupilGeom>"
                ui.update_outputText(temp_txt)
        #ui.comboBox_pupilGeom_list[i].currentIndexChanged.connect(ui.updatePupilGeomPars)
    except Exception as error:
        print(error)
        ui.update_outputText(str(error)+" at <mainFunctions.py> in function <searchPupilGeom2>")
#*******************************************************************************

#*******************************************************************************
def updatePupilGeomPars2(ui,Plane):
    "Updates Pupil Geometry parameters"

    # current selected Geometric model in plane <iP>
    current_pupilGeomModel = ui.comboBox_pupilGeom_list[Plane].currentText()

    # clearing
    for lab in ui.pupilGeom_labelParameters[Plane]:
        ui.clear_LabelText(lab)
        lab.deleteLater()
    for edits in ui.pupilGeom_lineEditParameters[Plane]:
        edits.deleteLater()
    # clearing label parameters
    ui.pupilGeom_labelParameters[Plane] = []
    ui.pupilGeom_lineEditParameters[Plane] = []

    # for each model
    num_models = len(ui.pupilGeomFunc_list[Plane])
    for i in range(0,num_models):
        if current_pupilGeomModel == ui.pupilGeomFunc_list[Plane][i][0]:
            # for each parameter:
            for j in range(0,len(ui.pupilGeomFuncPars_list[Plane][i])):
                # adding label for each parameter
                ui.pupilGeom_labelParameters[Plane].append(QtWidgets.QLabel(ui.scrollAreaWidgetContents_pupil_list[Plane]))
                ui.pupilGeom_labelParameters[Plane][-1].setPalette(palette_parSection)
                ui.pupilGeom_labelParameters[Plane][-1].setFont(font_normalLabel)
                ui.gridLayout_pupil_list[Plane].addWidget(ui.pupilGeom_labelParameters[Plane][-1], 1+j, 0, 1, 1)
                # adding line edit entries
                ui.pupilGeom_lineEditParameters[Plane].append(QtWidgets.QLineEdit(ui.scrollAreaWidgetContents_pupil_list[Plane]))
                ui.pupilGeom_lineEditParameters[Plane][-1].setFont(font_normalLabel)
                ui.pupilGeom_lineEditParameters[Plane][-1].setStyleSheet('background: '+colortxt_textEdit)
                ui.gridLayout_pupil_list[Plane].addWidget(ui.pupilGeom_lineEditParameters[Plane][-1], 1+j, 1, 1, 1)
                # setting size:
                ui.pupilGeom_lineEditParameters[Plane][-1].setMaximumWidth(size_entries(ui))
                # Text in APP:
                ui.add_labelsText(ui.pupilGeom_labelParameters[Plane][-1],ui.pupilGeomFuncPars_list[Plane][i][j]+":")
#*******************************************************************************

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Optic Devices Functions
#===============================================================================

#*******************************************************************************
def update_opticsArea2(ui):
    "Updates optical device Scroll Area"
    for i in range(0,ui.max_numPlanes):
        try:
            if ui.checkBox_optics_list[i].isChecked():
                ui.scrollArea_optics_list[i].setWidget(ui.scrollAreaWidgetContents_optics_list[i])
                ui.gridLayout_propPlanes_list[i].addWidget(ui.scrollArea_optics_list[i], 11, 0, 1, 3)
            else:
                ui.gridLayout_propPlanes_list[i].removeWidget(ui.scrollArea_optics_list[i])
                ui.scrollArea_optics_list[i].setParent(None)
        except Exception as Error:
            print(Error)
#*******************************************************************************

#*******************************************************************************
def searchOpticsFunc2(ui):
    "Search for optical device function in <functions\optics>"
    try:
        opticsFunc_dir = ui.current_dir+"\\models\\optics"
        os.chdir(opticsFunc_dir)
        sys.path.append(opticsFunc_dir)

        # cleaning combo box of Pupil Geometric Functions
        for i in range(0,ui.max_numPlanes):
            ui.comboBox_optDeviceFunc_list[i].clear()

        # for each propagation plane
        for i in range(0,ui.max_numPlanes):
            new_file=None
            count=0
            for file_dir in glob.glob("*.py"):
                new_file = __import__(str(file_dir[:-3]))
                ui.optDeviceFunc_list[i].append([new_file.optics_name,new_file,new_file.optics_function])
                ui.optDeviceFuncPars_list[i].append(new_file.optics_parameters)
                ui.comboBox_optDeviceFunc_list[i].addItem(ui.optDeviceFunc_list[i][-1][0],i+1)
                count+=1
            if count!=0:
                pass
            else:
                temp_txt = "No Optical Device Models were found in folder <optics>"
                ui.update_outputText(temp_txt)


    except Exception as Error:
        print(Error)
        #ui.comboBox_pupilGeom_list[i].currentIndexChanged.connect(ui.updatePupilGeomPars)
#*******************************************************************************

#*******************************************************************************
def updateOpticsFuncPars2(ui,Plane):
    "Update Optical Function Paremeters"
    # current selected Geometric model in plane <iP>
    current_opticsModel = ui.comboBox_optDeviceFunc_list[Plane].currentText()

    # clearing
    for lab in ui.optDeviceFunc_labelParameters[Plane]:
        ui.clear_LabelText(lab)
        lab.deleteLater()
    for edits in ui.optDevicePars_lineEditParameters[Plane]:
        edits.deleteLater()
    # clearing label parameters
    ui.optDeviceFunc_labelParameters[Plane] = []
    ui.optDevicePars_lineEditParameters[Plane] = []

    # for each model
    num_models = len(ui.optDeviceFunc_list[Plane])
    for i in range(0,num_models):
        if current_opticsModel == ui.optDeviceFunc_list[Plane][i][0]:
            # for each parameter:
            for j in range(0,len(ui.optDeviceFuncPars_list[Plane][i])):

                # adding label for each parameter
                ui.optDeviceFunc_labelParameters[Plane].append(QtWidgets.QLabel(ui.scrollAreaWidgetContents_optics_list[Plane]))
                ui.optDeviceFunc_labelParameters[Plane][-1].setPalette(palette_parSection)
                ui.optDeviceFunc_labelParameters[Plane][-1].setFont(font_normalLabel)
                ui.gridLayout_optics_list[Plane].addWidget(ui.optDeviceFunc_labelParameters[Plane][-1], 15+j, 0, 1, 1)
                # adding line edit entries
                ##optDevice_lineEditParameters
                ui.optDevicePars_lineEditParameters[Plane].append(QtWidgets.QLineEdit(ui.scrollAreaWidgetContents_optics_list[Plane]))
                ui.optDevicePars_lineEditParameters[Plane][-1].setFont(font_normalLabel)
                ui.optDevicePars_lineEditParameters[Plane][-1].setStyleSheet('background: '+colortxt_textEdit)
                ui.gridLayout_optics_list[Plane].addWidget(ui.optDevicePars_lineEditParameters[Plane][-1], 15+j, 1, 1, 1)
                # setting size
                ui.optDevicePars_lineEditParameters[Plane][-1].setMaximumWidth(size_entries(ui))
                # Text in APP
                ui.add_labelsText(ui.optDeviceFunc_labelParameters[Plane][-1],ui.optDeviceFuncPars_list[Plane][i][j]+":")
#*******************************************************************************

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#-------------------------------------------------------------------------------
def updateSpaceRes2(ui):
    "Updates Spatial resolution for each plane"
    try:
        dx_list = []
        numPlanes = int(ui.spinBox_numPlanes.text())
        N    = int(ui.lineEdit_N.text())
        NZ   = int(ui.lineEdit_NZ.text())
        angF = float(ui.lineEdit_centralFreq.text())

        for i in range(0,numPlanes):
            ds = None
            if i ==0:
                ds = float(ui.lineEdit_sourceRes.text())
                distance = float(ui.lineEdit_distances_list[i].text())
                if ui.checkBox_FFT.isChecked():
                    dx = 2*pi*3e8*distance/(angF*NZ*ds)
                else:
                    dx = 2*pi*3e8*distance/(angF*N*ds)

                text1 = "Spatial Resolution of Plane "+str(i+1)+":  "+"{:.6E}".format(Decimal(str(dx)))+" m"
                ui.textBrowser_spatialRes_list[i].setText(text1)
                dx_list.append(dx)
                ## van Cittert-Zernike correlation length
                try:
                    vCZCL = 7.66*3e8*distance/(2*angF*float(ui.geometry_lineEditParameters[0].text())*ds)
                    text2 = "Van Cittert-Zernike correlation length at Plane "+str(i+1)+":  "+"{:.6E}".format(Decimal(str(vCZCL)))+" m"
                    ui.textBrowser_spatialRes_list[i].setText(text1+"\n\n"+text2)
                except Exception as error:
                    ui.update_outputText(error)
            else:
                ds = float(dx_list[i-1])
                distance = float(ui.lineEdit_distances_list[i].text())
                dx = 2*pi*3e8*distance/(angF*N*ds)
                dx_list.append(dx)

                text1 = "Spatial Resolution of Plane "+str(i+1)+":  "+"{:.6E}".format(Decimal(str(dx)))+" m"
                ui.textBrowser_spatialRes_list[i].setText(text1)
                ## van Cittert-Zernike correlation length
                try:
                    vCZCL = 7.66*3e8*distance/(angF*ds)
                    text2 = "Van Cittert-Zernike correlation length (assuming size=1) at Plane "+str(i+1)+":  "+"{:.6E}".format(Decimal(str(vCZCL)))+" m"
                    ui.textBrowser_spatialRes_list[i].setText(text1+"\n\n"+text2)
                except Exception as error:
                    ui.update_outputText(error)

            ui.dx_list = dx_list

    except Exception as error:
        pass ## ui.update_outputText(error)
#_______________________________________________________________________________


#-------------------------------------------------------------------------------
def updateOmegaRes2(ui):
    "Updates the angular frequency resolution"
    try:
        theta = float(ui.lineEdit_theta.text())
        N = float(ui.lineEdit_N.text())
        if ui.checkBox_FFT.isChecked():
            N = float(ui.lineEdit_NZ.text())

        for i in range(0,int(ui.spinBox_numPlanes.text())):
            if i==0:
                ds = float(ui.lineEdit_sourceRes.text())
            else:
                ds = ui.dx_list[i]
            ui.d_omega = 2*sqrt(2)*pi*3e8/(N*ds*sin(theta))
            ui.textBrowser_spatialRes_list[i].setText('Angular Frequency Resolution: '+"{:.6E}".format(Decimal(str(ui.d_omega)))+" rad/s")

    except Exception as error:
        pass ##ui.update_outputText(error)
#_______________________________________________________________________________


#===============================================================================
# From File Updates
#===============================================================================

#*******************************************************************************
def updateGeoFromFile2(ui):
    if ui.checkBox_geoFromFile.checkState():
        #ui.gridLayout_cohModel.removeWidget(ui.scrollArea_cohModel)
        #ui.scrollArea_cohModel.setParent(None)
        ui.gridLayout_geometry.removeWidget(ui.scrollArea_geometry)
        ui.scrollArea_geometry.setParent(None)
        ui.checkBox_CSDAFromFile.setVisible(False)
        ui.lineEdit_dirCSDAmatrix.setVisible(False)
        ui.toolButton_CSDAfromfile.setVisible(False)
    else:
        #ui.scrollArea_cohModel.setWidget(ui.scrollAreaWidgetContents_cohModel)
        #ui.gridLayout_7.addWidget(ui.scrollArea_cohModel,51, 0, 1, 2)
        ui.checkBox_CSDAFromFile.setVisible(True)
        ui.lineEdit_dirCSDAmatrix.setVisible(True)
        ui.toolButton_CSDAfromfile.setVisible(True)
        ui.scrollArea_geometry.setWidget(ui.scrollAreaWidgetContents_geometry)
        ui.gridLayout_7.addWidget(ui.scrollArea_geometry,49, 0, 1, 2)
#*******************************************************************************

#*******************************************************************************
def updateCSDAFromFile2(ui):
    "Updates CSDA from file section"
    if ui.checkBox_CSDAFromFile.checkState():
        ui.checkBox_geoFromFile.setVisible(False)
        ui.lineEdit_dirGeoMatrix.setVisible(False)
        ui.toolButton_geoFromFile.setVisible(False)

        ui.gridLayout_cohModel.removeWidget(ui.scrollArea_cohModel)
        ui.scrollArea_cohModel.setParent(None)
        ui.gridLayout_geometry.removeWidget(ui.scrollArea_geometry)
        ui.scrollArea_geometry.setParent(None)
    else:
        ui.checkBox_geoFromFile.setVisible(True)
        ui.lineEdit_dirGeoMatrix.setVisible(True)
        ui.toolButton_geoFromFile.setVisible(True)

        ui.scrollArea_cohModel.setWidget(ui.scrollAreaWidgetContents_cohModel)
        ui.gridLayout_7.addWidget(ui.scrollArea_cohModel,51, 0, 1, 2)
        ui.scrollArea_geometry.setWidget(ui.scrollAreaWidgetContents_geometry)
        ui.gridLayout_7.addWidget(ui.scrollArea_geometry,49, 0, 1, 2)
#*******************************************************************************

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#*******************************************************************************
def updatePropQuantity2(ui):
    "Updates Propagation Quantity Section"
    _translate = QtCore.QCoreApplication.translate
    if ui.comboBox_propQuant.currentIndex()==0:
        #ui.checkBox_freqDep.setVisible(False)
        ui.comboBox_specPropModels.setVisible(False)
        ui.label_theta.setVisible(False)
        ui.label_propSpecModel.setVisible(False)
        ui.lineEdit_theta.setVisible(False)

        # TEXT BOX
        ui.lineEdit_N.textChanged.connect(ui.updateSpaceRes)
        ui.lineEdit_NZ.textChanged.connect(ui.updateSpaceRes)
        ui.lineEdit_centralFreq.textChanged.connect(ui.updateSpaceRes)
        ui.lineEdit_sourceRes.textChanged.connect(ui.updateSpaceRes)
        ui.lineEdit_theta.textChanged.connect(ui.updateSpaceRes)
        for i in range(0,int(ui.spinBox_numPlanes.text())):
            ui.lineEdit_distances_list[i].textChanged.connect(ui.updateSpaceRes)
        ui.updateSpaceRes()

    elif ui.comboBox_propQuant.currentIndex()==1:
        #ui.checkBox_freqDep.setText(_translate("MainWindow", "Frequency-independent Spatial Coherence"))
        ui.comboBox_specPropModels.setVisible(True)
        ui.label_propSpecModel.setVisible(True)
        ui.label_theta.setVisible(True)
        ui.lineEdit_theta.setVisible(True)

        # TEXT BOX
        ui.lineEdit_N.textChanged.connect(ui.updateOmegaRes)
        ui.lineEdit_NZ.textChanged.connect(ui.updateOmegaRes)
        ui.lineEdit_centralFreq.textChanged.connect(ui.updateOmegaRes)
        ui.lineEdit_sourceRes.textChanged.connect(ui.updateOmegaRes)
        ui.lineEdit_theta.textChanged.connect(ui.updateOmegaRes)
        for i in range(0,int(ui.spinBox_numPlanes.text())):
            ui.lineEdit_distances_list[i].textChanged.connect(ui.updateOmegaRes)
        ui.updateOmegaRes()
#_______________________________________________________________________________

