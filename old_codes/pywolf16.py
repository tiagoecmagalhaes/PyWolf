# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyProPCL4.UI'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QInputDialog, QFileDialog, QLabel, QHBoxLayout

import numpy
from decimal import Decimal

import pyopencl
import os
import psutil
import glob
import sys


current_dir = os.getcwd()
sys.path.insert(1, current_dir+"\plot")

from windowPlot import *
from palettes import *
from fonts import *
from color import *
from platdev import *
from testPars import *
from createSource import *
from startSim import *
from mainFunctions import *

from datetime import datetime

global W_temp


class Ui_MainWindow(object):

    def setupUi(self, MainWindow,appname,rect,current_dir,log_txt,output_txt):

        self.log_txt    = log_txt
        self.output_txt = output_txt
        self.rect       = rect
        self.current_dir = current_dir

        #=======================================================================
        # Main Window
        #=======================================================================
        # setting app name
        MainWindow.setObjectName("MainWindow")

        # setting app window size
        MainWindow.resize(2*rect.width()/3, 2*rect.height()/3)

        # MainWindows Color palette
        MainWindow.setPalette(palette_mainwindow)

        # not a document
        MainWindow.setDocumentMode(False)
        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # Central Widget
        #=======================================================================

        # MainWindow -> Central Widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # adding grid to central widget
        self.gridLayout_main = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_main.setObjectName("gridLayout_main")

        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # groupBox
        #=======================================================================

        # MainWindow -> Central Widget -> groupBox Layout

        # adding groupbox to central widget
        self.groupBox_project = QtWidgets.QGroupBox(self.centralwidget)

        #font = QtGui.QFont()
        #font.setPointSize(12)
        self.groupBox_project.setFont(font_title)
        self.groupBox_project.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_project.setCheckable(False)
        self.groupBox_project.setObjectName("groupBox_project")
        self.groupBox_project.setPalette(palette_groupBoxProject)

        self.gridLayout_main_project = QtWidgets.QGridLayout(self.groupBox_project)
        self.gridLayout_main_project.setObjectName("gridLayout_main_project")

        #self.groupBox_project.setStyleSheet('QGroupBox:title {color: rgb(255, 255, 255);}')
        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # gridLayout Project
        #=======================================================================

        # MainWindow -> Central Widget -> groupBox Layout -> gridLayout Project

        self.gridLayout_project = QtWidgets.QGridLayout()
        self.gridLayout_project.setObjectName("gridLayout_project")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_project.addItem(spacerItem, 1, 1, 1, 1)
        #self.gridLayout_project.setRowMinimumHeight(1, int(0.5*self.rect.height()))
        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # Message Scroll Area Color palette
        #=======================================================================
        # MainWindow -> Central Widget -> groupBox project -> Message area

        self.scrollArea_messages = QtWidgets.QScrollArea(self.groupBox_project)
        self.scrollArea_messages.setPalette(palette_messageArea)
        #self.scrollArea_messages.setMaximumHeight(self.rect.height()/3)
        self.scrollArea_messages.setWidgetResizable(True)
        self.scrollArea_messages.setObjectName("scrollArea_messages")

        self.scrollAreaWidgetContents_messages = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_messages.setGeometry(QtCore.QRect(0, 0, 465, 490))
        self.scrollAreaWidgetContents_messages.setObjectName("scrollAreaWidgetContents_9")

        self.gridLayout_messages = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_messages)
        self.gridLayout_messages.setObjectName("gridLayout_messages")
        #_______________________________________________________________________


        #-----------------------------------------------------------------------
        # Output Text Box
        #-----------------------------------------------------------------------
        self.textBrowser = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents_messages)
        self.textBrowser.setPalette(palette_outputText)
        self.textBrowser.setMinimumHeight(2*rect.height()/12)

        # font
        self.textBrowser.setFont(font_outText)

        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_messages.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.textBrowser.append(str(output_txt))
        #_______________________________________________________________________


        #-----------------------------------------------------------------------
        # Graphics Zone palette
        #-----------------------------------------------------------------------
        """
        self.graphicsView_optSys = QtWidgets.QGraphicsView(self.scrollAreaWidgetContents_messages)
        self.graphicsView_optSys.setObjectName("graphicsView_optSys")
        self.gridLayout_messages.addWidget(self.graphicsView_optSys, 7, 0, 1, 1)
        """

        # Label Optical System image
        self.label_opticalSys = QtWidgets.QLabel(self.scrollAreaWidgetContents_messages)
        self.label_opticalSys.setFont(font_semititle)
        self.label_opticalSys.setObjectName("label_opticalSys")
        self.gridLayout_messages.addWidget(self.label_opticalSys, 6, 0, 1, 1)

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_messages.addItem(spacerItem2, 2, 0, 1, 1)
        self.scrollArea_messages.setWidget(self.scrollAreaWidgetContents_messages)
        self.gridLayout_project.addWidget(self.scrollArea_messages, 0, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_project.addItem(spacerItem3, 0, 1, 1, 1)
        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # Matplotlib Scoll area Color palette
        #=======================================================================
        self.scrollArea_matplot = QtWidgets.QScrollArea(self.groupBox_project)
        self.scrollArea_matplot.setPalette(palette_matplotScroll)

        self.scrollArea_matplot.setWidgetResizable(True)
        self.scrollArea_matplot.setObjectName("scrollArea_matplot")
        self.scrollAreaWidgetContents_plots = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_plots.setGeometry(QtCore.QRect(0, 0, 444, 248))
        self.scrollAreaWidgetContents_plots.setObjectName("scrollAreaWidgetContents_plots")


        self.formLayout_4 = QtWidgets.QFormLayout(self.scrollAreaWidgetContents_plots)
        self.formLayout_4.setObjectName("formLayout_4")
        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #-----------------------------------------------------------------------
        # Tab Widget_plots
        #-----------------------------------------------------------------------
        self.tabWidget_plots = QtWidgets.QTabWidget(self.scrollAreaWidgetContents_plots)
        self.tabWidget_plots.setPalette(palette_TabPlots)
        self.tabWidget_plots.setObjectName("tabWidget_plots")
        self.tabWidget_plots.setMinimumHeight(2*self.rect.height()/3)
        self.tabWidget_plots.setFont(font_semititle)
        #_______________________________________________________________________


        #-----------------------------------------------------------------------
        # Tab Widget Plot Source
        #-----------------------------------------------------------------------
        self.tab_plotSource = QtWidgets.QWidget()
        self.tab_plotSource.setObjectName("tab_plotSource")

        self.gridLayout_tabPlotSource = QtWidgets.QGridLayout(self.tab_plotSource)
        self.gridLayout_tabPlotSource.setObjectName("gridLayout_5")

        # Plot Source
        self.scrollArea_plotSourceSDC = QtWidgets.QScrollArea(self.tab_plotSource)
        self.scrollArea_plotSourceSDC.setPalette(palette_scrollPlotSource)
        self.scrollArea_plotSourceSDC.setWidgetResizable(True)
        self.scrollArea_plotSourceSDC.setObjectName("scrollArea_plotSource")

        self.scrollAreaWidgetContents_plotSourceSDC = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_plotSourceSDC.setGeometry(QtCore.QRect(0, 0, 445, 1780))
        self.scrollAreaWidgetContents_plotSourceSDC.setObjectName("scrollAreaWidgetContents_plotSource")
        self.scrollAreaWidgetContents_plotSourceSDC.setMinimumWidth(1000)
        self.scrollAreaWidgetContents_plotSourceSDC.setMinimumHeight(1000)

        self.gridLayout_plotSourceSDC = QtWidgets.QGridLayout(self.scrollArea_plotSourceSDC)
        self.gridLayout_plotSourceSDC.setObjectName("gridLayout_plotSourceSDC")

        # plots
        self.canvas_plotSourceSDC = Canvas_source(self.scrollAreaWidgetContents_plotSourceSDC,self,1,"Spectral Degree of Coherence")
        self.canvas_plotSourceSDC.move(20,20)

        self.gridLayout_plotSourceSDC.addWidget(self.canvas_plotSourceSDC, 1, 0, 1, 1)

        self.gridLayout_tabPlotSource.addWidget(self.scrollArea_plotSourceSDC, 1, 0, 1, 1)



        """
        # Plot Source
        self.scrollArea_plotSourceSDC = QtWidgets.QScrollArea(self.tab_plotSource)
        self.scrollArea_plotSourceSDC.setPalette(palette_scrollPlotSource)
        self.scrollArea_plotSourceSDC.setWidgetResizable(True)
        self.scrollArea_plotSourceSDC.setObjectName("scrollArea_plotSource")



        # plots
        self.canvas_plotSourceSpec = Canvas_source(self.scrollArea_plotSourceSDC,self,3,"Spectral Degree of Coherence")
        self.canvas_plotSourceSpec.move(20,20)
        self.gridLayout_tabPlotSource.addWidget(self.scrollArea_plotSourceSDC, 3, 0, 1, 1)
        """

        self.tabWidget_plots.addTab(self.tab_plotSource, "Source")


        # prop
        self.tab_plotProp = QtWidgets.QWidget()
        self.tab_plotProp.setObjectName("tab_plotProp")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_plotProp)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.scrollArea_plotProp = QtWidgets.QScrollArea(self.tab_plotProp)

        # Scroll Area plot Propagation Color palette
        self.scrollArea_plotProp.setPalette(palette_scrollPlotProp)
        self.scrollArea_plotProp.setWidgetResizable(True)
        self.scrollArea_plotProp.setObjectName("scrollArea_plotProp")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 385, 86))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.scrollArea_plotProp.setWidget(self.scrollAreaWidgetContents_4)
        self.gridLayout_6.addWidget(self.scrollArea_plotProp, 0, 0, 1, 1)
        self.tabWidget_plots.addTab(self.tab_plotProp, "Propagation")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.tabWidget_plots)


        self.scrollArea_matplot.setWidget(self.scrollAreaWidgetContents_plots)
        self.gridLayout_project.addWidget(self.scrollArea_matplot, 1, 2, 1, 1)

        #_______________________________________________________________________


        #=======================================================================
        # Scroll Area Section Parameters
        #=======================================================================

        # Scroll Area section parameters
        self.scrollArea_sectionParams = QtWidgets.QScrollArea(self.groupBox_project)
        self.scrollArea_sectionParams.setPalette(palette_parSection)
        self.scrollArea_sectionParams.setWidgetResizable(True)
        self.scrollArea_sectionParams.setObjectName("scrollArea_sectionParams")
        self.scrollArea_sectionParams.setMaximumWidth(int(rect.width()/4))

        self.scrollAreaWidgetContents_numPlanes = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_numPlanes.setGeometry(QtCore.QRect(0, 0, 445, 1780))
        self.scrollAreaWidgetContents_numPlanes.setObjectName("scrollAreaWidgetContents_numPlanes")

        self.gridLayout_7 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_numPlanes)
        self.gridLayout_7.setObjectName("gridLayout_7")

        #self.scrollArea_sectionParams.verticalScrollBar().setStyleSheet(stylesheet)
        #_______________________________________________________________________


        #=======================================================================
        # Scroll Area Text Box
        #=======================================================================
        self.scrollArea_textBox = QtWidgets.QScrollArea(self.scrollAreaWidgetContents_numPlanes)
        self.scrollArea_textBox.setWidgetResizable(True)
        self.scrollArea_textBox.setObjectName("ScrollArea_textBox")
        self.scrollArea_textBox.setMinimumHeight(rect.height()/6.)

        self.scrollAreaWidgetContents_textBox = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_textBox.setGeometry(QtCore.QRect(0, 0, 421, 85))
        self.scrollAreaWidgetContents_textBox.setObjectName("scrollAreaWidgetContents_textBox")

        self.gridLayout_textBox = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_textBox)
        self.gridLayout_textBox.setObjectName("gridLayout_geometry")
        #_______________________________________________________________________


        #-----------------------------------------------------------------------
        # Text Box to Write
        #-----------------------------------------------------------------------
        # adding text box to write

        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents_textBox)

        # palette color
        self.plainTextEdit.setPalette(palette_textEdit)

        # font
        self.plainTextEdit.setFont(font_textBox)
        self.plainTextEdit.setObjectName("plainTextEdit")

        # grid
        self.gridLayout_textBox.addWidget(self.plainTextEdit, 1, 0, 1, 3)

        # adding space
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_textBox.addItem(spacerItem1, 1, 0, 1, 1)
        #_______________________________________________________________________


        #=======================================================================
        # Scroll Area Save
        #=======================================================================
        self.scrollArea_save = QtWidgets.QScrollArea(self.scrollAreaWidgetContents_numPlanes)
        self.scrollArea_save.setWidgetResizable(True)
        self.scrollArea_save.setObjectName("ScrollArea_save")
        self.scrollArea_save.setMinimumHeight(rect.height()/6.)

        self.scrollAreaWidgetContents_save = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_save.setGeometry(QtCore.QRect(0, 0, 421, 85))
        self.scrollAreaWidgetContents_save.setObjectName("scrollAreaWidgetContents_save")

        self.gridLayout_save = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_save)
        self.gridLayout_save.setObjectName("gridLayout_save")
        #_______________________________________________________________________


        #=======================================================================
        # Scroll Area Propagation Quantity
        #=======================================================================
        self.scrollArea_propQuantity = QtWidgets.QScrollArea(self.scrollAreaWidgetContents_numPlanes)
        self.scrollArea_propQuantity.setWidgetResizable(True)
        self.scrollArea_propQuantity.setObjectName("ScrollArea_cohModel")
        self.scrollArea_propQuantity.setMinimumHeight(rect.height()/6.)

        self.scrollAreaWidgetContents_propQuantity = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_propQuantity.setGeometry(QtCore.QRect(0, 0, 421, 85))
        self.scrollAreaWidgetContents_propQuantity.setObjectName("scrollAreaWidgetContents_propQuantity")

        self.gridLayout_propQuantity = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_propQuantity)
        self.gridLayout_propQuantity.setObjectName("gridLayout_propQuantity")
        #_______________________________________________________________________


        #=======================================================================
        # Scroll Area Spectrum Model
        #=======================================================================
        self.scrollArea_spectrumModel = QtWidgets.QScrollArea(self.scrollAreaWidgetContents_numPlanes)
        self.scrollArea_spectrumModel.setWidgetResizable(True)
        self.scrollArea_spectrumModel.setObjectName("ScrollArea_spectrumModel")
        self.scrollArea_spectrumModel.setMinimumHeight(rect.height()/6.)


        self.scrollAreaWidgetContents_spectrumModel = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_spectrumModel.setGeometry(QtCore.QRect(0, 0, 421, 85))
        self.scrollAreaWidgetContents_spectrumModel.setObjectName("scrollAreaWidgetContents_spectrumModel")

        self.gridLayout_specModel = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_spectrumModel)
        self.gridLayout_specModel.setObjectName("gridLayout")
        #_______________________________________________________________________


        #=======================================================================
        # Scroll Area Coherence Model
        #=======================================================================
        self.scrollArea_cohModel = QtWidgets.QScrollArea(self.scrollAreaWidgetContents_numPlanes)
        self.scrollArea_cohModel.setWidgetResizable(True)
        self.scrollArea_cohModel.setObjectName("ScrollArea_cohModel")
        self.scrollArea_cohModel.setMinimumHeight(rect.height()/6.)

        self.scrollAreaWidgetContents_cohModel = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_cohModel.setGeometry(QtCore.QRect(0, 0, 421, 85))
        self.scrollAreaWidgetContents_cohModel.setObjectName("scrollAreaWidgetContents_cohModel")

        self.gridLayout_cohModel = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_cohModel)
        self.gridLayout_cohModel.setObjectName("gridLayout_cohModel")
        #_______________________________________________________________________


        #=======================================================================
        # Scroll Area Geometries
        #=======================================================================
        self.scrollArea_geometry = QtWidgets.QScrollArea(self.scrollAreaWidgetContents_numPlanes)
        self.scrollArea_geometry.setWidgetResizable(True)
        self.scrollArea_geometry.setObjectName("ScrollArea_geometry")
        self.scrollArea_geometry.setMinimumHeight(rect.height()/6.)

        self.scrollAreaWidgetContents_geometry = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_geometry.setGeometry(QtCore.QRect(0, 0, 421, 85))
        self.scrollAreaWidgetContents_geometry.setObjectName("scrollAreaWidgetContents_geometry")

        self.gridLayout_geometry = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_geometry)
        self.gridLayout_geometry.setObjectName("gridLayout_geometry")
        #_______________________________________________________________________


        #=======================================================================
        # Tab and Scroll Area Propagation System
        #=======================================================================

        # Tab Propagation System
        self.tabWidget_propsystem = QtWidgets.QTabWidget(self.scrollAreaWidgetContents_numPlanes)
        self.tabWidget_propsystem.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget_propsystem.sizePolicy().hasHeightForWidth())
        self.tabWidget_propsystem.setSizePolicy(sizePolicy)
        self.tabWidget_propsystem.setPalette(palette_tabPropSys)
        self.tabWidget_propsystem.setFont(font_normalLabel)
        self.tabWidget_propsystem.setIconSize(QtCore.QSize(20, 20))
        self.tabWidget_propsystem.setObjectName("tabWidget_propsystem")

        # list of text browser for spatial resolutioon
        self.textBrowser_spatialRes_list = []

        # max number of propagation planes
        self.max_numPlanes = 3

        # List of Tab for propagation planes
        self.tab_planes_list      = []

        # list of layouts for tabs of propagations planes
        self.gridLayoutTab_list = []

        #-----------------------------------------------------------------------
        # Propagation Planes | area, widget contents and gridlayout
        #-----------------------------------------------------------------------
        # list of scroll Area of propagation planes
        self.scrollArea_propPlanes_list = []

        # list of scrollAreaWidgetContents of propagation planes
        self.scrollAreaWidgetContents_propPlanes_list = []

        # list of grid layouts for propagation planes
        self.gridLayout_propPlanes_list = []
        #_______________________________________________________________________

        #-----------------------------------------------------------------------
        # Pupil Function and Parameters | area, widget contents and gridlayout
        #-----------------------------------------------------------------------
        # list of scrollArea for Pupil functions and parameters
        self.scrollArea_pupil_list = []

        # list of scrollArea for Pupil functions and parameters
        self.scrollAreaWidgetContents_pupil_list = []

        # list of gridlayout for pupil functions and parameters
        self.gridLayout_pupil_list=[]
        #_______________________________________________________________________

        #-----------------------------------------------------------------------
        # Aberration Function and Parameters | area, widget contents and gridlayout
        #-----------------------------------------------------------------------
        # list of scrollArea for aberration functions and parameters
        self.scrollArea_lens_list = []

        # list of scroll area widgets contents for aberration functions
        self.scrollAreaWidgetContents_lens_list = []

        # list of gridlayout for aberration functions
        self.gridLayout_lens_list=[]
        #_______________________________________________________________________


        #=======================================================================
        # Spin Box
        #=======================================================================
        self.spinBox_numPlanes = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_numPlanes)
        self.spinBox_numPlanes.setObjectName("spinBox_numPlanes")
        self.spinBox_numPlanes.setFont(font_normalLabel)
        self.spinBox_numPlanes.setMinimum(1)
        self.spinBox_numPlanes.setMaximum(3)
        self.spinBox_numPlanes.setMaximumWidth(size_spinBox(self))
        self.gridLayout_7.addWidget(self.spinBox_numPlanes, 64, 1, 1, 1)
        self.spinBox_numPlanes.valueChanged.connect(self.update_numPlanes)
        #_______________________________________________________________________


        #=======================================================================
        # date time widget
        #=======================================================================
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.scrollAreaWidgetContents_numPlanes)
        self.dateTimeEdit.setFont(font_normalLabel)
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.gridLayout_7.addWidget(self.dateTimeEdit, 85, 0, 1, 2)
        self.dateTimeEdit.setMaximumWidth(size_schedule(self))
        self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())

        #_______________________________________________________________________


        #=======================================================================
        # Computational Variables
        #=======================================================================
        self.list_filesGeom = []
        self.list_filesCoh = []

        # directories
        self.dirName       = None # saved results directory
        self.dirSourceCSDM = None # directory with source CSDM

        # present time
        self.nowTime = datetime.now()

        # directory name
        self.saveDirName = None

        # minimum size for combo boxes
        self.minwidth_combo = rect.width()/7

        # max width size for combo boxes when VIEWING
        self.maxWidthView_combo = rect.width()/2

        #-----------------------------------------------------------------------
        # Spectrum Models and parameters | list, line Edit
        #-----------------------------------------------------------------------

        # Spectrum Models List ex: [ ["Gaussian", OBJECT] , ["Lorentzian, OBJECT] ]
        self.specModel_list = []

        # Spectrum Model Parameters ex: [ ["a"],["a","b"] ]
        self.specModelPar_list = []

        # Spectrum Model Line Edit Parameters
        self.specModel_lineEditParameters = []
        #_______________________________________________________________________

        #-----------------------------------------------------------------------
        # Geometry Models and parameters | list, line Edit
        #-----------------------------------------------------------------------
        self.geometryModelsFunc = []

        # Geometry Models List ex: [ ["Circle", OBJECT] , ["Rectangle", OBJECT] ]
        self.geometry_list = []

        # Geometry Model Parameters ex: [ ["a"],["a","b"] ]
        self.geometryPar_list = []

        # Geometry Line Edit Parameters  ex. [ OBJECT, OBJECT]
        self.geometry_lineEditParameters = []
        #_______________________________________________________________________


        #-----------------------------------------------------------------------
        # Coherence Models and parameters | list, line Edit
        #-----------------------------------------------------------------------
        # Coherence Models List ex: [ ["GSM", OBJECT] , ["GSM2", OBJECT] ]
        self.cohModel_list = []

        # Geometry Model Parameters ex: [ ["a"],["a","b"] ]
        self.cohModelPar_list = []

        # Geometry Line Edit Parameters  ex. [ OBJECT, OBJECT]
        self.cohModel_lineEditParameters = []
        #_______________________________________________________________________


        #-----------------------------------------------------------------------
        # Pupil Geometry  Function, Parameters and Line Edits
        #-----------------------------------------------------------------------

        # Pupil Geometry Models List
        self.pupilGeomFunc_list = []
        for i in range(0,self.max_numPlanes):
            self.pupilGeomFunc_list.append([])

        # Pupil Geometry Parameters Models List
        self.pupilGeomFuncPars_list = []
        for i in range(0,self.max_numPlanes):
            self.pupilGeomFuncPars_list.append([])

        # Pupil Geometry Line Edit Parameters  ex. [ OBJECT, OBJECT]
        self.pupilGeom_lineEditParameters = []
        for i in range(0,self.max_numPlanes):
            self.pupilGeom_lineEditParameters.append([])
        #_______________________________________________________________________

        #-----------------------------------------------------------------------
        # Aberration  Function, Parameters and Line Edits
        #-----------------------------------------------------------------------
        # Aberration Models List
        self.lensAberrationFunc_list = []
        for i in range(0,self.max_numPlanes):
            self.lensAberrationFunc_list.append([])

        # Aberration Parameters Models List
        self.lensAberrationPars_list = []
        for i in range(0,self.max_numPlanes):
            self.lensAberrationPars_list.append([])

        # Pupil Geometry Line Edit Parameters  ex. [ OBJECT, OBJECT]
        self.lensAberration_lineEditParameters = []
        for i in range(0,self.max_numPlanes):
            self.lensAberration_lineEditParameters.append([])
        #_______________________________________________________________________


        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # Labels
        #=======================================================================

        # just a bar
        self.bar = "------------------------------------------------"

        # label simulation name
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label.setFont(font_normalLabel)
        self.label.setObjectName("label")
        self.gridLayout_7.addWidget(self.label, 1, 0, 1, 1)

        # label computational parameters (title)
        self.label_comParams = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_comParams.setPalette(palette_titles)
        self.label_comParams.setFont(font_title)
        self.label_comParams.setAlignment(QtCore.Qt.AlignCenter)
        self.label_comParams.setObjectName("label_comParams")
        self.gridLayout_7.addWidget(self.label_comParams, 4, 0, 1, 2)

        # label platform
        self.label_platform = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_platform.setPalette(palette_parSection)
        self.label_platform.setFont(font_normalLabel)
        self.label_platform.setObjectName("label_platform")
        self.gridLayout_7.addWidget(self.label_platform, 8, 0, 1, 1)

        # label device
        self.label_device = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_device.setPalette(palette_parSection)
        self.label_device.setFont(font_normalLabel)
        self.label_device.setObjectName("label_device")
        self.gridLayout_7.addWidget(self.label_device, 9, 0, 1, 1)

        # save file
        self.label_saveFile = QtWidgets.QLabel(self.scrollAreaWidgetContents_save)
        self.label_saveFile.setFont(font_normalLabel)
        self.label_saveFile.setObjectName("label_saveFile")
        self.gridLayout_save.addWidget(self.label_saveFile, 1, 0, 1, 1)

        # Label N
        self.label_N = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_N.setFont(font_normalLabel)
        self.label_N.setObjectName("label_N")
        self.gridLayout_7.addWidget(self.label_N, 15, 0, 1, 1)

        # label Propagation Quantities (title)
        self.label_PropagationQuantities = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_PropagationQuantities.setPalette(palette_titles)
        self.label_PropagationQuantities.setFont(font_title)
        self.label_PropagationQuantities.setAlignment(QtCore.Qt.AlignCenter)
        self.label_PropagationQuantities.setObjectName("label_PropagationQuantities")
        self.gridLayout_7.addWidget(self.label_PropagationQuantities, 22, 0, 1, 2)

        # label Propagation Quantity
        self.label_propQuant = QtWidgets.QLabel(self.scrollAreaWidgetContents_propQuantity)
        self.label_propQuant.setPalette(palette_parSection)
        self.label_propQuant.setFont(font_normalLabel)
        self.label_propQuant.setObjectName("label_propQuant")
        self.gridLayout_propQuantity.addWidget(self.label_propQuant, 0, 0, 1, 1)

        # Label Spectrum Parameters (Title)
        self.label_SpectrumParameters = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_SpectrumParameters.setPalette(palette_titles)
        self.label_SpectrumParameters.setFont(font_title)
        self.label_SpectrumParameters.setAlignment(QtCore.Qt.AlignCenter)
        self.label_SpectrumParameters.setObjectName("label_SpectrumParameters")
        self.gridLayout_7.addWidget(self.label_SpectrumParameters, 32, 0, 1, 2)

        # label central frequency
        self.label_centralFreq = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_centralFreq.setFont(font_normalLabel)
        self.label_centralFreq.setObjectName("label_centralFreq")
        self.gridLayout_7.addWidget(self.label_centralFreq, 38, 0, 1, 1)

        # label_specType
        self.label_specType = QtWidgets.QLabel(self.scrollAreaWidgetContents_spectrumModel)
        self.label_specType.setPalette(palette_parSection)
        self.label_specType.setFont(font_normalLabel)
        self.label_specType.setObjectName("label_specType")
        self.gridLayout_specModel.addWidget(self.label_specType, 0, 0, 1, 1)
        # list of label parameters
        self.specModel_labelParameters = []

        # Label Source Parameters
        self.label_SourceParameters = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_SourceParameters.setPalette(palette_titles)
        self.label_SourceParameters.setFont(font_title)
        self.label_SourceParameters.setAlignment(QtCore.Qt.AlignCenter)
        self.label_SourceParameters.setObjectName("label_SourceParameters")
        self.gridLayout_7.addWidget(self.label_SourceParameters, 44, 0, 1, 2)

        # label source Resolution
        self.label_sourceRes = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_sourceRes.setPalette(palette_parSection)
        self.label_sourceRes.setFont(font_normalLabel)
        self.label_sourceRes.setObjectName("label_sourceRes")
        self.gridLayout_7.addWidget(self.label_sourceRes, 47, 0, 1, 1)

        # Label Geometry
        self.label_geometry = QtWidgets.QLabel(self.scrollAreaWidgetContents_geometry)
        self.label_geometry.setFont(font_normalLabel)
        self.label_geometry.setObjectName("label_geometry")
        self.gridLayout_geometry.addWidget(self.label_geometry, 0, 0, 1, 1)
        # list of label parameters
        self.geometry_labelParameters = []

        # label coherence model
        self.label_cohModel = QtWidgets.QLabel(self.scrollAreaWidgetContents_cohModel)
        self.label_cohModel.setPalette(palette_parSection)
        self.label_cohModel.setFont(font_normalLabel)
        self.label_cohModel.setObjectName("label_cohModel")
        self.gridLayout_cohModel.addWidget(self.label_cohModel, 0, 0, 1, 1)
        self.cohModel_labelParameters = []

        # label Propgation System
        self.label_PropgationSystem = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_PropgationSystem.setPalette(palette_titles)
        self.label_PropgationSystem.setFont(font_title)
        self.label_PropgationSystem.setAlignment(QtCore.Qt.AlignCenter)
        self.label_PropgationSystem.setObjectName("label_PropgationSystem")
        self.gridLayout_7.addWidget(self.label_PropgationSystem, 61, 0, 1, 2)

        # label_numPlanes
        self.label_numPlanes = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_numPlanes.setPalette(palette_parSection)
        self.label_numPlanes.setFont(font_normalLabel)
        self.label_numPlanes.setObjectName("label_numPlanes")
        self.gridLayout_7.addWidget(self.label_numPlanes, 64, 0, 1, 1)

        # labels for distances of planes
        self.label_distances_list = []

        # labels pupil geometric model
        self.label_pupilGeom_list = []

        # labels pupil geometric model
        self.pupilGeom_labelParameters = []
        for i in range(0,self.max_numPlanes):
            self.pupilGeom_labelParameters.append([])

        # labels for focal length
        self.label_focalLength_list = []

        # labels for aberration function
        self.label_aberrationFunc_list = []

        # labels pupil geometric model
        self.aberrationFunc_labelParameters = []
        for i in range(0,self.max_numPlanes):
            self.aberrationFunc_labelParameters.append([])

        # label Start Simulation
        self.label_startSim = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_startSim.setPalette(palette_titles)
        self.label_startSim.setFont(font_title)
        self.label_startSim.setAlignment(QtCore.Qt.AlignCenter)
        self.label_startSim.setObjectName("label_2")
        self.gridLayout_7.addWidget(self.label_startSim, 74, 0, 1, 2)

        # Label Insert Comments
        self.label_insertComments = QtWidgets.QLabel(self.scrollAreaWidgetContents_textBox)
        self.label_insertComments.setFont(font_normalLabel)
        self.label_insertComments.setObjectName("label_insertComments")
        self.gridLayout_textBox.addWidget(self.label_insertComments, 0, 0, 1, 1)

        # Label Output Messages
        self.label_outMessages = QtWidgets.QLabel(self.scrollAreaWidgetContents_messages)
        self.label_outMessages.setFont(font_semititle)
        self.label_outMessages.setObjectName("label_outMessages")
        self.gridLayout_messages.addWidget(self.label_outMessages, 0, 0, 1, 1)

        # Label Plot
        self.label_Plots = QtWidgets.QLabel(self.scrollAreaWidgetContents_plots)
        self.label_Plots.setPalette(palette_titles)
        self.label_Plots.setFont(font_title)
        self.label_Plots.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Plots.setObjectName("label_Plots")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_Plots)

        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # Lines
        #=======================================================================

        # horizontal line computation parameters 1
        self.line_comPar1 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_comPar1.setLineWidth(2)
        self.line_comPar1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_comPar1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_comPar1.setObjectName("line_comPar1")
        self.line_comPar1.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_comPar1, 3, 0, 1, 3)

        # horizontal line computation parameters 2
        self.line_compPar2 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_compPar2.setLineWidth(2)
        self.line_compPar2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_compPar2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_compPar2.setObjectName("line_compPar2")
        self.line_compPar2.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_compPar2, 5, 0, 1, 3)

        # Horizontal Line propagation quantities 1
        self.line_propQuant1 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_propQuant1.setLineWidth(2)
        self.line_propQuant1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_propQuant1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_propQuant1.setObjectName("line_propQuant1")
        self.line_propQuant1.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_propQuant1, 19, 0, 1, 3)

        # horizontal line propagation quantity 2
        self.line_propQuant2 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_propQuant2.setLineWidth(2)
        self.line_propQuant2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_propQuant2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_propQuant2.setObjectName("line_propQuant2")
        self.line_propQuant2.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_propQuant2, 24, 0, 1, 3)

        # horizontal line spectral parameters 1
        self.line_specPar1 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_specPar1.setLineWidth(2)
        self.line_specPar1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_specPar1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_specPar1.setObjectName("line_specPar1")
        self.line_specPar1.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_specPar1, 30, 0, 1, 3)

        # horizontal line spectral parameters 2
        self.line_specPar2 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_specPar2.setLineWidth(2)
        self.line_specPar2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_specPar2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_specPar2.setObjectName("line_specPar2")
        self.line_specPar2.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_specPar2, 33, 0, 1, 3)

        # horizontal line source parameter2 1
        self.line_sourcePar1 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_sourcePar1.setLineWidth(2)
        self.line_sourcePar1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_sourcePar1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_sourcePar1.setObjectName("line_sourcePar1")
        self.line_sourcePar1.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_sourcePar1, 43, 0, 1, 3)

        # Horizontal Line source parameters 2
        self.line_sourcePar2 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_sourcePar2.setLineWidth(2)
        self.line_sourcePar2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_sourcePar2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_sourcePar2.setObjectName("line_sourcePar2")
        self.line_sourcePar2.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_sourcePar2, 45, 0, 1, 3)

        # horizontal line propagation system 1
        self.line_propSys1 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_propSys1.setLineWidth(2)
        self.line_propSys1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_propSys1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_propSys1.setObjectName("line_propSys1")
        self.line_propSys1.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_propSys1, 60, 0, 1, 3)

        # Horizontal line propagation system 2
        self.line_propSys2 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_propSys2.setLineWidth(2)
        self.line_propSys2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_propSys2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_propSys2.setObjectName("line_propSys2")
        self.line_propSys2.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_propSys2, 62, 0, 1, 3)

        # horizontal line start sim 1
        self.line = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line_startSim1")
        self.line.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line, 73, 0, 1, 3)

        # horizontal line start sim 2
        self.line_2 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_startSim2")
        self.line_2.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_2, 75, 0, 1, 3)

        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # Spaces
        #=======================================================================

        # space 4
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem4, 52, 0, 1, 2)

        # space 5
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem5, 53, 0, 1, 2)

        # space 6
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem6, 63, 0, 1, 2)

        # space 9
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem9, 17, 0, 1, 2)

        # space 10
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem10, 28, 0, 1, 2)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem11, 18, 0, 1, 2)

        # space 12
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem12, 46, 0, 1, 2)

        # space 13
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem13, 10, 0, 1, 2)

        # space 14
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem14, 1, 0, 1, 2)

        # space 15
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem15, 76, 0, 1, 2)

        # space 16
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem16, 29, 0, 1, 2)

        # space 17
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem17, 34, 0, 1, 2)

        # space 18
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem18, 6, 0, 1, 2)

        # space 19
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem19, 72, 0, 1, 2)

        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # Line Edit Text
        #=======================================================================

        # line edit Simulation Name
        self.lineEdit_simName = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_numPlanes)
        self.lineEdit_simName.setFont(font_normalLabel)
        self.lineEdit_simName.setObjectName("lineEdit_2")
        self.lineEdit_simName.setStyleSheet('background: '+colortxt_textEdit)
        self.gridLayout_7.addWidget(self.lineEdit_simName, 1, 1, 1, 1)
        # setting size
        self.lineEdit_simName.setMaximumWidth(self.minwidth_combo)
        #self.lineEdit_simName.actionEvent()
        self.lineEdit_simName.textChanged.connect(self.update_titleProject)

        # line Save file txt
        self.lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_save)
        self.lineEdit.setFont(font_normalLabel)
        self.lineEdit.setObjectName("Save File")
        self.lineEdit.setStyleSheet('background: '+colortxt_textEdit)
        self.gridLayout_save.addWidget(self.lineEdit, 1, 1, 1, 1)
        results_directory = str(current_dir)+'\\results'
        self.saveDirName = results_directory
        self.lineEdit.setText(results_directory)
        # start at the line 0:
        self.lineEdit.setCursorPosition(0)
        # setting size
        self.lineEdit.setMaximumWidth(self.minwidth_combo)

        # line open NPY source
        self.lineEdit_dirNPY = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_numPlanes)
        self.lineEdit_dirNPY.setFont(font_normalLabel)
        self.lineEdit_dirNPY.setObjectName("Save File")
        self.lineEdit_dirNPY.setStyleSheet('background: '+colortxt_textEdit)
        self.gridLayout_7.addWidget(self.lineEdit_dirNPY, 48, 1, 1, 1)
        self.lineEdit_dirNPY.setText(results_directory)
        # start at the line 0:
        self.lineEdit_dirNPY.setCursorPosition(0)
        # setting size
        self.lineEdit_dirNPY.setMaximumWidth(self.minwidth_combo)

        # text edit in N
        self.lineEdit_N = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_numPlanes)
        self.lineEdit_N.setFont(font_normalLabel)
        self.lineEdit_N.setObjectName("lineEdit_N")
        self.lineEdit_N.setStyleSheet('background: '+colortxt_textEdit)
        self.gridLayout_7.addWidget(self.lineEdit_N, 15, 1, 1, 1)
        self.lineEdit_N.setMaximumWidth(size_entries(self))
        self.lineEdit_N.textChanged.connect(self.updateSpaceRes)
        self.lineEdit_N.setText("150")

        # line edit Central Frequency
        self.lineEdit_centralFreq = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_numPlanes)
        self.lineEdit_centralFreq.setObjectName("lineEdit_centralFreq")
        self.lineEdit_centralFreq.setStyleSheet('background: '+colortxt_textEdit)
        self.gridLayout_7.addWidget(self.lineEdit_centralFreq, 38, 1, 1, 1)
        # setting size
        self.lineEdit_centralFreq.setFont(font_normalLabel)
        self.lineEdit_centralFreq.textChanged.connect(self.updateSpaceRes)
        self.lineEdit_centralFreq.setText("3.887e15")
        self.lineEdit_centralFreq.setMaximumWidth(size_entries(self))

        # line edit text source resolution
        self.lineEdit_souceRes = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_numPlanes)
        self.lineEdit_souceRes.setFont(font_normalLabel)
        self.lineEdit_souceRes.setObjectName("lineEdit_souceRes")
        self.lineEdit_souceRes.setStyleSheet('background: '+colortxt_textEdit)
        self.gridLayout_7.addWidget(self.lineEdit_souceRes, 47, 1, 1, 1)
        # setting size
        self.lineEdit_souceRes.textChanged.connect(self.updateSpaceRes)
        self.lineEdit_souceRes.setText("1e-3")
        self.lineEdit_souceRes.setMaximumWidth(size_entries(self))

        # line edit text distance for propagation planes
        self.lineEdit_distances_list = []

        # line edit text focal length for propagation planes
        self.lineEdit_focalLength_list = []

        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # Combo Boxes
        #=======================================================================

        # combo box platform
        self.comboBox_platform = QtWidgets.QComboBox(self.scrollAreaWidgetContents_numPlanes)
        self.comboBox_platform.setFont(font_normalLabel)
        self.comboBox_platform.setObjectName("comboBox_platform")
        self.gridLayout_7.addWidget(self.comboBox_platform, 8, 1, 1, 1)
        # filling combo box

        # get platforms and devices
        temp = getPlatformsDevices()
        self.platform_choices = temp[0]
        self.list_platforms   = temp[1]
        self.device_choices   = temp[2]

        for i in range(0,len(self.list_platforms)):
            self.comboBox_platform.addItem(str(self.list_platforms[i]),self.platform_choices[str(self.list_platforms[i])])
        # setting size
        self.comboBox_platform.setMaximumWidth(self.minwidth_combo)
        self.comboBox_platform.setStyleSheet('''*
        QComboBox QAbstractItemView
            {
            min-width: '''+str(self.maxWidthView_combo)+'''px;
            }
        ''')

        # combo box device
        self.comboBox_device = QtWidgets.QComboBox(self.scrollAreaWidgetContents_numPlanes)
        self.comboBox_device.setFont(font_normalLabel)
        self.comboBox_device.setObjectName("comboBox_device")
        self.gridLayout_7.addWidget(self.comboBox_device, 9, 1, 1, 1)
        self.update_devices()
        self.comboBox_platform.currentIndexChanged.connect(self.update_devices)
        # setting size
        self.comboBox_device.setMaximumWidth(self.minwidth_combo)
        self.comboBox_device.setStyleSheet('''*
        QComboBox QAbstractItemView
            {
            min-width: '''+str(self.maxWidthView_combo)+'''px;
            }
        ''')

        # combo box propagation quantities
        self.comboBox_propQuant = QtWidgets.QComboBox(self.scrollAreaWidgetContents_propQuantity)
        self.comboBox_propQuant.setFont(font_normalLabel)
        self.comboBox_propQuant.setObjectName("comboBox_propQuant")
        self.gridLayout_propQuantity.addWidget(self.comboBox_propQuant, 0, 1, 1, 1)
        self.comboBox_propQuant.addItem("Degree of coherence",1)
        self.comboBox_propQuant.addItem("Spectrum",2)
        # setting size
        self.comboBox_propQuant.setMaximumWidth(self.minwidth_combo)
        self.comboBox_propQuant.setStyleSheet('''*
        QComboBox QAbstractItemView
            {
            min-width: '''+str(self.maxWidthView_combo)+'''px;
            }
        ''')
        self.comboBox_propQuant.currentIndexChanged.connect(self.updatePropQuantity)

        # combo box spectral model
        self.comboBox_specType = QtWidgets.QComboBox(self.scrollAreaWidgetContents_spectrumModel)
        self.comboBox_specType.setFont(font_normalLabel)
        self.comboBox_specType.setObjectName("comboBox_specType")
        self.gridLayout_specModel.addWidget(self.comboBox_specType, 0, 1, 1, 1)
        # setting size
        self.comboBox_specType.setMaximumWidth(self.minwidth_combo)
        self.comboBox_specType.setStyleSheet('''*
        QComboBox QAbstractItemView
            {
            min-width: '''+str(self.maxWidthView_combo)+'''px;
            }
        ''')
        # action
        self.comboBox_specType.currentIndexChanged.connect(self.updateSpecModelPars)

        # combo box coherence model
        self.comboBox_cohModel = QtWidgets.QComboBox(self.scrollAreaWidgetContents_cohModel)
        self.comboBox_cohModel.setFont(font_normalLabel)
        self.comboBox_cohModel.setObjectName("comboBox_cohModel")
        self.gridLayout_cohModel.addWidget(self.comboBox_cohModel, 0, 1, 1, 1)
        # setting size
        self.comboBox_cohModel.setMaximumWidth(self.minwidth_combo)
        self.comboBox_cohModel.setStyleSheet('''*
        QComboBox QAbstractItemView
            {
            min-width: '''+str(self.maxWidthView_combo)+'''px;
            }
        ''')
        self.comboBox_cohModel.currentIndexChanged.connect(self.updateCohModelPars)

        # combo box geometry
        self.comboBox_geometry = QtWidgets.QComboBox(self.scrollAreaWidgetContents_geometry)
        self.comboBox_geometry.setFont(font_normalLabel)
        self.comboBox_geometry.setObjectName("comboBox_geometry")
        self.gridLayout_geometry.addWidget(self.comboBox_geometry, 0, 1, 1, 1)
        # setting size
        self.comboBox_geometry.setMaximumWidth(self.minwidth_combo)
        self.comboBox_geometry.setStyleSheet('''*
        QComboBox QAbstractItemView
            {
            min-width: '''+str(self.maxWidthView_combo)+'''px;
            }
        ''')
        # action
        self.comboBox_geometry.currentIndexChanged.connect(self.updateGeometryPars)


        # list of comboBoxes with pupil functions for propagation planes
        self.comboBox_pupilGeom_list = []

        # list of comboBoxes with aberration functions for propagation planes
        self.comboBox_aberrationFunc_list = []
        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------

        #=======================================================================
        # Check Boxes
        #=======================================================================

        # check box PyOpenCL
        self.checkBox_pyopencl = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_numPlanes)
        self.checkBox_pyopencl.setPalette(palette_parSection)
        self.checkBox_pyopencl.setFont(font_normalLabel)
        self.checkBox_pyopencl.setObjectName("checkBox_pyopencl")
        self.gridLayout_7.addWidget(self.checkBox_pyopencl, 7, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem7, 41, 0, 1, 2)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem8, 2, 0, 1, 2)
        # setting checked by default
        self.checkBox_pyopencl.setChecked(True)

        # checkbox save
        self.checkBox_save = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_save)
        self.checkBox_save.setFont(font_normalLabel)
        self.checkBox_save.setObjectName("checkBox_save")
        self.gridLayout_save.addWidget(self.checkBox_save, 0, 0, 1, 1)
        self.checkBox_save.setChecked(False)

        # checkbox save source CSDM
        self.checkBox_saveSourceCSDM = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_save)
        self.checkBox_saveSourceCSDM.setFont(font_normalLabel)
        self.checkBox_saveSourceCSDM.setObjectName("checkBox_saveSourceCSDM")
        self.gridLayout_save.addWidget(self.checkBox_saveSourceCSDM, 2, 0, 1, 1)

        # checkbox save source CSDM
        self.checkBox_savePropCSDM = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_save)
        self.checkBox_savePropCSDM.setFont(font_normalLabel)
        self.checkBox_savePropCSDM.setObjectName("checkBox_saveSourceCSDM")
        self.gridLayout_save.addWidget(self.checkBox_savePropCSDM, 3, 0, 1, 1)

        # checkBox_sourcefromfile Color palette
        self.checkBox_sourcefromfile = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_numPlanes)
        self.checkBox_sourcefromfile.setPalette(palette_parSection)
        self.checkBox_sourcefromfile.setFont(font_normalLabel)
        self.checkBox_sourcefromfile.setObjectName("checkBox_sourcefromfile")
        self.gridLayout_7.addWidget(self.checkBox_sourcefromfile, 48, 0, 1, 1)
        self.checkBox_sourcefromfile.stateChanged.connect(self.updateFomFile)

        # checkbox debug
        self.checkBox_debug = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_numPlanes)
        self.checkBox_debug.setPalette(palette_parSection)
        self.checkBox_debug.setFont(font_normalLabel)
        self.checkBox_debug.setObjectName("checkBox_debug")
        self.gridLayout_7.addWidget(self.checkBox_debug, 14, 0, 1, 1)

        # checkbox freq dependent
        self.checkBox_freqDep = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_propQuantity)
        self.checkBox_freqDep.setPalette(palette_parSection)
        self.checkBox_freqDep.setFont(font_normalLabel)
        self.checkBox_freqDep.setObjectName("checkBox_freqDep")
        self.gridLayout_propQuantity.addWidget(self.checkBox_freqDep, 2, 0, 1, 3)
        self.checkBox_freqDep.setChecked(True)


        # CheckBox for far-field of planes
        self.checkBox_farfied_list = []

        # CheckBox for Pupil
        self.checkBox_pupil_list = []

        # CheckBox for lens of planes
        self.checkBox_lens_list = []

        # CheckBox for lens of planes
        self.checkBox_aberration_list = []

        # checkbox schedule simulation
        self.checkBox_schedule = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_numPlanes)
        self.checkBox_schedule.setFont(font_normalLabel)
        self.checkBox_schedule.setObjectName("checkBox")
        self.gridLayout_7.addWidget(self.checkBox_schedule, 84, 0, 1, 2)

        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # Radio buttons
        #=======================================================================

        """
        # propagation quantity
        self.radio_propQuantityPars1 = QtWidgets.QRadioButton(self.scrollAreaWidgetContents_propQuantity))
        self.radio_propQuantityPars1.setFont(font_normalLabel)
        self.radio_propQuantityPars1.setObjectName("radioButton_")
        self.gridLayout_propQuantity.addWidget(self.radioButton_quasi, 0, 0, 1, 1)
        """


        # Radio Buttons
        self.radioButton_quasi = QtWidgets.QRadioButton(self.scrollAreaWidgetContents_numPlanes)
        self.radioButton_quasi.setFont(font_normalLabel)
        self.radioButton_quasi.setObjectName("radioButton_quasi")
        self.gridLayout_7.addWidget(self.radioButton_quasi, 36, 0, 1, 1)
        self.radioButton_quasi.toggled.connect(self.update_specPars)

        # radio button
        self.radioButton_poly = QtWidgets.QRadioButton(self.scrollAreaWidgetContents_numPlanes)
        self.radioButton_poly.setFont(font_normalLabel)
        self.radioButton_poly.setObjectName("radioButton_2")
        self.gridLayout_7.addWidget(self.radioButton_poly, 37, 0, 1, 1)
        self.radioButton_poly.toggled.connect(self.update_specPars)

        # 1 frequency, quasi-monochomatic, polychromatic
        self.radioButton_1freq = QtWidgets.QRadioButton(self.scrollAreaWidgetContents_numPlanes)
        self.radioButton_1freq.setFont(font_normalLabel)
        self.radioButton_1freq.setObjectName("radioButton_1freq")
        self.gridLayout_7.addWidget(self.radioButton_1freq, 35, 0, 1, 1)
        self.radioButton_1freq.toggled.connect(self.update_specPars)
        self.radioButton_1freq.setChecked(True)

        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------

        #=======================================================================
        # Tool buttons
        #=======================================================================

        # tool button save file
        self.toolButton_saveFile = QtWidgets.QToolButton(self.scrollAreaWidgetContents_save)
        self.toolButton_saveFile.setFont(font_normalLabel)
        self.toolButton_saveFile.setObjectName("toolButton_saveFile")
        self.gridLayout_save.addWidget(self.toolButton_saveFile, 1, 2, 1, 1)
        # action
        self.toolButton_saveFile.clicked.connect(self.openFileNameDialog_saveDir)

        # tool button source file
        self.toolButton_sourcefromfile = QtWidgets.QToolButton(self.scrollAreaWidgetContents_numPlanes)
        self.toolButton_sourcefromfile.setFont(font_normalLabel)
        self.toolButton_sourcefromfile.setObjectName("toolButton_sourcefromfile")
        self.gridLayout_7.addWidget(self.toolButton_sourcefromfile, 48, 2, 1, 1)
        self.toolButton_sourcefromfile.clicked.connect(self.openFileNameDialog_openCSDM)

        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------

        #=======================================================================
        # Push buttons
        #=======================================================================

        # Button Start
        self.pushButton_start = QtWidgets.QPushButton(self.scrollAreaWidgetContents_numPlanes)
        self.pushButton_start.setPalette(palette_buttonStart)
        self.pushButton_start.setFont(font_button)
        self.pushButton_start.setObjectName("pushButton_start")
        self.gridLayout_7.addWidget(self.pushButton_start, 83, 0, 1, 3,alignment=QtCore.Qt.AlignCenter)
        self.pushButton_start.setMinimumWidth(self.rect.width()/8)
        self.pushButton_start.clicked.connect(self.start_simulation)


        # Update button
        self.pushButton_updatePlots = QtWidgets.QPushButton(self.scrollAreaWidgetContents_plots)
        self.pushButton_updatePlots.setFont(font_button)
        self.pushButton_updatePlots.setObjectName("pushButton_updatePlots")
        #self.pushButton_updatePlots.setMinimumWidth(self.rect.width()/8)
        self.pushButton_updatePlots.setMaximumWidth(self.rect.width()/8)
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.pushButton_updatePlots)

        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------

        # textBox
        self.scrollArea_textBox.setWidget(self.scrollAreaWidgetContents_textBox)
        self.gridLayout_7.addWidget(self.scrollArea_textBox,0, 0, 1, 2)

        # Save
        self.scrollArea_save.setWidget(self.scrollAreaWidgetContents_save)
        self.gridLayout_7.addWidget(self.scrollArea_save,11, 0, 1, 2)

        # Propagation quantity
        self.scrollArea_propQuantity.setWidget(self.scrollAreaWidgetContents_propQuantity)
        self.gridLayout_7.addWidget(self.scrollArea_propQuantity,25, 0, 1, 2)

        # Geometry Model
        self.scrollArea_geometry.setWidget(self.scrollAreaWidgetContents_geometry)
        self.gridLayout_7.addWidget(self.scrollArea_geometry,49, 0, 1, 2)

        # Coherence Model
        self.scrollArea_cohModel.setWidget(self.scrollAreaWidgetContents_cohModel)
        self.gridLayout_7.addWidget(self.scrollArea_cohModel,51, 0, 1, 2)

        # Spectrum Model
        self.scrollArea_spectrumModel.setWidget(self.scrollAreaWidgetContents_spectrumModel)
        self.gridLayout_7.addWidget(self.scrollArea_spectrumModel,39, 0, 1, 2)

        self.scrollArea_sectionParams.setWidget(self.scrollAreaWidgetContents_numPlanes)
        self.gridLayout_project.addWidget(self.scrollArea_sectionParams, 0, 0, 2, 2)

        self.gridLayout_main_project.addLayout(self.gridLayout_project, 0, 0, 1, 1)
        self.gridLayout_main.addWidget(self.groupBox_project, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1017, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.actionNew_Project = QtWidgets.QAction(MainWindow)
        self.actionNew_Project.setObjectName("actionNew_Project")
        self.actionLoad_Project = QtWidgets.QAction(MainWindow)
        self.actionLoad_Project.setObjectName("actionLoad_Project")
        self.actionSave_Project = QtWidgets.QAction(MainWindow)
        self.actionSave_Project.setObjectName("actionSave_Project")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtWidgets.QAction(MainWindow)
        self.actionRedo.setObjectName("actionRedo")
        self.actionCut = QtWidgets.QAction(MainWindow)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionDelete = QtWidgets.QAction(MainWindow)
        self.actionDelete.setObjectName("actionDelete")
        self.actionManual = QtWidgets.QAction(MainWindow)
        self.actionManual.setObjectName("actionManual")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionGet_Citation = QtWidgets.QAction(MainWindow)
        self.actionGet_Citation.setObjectName("actionGet_Citation")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionExport_Data = QtWidgets.QAction(MainWindow)
        self.actionExport_Data.setObjectName("actionExport_Data")
        self.menuFile.addAction(self.actionNew_Project)
        self.menuFile.addAction(self.actionLoad_Project)
        self.menuFile.addAction(self.actionSave_Project)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport_Data)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionDelete)
        self.menuHelp.addAction(self.actionManual)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionGet_Citation)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        # last functions:
        self.retranslateUi(MainWindow)
        self.tabWidget_plots.setCurrentIndex(0)
        self.tabWidget_propsystem.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)




    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", appname))
        self.groupBox_project.setTitle(_translate("MainWindow", "New Project"))
        self.label_insertComments.setText(_translate("MainWindow", "Insert Comments: "))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "# Write your comments here. They are saved after the simulation\n"""))

        """
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">« PyWolf version 1.0 »</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        """
        self.label_outMessages.setText(_translate("MainWindow", "Output Messages:"))
        self.label_opticalSys.setText(_translate("MainWindow", "Optical System:"))
        self.label_Plots.setText(_translate("MainWindow", "Plots"))
        self.pushButton_updatePlots.setText(_translate("MainWindow", "Update"))
        self.tabWidget_plots.setTabText(self.tabWidget_plots.indexOf(self.tab_plotSource), _translate("MainWindow", "Source"))
        self.tabWidget_plots.setTabText(self.tabWidget_plots.indexOf(self.tab_plotProp), _translate("MainWindow", "Propagation"))
        self.radioButton_quasi.setText(_translate("MainWindow", "Quasi-monochromatic"))
        self.label_N.setText(_translate("MainWindow", "Matrix size N:"))
        self.pushButton_start.setText(_translate("MainWindow", "Start Simulation"))
        self.checkBox_save.setText(_translate("MainWindow", "Save Results"))
        self.checkBox_saveSourceCSDM.setText(_translate("MainWindow", "Save Source Matrix"))
        self.checkBox_savePropCSDM.setText(_translate("MainWindow", "Save Propagation Matrix"))
        self.label_geometry.setText(_translate("MainWindow", "Geometry:"))
        self.label_SpectrumParameters.setText(_translate("MainWindow", "Spectrum Parameters"))
        self.label.setText(_translate("MainWindow", "Simulation Name: "))
        self.checkBox_schedule.setText(_translate("MainWindow", "Scheldule Simulation"))
        self.radioButton_poly.setText(_translate("MainWindow", "Polychromatic"))
        self.label_SourceParameters.setText(_translate("MainWindow", "Source Parameters"))
        self.label_specType.setText(_translate("MainWindow", "Spectrum model:"))
        self.checkBox_debug.setText(_translate("MainWindow", "Debug"))
        self.checkBox_pyopencl.setText(_translate("MainWindow", "Use PyOpenCL"))
        self.label_startSim.setText(_translate("MainWindow", "Start Simulation"))
        self.label_PropgationSystem.setText(_translate("MainWindow", "Propagation System"))
        self.label_device.setText(_translate("MainWindow", "Device:"))
        self.label_cohModel.setText(_translate("MainWindow", "Coherence Model:"))
        self.label_PropagationQuantities.setText(_translate("MainWindow", "Propagation Quantities"))
        self.label_saveFile.setText(_translate("MainWindow", "Save File:"))
        self.label_numPlanes.setText(_translate("MainWindow", "Number of Propagation Planes:"))
        self.label_platform.setText(_translate("MainWindow", "Platform:"))
        self.toolButton_sourcefromfile.setText(_translate("MainWindow", "..."))
        self.radioButton_1freq.setText(_translate("MainWindow", "One Frequency"))
        self.lineEdit_simName.setText(_translate("MainWindow", "New Project"))
        self.label_sourceRes.setText(_translate("MainWindow", "Source Spatial Resolution (m):"))
        self.label_comParams.setText(_translate("MainWindow", "Options"))
        self.checkBox_sourcefromfile.setText(_translate("MainWindow", "From File"))
        self.label_propQuant.setText(_translate("MainWindow", "Propagation Quantity:"))
        self.toolButton_saveFile.setText(_translate("MainWindow", "..."))
        self.label_centralFreq.setText(_translate("MainWindow", "Angular Frequency (rad/s):"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionNew_Project.setText(_translate("MainWindow", "New Project"))
        self.actionLoad_Project.setText(_translate("MainWindow", "Load Project"))
        self.actionSave_Project.setText(_translate("MainWindow", "Save Project"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionUndo.setText(_translate("MainWindow", "Undo"))
        self.actionRedo.setText(_translate("MainWindow", "Redo"))
        self.actionCut.setText(_translate("MainWindow", "Cut"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.actionManual.setText(_translate("MainWindow", "Manual"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionGet_Citation.setText(_translate("MainWindow", "Get Citation"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionExport_Data.setText(_translate("MainWindow", "Export Results"))

        # initial running functions
        self.showRAM()
        self.search_specModel()
        self.search_cohModel()
        self.search_geometry()
        self.update_specPars()
        self.update_numPlanes()
        self.updatePropPlanePars()
        self.update_numPlanes()
        self.update_lensPars()
        self.searchPupilGeom()
        self.updatePupilArea()
        self.updatePupilGeomPars()

        self.searchAberrationFunc()
        self.updateAberrationFuncPars()
        self.updatePropQuantity()

    def update_devices(self):
        update_devices2(self)

    def update_outputText(self,text):
        "Updates the Output Message box in the application"
        self.textBrowser.append("\n"+self.give_time()+"  | >> "+str(text))
        self.textBrowser.update()
        self.textBrowser.moveCursor(QtGui.QTextCursor.End)
        QtWidgets.qApp.processEvents()

    def update_outputTextSameLine(self,text):
        "Updates the Output Message box in the application in the same previous line"
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        cursor.removeSelectedText()
        cursor.movePosition(QtGui.QTextCursor.StartOfLine)
        cursor.insertText(str(text))
        QtWidgets.qApp.processEvents()

    def give_time(self):
        "returns the currente date and time"
        self.nowTime = datetime.now()
        day_time = self.nowTime.strftime("%d/%m/%Y %H:%M:%S")
        new_txt = "["+str(day_time)+"]"
        return new_txt

    def show_citation(self):
        mydialog = QDialog()
        mydialog.setModal(True)
        mydialog.exec()

    def openFileNameDialog_saveDir(self):
        openFileNameDialog_saveDir2(self)

    def openFileNameDialog_openCSDM(self):
        openFileNameDialog_openCSDM2(self)

    def showRAM(self):
        showRAM2(self)

    def addTime(self):
        addTime2(self)

    def search_specModel(self):
        search_specModel2(self)

    def updateSpecModelPars(self):
        updateSpecModelPars2(self)

    def add_labelsText(self,label,text):
        _translate = QtCore.QCoreApplication.translate
        label.setText(_translate("MainWindow", text))

    def clear_LabelText(self,label):
        label.clear()

    def search_geometry(self):
        search_geometry2(self)

    def updateGeometryPars(self):
        updateGeometryPars2(self)

    def search_cohModel(self):
        search_cohModel2(self)

    def updateCohModelPars(self):
        updateCohModelPars2(self)

    def update_titleProject(self):
        update_titleProject2(self)

    def update_specPars(self):
        update_specPars2(self)

    def update_numPlanes(self):
        update_numPlanes2(self)

    def updatePropPlanePars(self):
        updatePropPlanePars2(self)

    def update_lensPars(self):
        update_lensPars2(self)

    def updateSpaceRes(self):
        updateSpaceRes2(self)

    def updatePupilArea(self):
        updatePupilArea2(self)

    def searchPupilGeom(self):
        searchPupilGeom2(self)

    def updatePupilGeomPars(self):
        updatePupilGeomPars2(self)

    def searchAberrationFunc(self):
        searchAberrationFunc2(self)

    def updateAberrationFuncPars(self):
        updateAberrationFuncPars2(self)

    def updateFomFile(self):
        updateFomFile2(self)

    def updatePropQuantity(self):
        updatePropQuantity2(self)

    def update_aberrationMod(self):
        update_aberrationMod2(self)


    def start_simulation(self):
        print("Start Simulation")
        # [ [Options], [Propagation Quantities], [Spectrum Parameters], [Source Parameters], [Propagation System]  ]
        self.update_outputText("We will first test the parameters. Please wait...")

        # updating text
        QtWidgets.qApp.processEvents()

        #-----------------------------------------------------------------------
        # Testing parameters
        #-----------------------------------------------------------------------
        test = func_testPars(self)

        all_ok=None
        all_parameters_list = None
        if test:
            all_ok = test[0]
            all_parameters_list = test[1]

        #_______________________________________________________________________


        #-----------------------------------------------------------------------
        # Starting Simulation
        #-----------------------------------------------------------------------
        if test:
            if test[0]:
                sim = func_startSim(self,all_parameters_list)
        #_______________________________________________________________________


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # initial parameters
    log_txt    = "" # log file
    debug      = True
    appname    = "PyWolf 1.0"
    cr = "Copyright (C) 2020 Tiago E. C. Magalhaes under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version."

    # time
    now        = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    double_bar = "="*40
    output_txt = double_bar+"\n"+str(appname)+"\n\n"+str(cr)+" "*10+"\n"+ double_bar  # to be displayed in app
    log_txt+="\n["+str(dt_string)+"]\n"

    # directory
    current_dir = os.getcwd()

    # screen info
    screen = app.primaryScreen()
    size = screen.size()
    rect = screen.availableGeometry()

    # debug
    if debug:
        print('Screen: %s' % screen.name())
        print('Size: %d x %d' % (size.width(), size.height()))
        print('Available: %d x %d' % (rect.width(), rect.height()))

    # creating main window
    MainWindow = QtWidgets.QMainWindow()
    #app.setStyleSheet(stylesheet)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow,appname,rect,current_dir,log_txt,output_txt)
    MainWindow.show()



    sys.exit(app.exec_())
