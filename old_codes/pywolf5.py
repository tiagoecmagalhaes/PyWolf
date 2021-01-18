# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyProPCL4.UI'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QInputDialog, QFileDialog, QLabel, QHBoxLayout

import pyopencl
import os
import psutil
import glob

from palettes import *
from fonts import *
from color import *
from platdev import *

from datetime import datetime


class Ui_MainWindow(object):

    def setupUi(self, MainWindow,appname,rect,current_dir,log_txt,output_txt):

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
        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # Message Scroll Area Color palette
        #=======================================================================
        # MainWindow -> Central Widget -> groupBox project -> Message area

        self.scrollArea_messages = QtWidgets.QScrollArea(self.groupBox_project)
        self.scrollArea_messages.setPalette(palette_messageArea)

        self.scrollArea_messages.setWidgetResizable(True)
        self.scrollArea_messages.setObjectName("scrollArea_messages")
        self.scrollAreaWidgetContents_9 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_9.setGeometry(QtCore.QRect(0, 0, 465, 490))
        self.scrollAreaWidgetContents_9.setObjectName("scrollAreaWidgetContents_9")

        self.gridLayout_4 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_9)
        self.gridLayout_4.setObjectName("gridLayout_4")

        #-----------------------------------------------------------------------
        # Text Box to Write
        #-----------------------------------------------------------------------
        # adding text box to write

        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents_9)

        # palette color
        self.plainTextEdit.setPalette(palette_textEdit)

        # font
        self.plainTextEdit.setFont(font_textBox)
        self.plainTextEdit.setObjectName("plainTextEdit")

        # grid
        self.gridLayout_4.addWidget(self.plainTextEdit, 4, 0, 1, 1)

        # adding space
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 5, 0, 1, 1)
        #_______________________________________________________________________

        #-----------------------------------------------------------------------
        # Output Text Box
        #-----------------------------------------------------------------------
        self.textBrowser = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents_9)
        self.textBrowser.setPalette(palette_outputText)
        self.textBrowser.setMinimumHeight(2*rect.height()/12)

        # font
        self.textBrowser.setFont(font_outText)

        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_4.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.textBrowser.append(str(output_txt))
        #_______________________________________________________________________


        #-----------------------------------------------------------------------
        # Graphics Zone palette
        #-----------------------------------------------------------------------
        self.graphicsView_optSys = QtWidgets.QGraphicsView(self.scrollAreaWidgetContents_9)
        self.graphicsView_optSys.setObjectName("graphicsView_optSys")
        self.gridLayout_4.addWidget(self.graphicsView_optSys, 7, 0, 1, 1)

        # Label Optical System image
        self.label_opticalSys = QtWidgets.QLabel(self.scrollAreaWidgetContents_9)
        self.label_opticalSys.setFont(font_semititle)
        self.label_opticalSys.setObjectName("label_opticalSys")
        self.gridLayout_4.addWidget(self.label_opticalSys, 6, 0, 1, 1)

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 2, 0, 1, 1)
        self.scrollArea_messages.setWidget(self.scrollAreaWidgetContents_9)
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
        self.tab_plotSource = QtWidgets.QWidget()
        self.tab_plotSource.setObjectName("tab_plotSource")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_plotSource)
        self.gridLayout_5.setObjectName("gridLayout_5")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 385, 86))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        # Plot Source
        self.scrollArea_plotSource = QtWidgets.QScrollArea(self.tab_plotSource)
        self.scrollArea_plotSource.setPalette(palette_scrollPlotSource)
        self.scrollArea_plotSource.setWidgetResizable(True)
        self.scrollArea_plotSource.setObjectName("scrollArea_plotSource")
        self.scrollArea_plotSource.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_5.addWidget(self.scrollArea_plotSource, 0, 0, 1, 1)

        self.tabWidget_plots.addTab(self.tab_plotSource, "")
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
        self.tabWidget_plots.addTab(self.tab_plotProp, "")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.tabWidget_plots)
        self.scrollArea_matplot.setWidget(self.scrollAreaWidgetContents_plots)
        self.gridLayout_project.addWidget(self.scrollArea_matplot, 1, 2, 1, 1)
        self.scrollArea_sectionParams = QtWidgets.QScrollArea(self.groupBox_project)
        #_______________________________________________________________________


        #=======================================================================
        # Scroll Area Section Parameters
        #=======================================================================

        # Scroll Area section parameters
        self.scrollArea_sectionParams.setPalette(palette_parSection)
        self.scrollArea_sectionParams.setWidgetResizable(True)
        self.scrollArea_sectionParams.setObjectName("scrollArea_sectionParams")
        self.scrollAreaWidgetContents_numPlanes = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_numPlanes.setGeometry(QtCore.QRect(0, 0, 445, 1780))
        self.scrollAreaWidgetContents_numPlanes.setObjectName("scrollAreaWidgetContents_numPlanes")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_numPlanes)
        self.gridLayout_7.setObjectName("gridLayout_7")

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

        # Tab Widget prop system
        self.tabWidget_propsystem.setSizePolicy(sizePolicy)
        self.tabWidget_propsystem.setPalette(palette_tabPropSys)
        self.tabWidget_propsystem.setFont(font_normalLabel)
        self.tabWidget_propsystem.setIconSize(QtCore.QSize(20, 20))
        self.tabWidget_propsystem.setObjectName("tabWidget_propsystem")

        # tab plane 1
        self.tab_plane1 = QtWidgets.QWidget()
        self.tab_plane1.setPalette(palette_tabPlane)
        self.tab_plane1.setObjectName("tab_plane1")
        self.formLayout_2 = QtWidgets.QFormLayout(self.tab_plane1)
        self.formLayout_2.setObjectName("formLayout_2")

        # Scroll Area Plane 1
        self.scrollArea_plane1 = QtWidgets.QScrollArea(self.tab_plane1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_plane1.sizePolicy().hasHeightForWidth())
        self.scrollArea_plane1.setSizePolicy(sizePolicy)
        self.scrollArea_plane1.setMinimumSize(QtCore.QSize(0, 200))
        self.scrollArea_plane1.setPalette(palette_scrollAreaPlane1)
        self.scrollArea_plane1.setWidgetResizable(True)
        self.scrollArea_plane1.setObjectName("scrollArea_plane1")
        self.scrollAreaWidgetContents_plane1 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_plane1.setGeometry(QtCore.QRect(0, 0, 393, 198))
        self.scrollAreaWidgetContents_plane1.setObjectName("scrollAreaWidgetContents_plane1")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_plane1)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.scrollArea_plane1.setWidget(self.scrollAreaWidgetContents_plane1)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.scrollArea_plane1)
        self.tabWidget_propsystem.addTab(self.tab_plane1, "")

        # Tab plane 2
        self.tab_plane2 = QtWidgets.QWidget()
        self.tab_plane2.setObjectName("tab_plane2")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.tab_plane2)
        self.gridLayout_8.setObjectName("gridLayout_8")

        # Scroll Area Plane 2
        self.scrollArea_plane2 = QtWidgets.QScrollArea(self.tab_plane2)
        self.scrollArea_plane2.setPalette(palette_scrollAreaPlane1)
        self.scrollArea_plane2.setWidgetResizable(True)
        self.scrollArea_plane2.setObjectName("scrollArea_plane2")
        self.scrollAreaWidgetContents_plane2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_plane2.setGeometry(QtCore.QRect(0, 0, 393, 199))
        self.scrollAreaWidgetContents_plane2.setObjectName("scrollAreaWidgetContents_plane2")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_plane2)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.scrollArea_plane2.setWidget(self.scrollAreaWidgetContents_plane2)
        self.gridLayout_8.addWidget(self.scrollArea_plane2, 0, 0, 1, 1)
        self.tabWidget_propsystem.addTab(self.tab_plane2, "")

        # Tab Plane 2
        self.tab_plane3 = QtWidgets.QWidget()
        self.tab_plane3.setObjectName("tab_plane3")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.tab_plane3)
        self.gridLayout_9.setObjectName("gridLayout_9")

        # Scroll Area Plane 3
        self.scrollArea_plane3 = QtWidgets.QScrollArea(self.tab_plane3)
        self.scrollArea_plane3.setPalette(palette_scrollAreaPlane1)
        self.scrollArea_plane3.setWidgetResizable(True)
        self.scrollArea_plane3.setObjectName("scrollArea_plane3")
        self.scrollAreaWidgetContents_plane3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_plane3.setGeometry(QtCore.QRect(0, 0, 393, 199))
        self.scrollAreaWidgetContents_plane3.setObjectName("scrollAreaWidgetContents_plane3")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_plane3)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.scrollArea_plane3.setWidget(self.scrollAreaWidgetContents_plane3)
        self.gridLayout_9.addWidget(self.scrollArea_plane3, 0, 0, 1, 1)
        self.tabWidget_propsystem.addTab(self.tab_plane3, "")
        self.gridLayout_7.addWidget(self.tabWidget_propsystem, 65, 0, 1, 2)
        #_______________________________________________________________________


        #=======================================================================
        # Spin Box
        #=======================================================================
        self.spinBox_numPlanes = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_numPlanes)
        self.spinBox_numPlanes.setObjectName("spinBox_numPlanes")
        self.spinBox_numPlanes.setFont(font_normalLabel)
        self.spinBox_numPlanes.setMinimum(1)
        self.spinBox_numPlanes.setMaximum(3)
        self.gridLayout_7.addWidget(self.spinBox_numPlanes, 64, 1, 1, 1)
        #_______________________________________________________________________


        #=======================================================================
        # date time widget
        #=======================================================================
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.scrollAreaWidgetContents_numPlanes)
        self.dateTimeEdit.setFont(font_normalLabel)
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.gridLayout_7.addWidget(self.dateTimeEdit, 85, 0, 1, 2)
        #_______________________________________________________________________


        #=======================================================================
        # Computational Variables
        #=======================================================================

        # present time
        self.nowTime = datetime.now()

        # directory name
        self.saveDirName = None

        # minimum size for combo boxes
        self.minwidth_combo = rect.width()/7

        # max width size for combo boxes when VIEWING
        self.maxWidthView_combo = rect.width()/2

        #-------------------------Spectrum Parameters---------------------------

        # Spectrum Models List ex: [ ["Gaussian", OBJECT] , ["Lorentzian, OBJECT] ]
        self.specModel_list = []

        # Spectrum Model Parameters ex: [ ["a"],["a","b"] ]
        self.specModelPar_list = []

        # Spectrum Model Line Edit Parameters
        self.specModel_lineEditParameters = []
        #_______________________________________________________________________

        #-------------------------Geometry Parameters---------------------------

        # Geometry Models List ex: [ ["Circle", OBJECT] , ["Rectangle", OBJECT] ]
        self.geometry_list = []

        # Geometry Model Parameters ex: [ ["a"],["a","b"] ]
        self.geometryPar_list = []

        # Geometry Line Edit Parameters  ex. [ OBJECT, OBJECT]
        self.geometry_lineEditParameters = []
        #_______________________________________________________________________


        #-------------------------Coherence Parameters--------------------------
        # Coherence Models List ex: [ ["GSM", OBJECT] , ["GSM2", OBJECT] ]
        self.cohModel_list = []

        # Geometry Model Parameters ex: [ ["a"],["a","b"] ]
        self.cohModelPar_list = []

        # Geometry Line Edit Parameters  ex. [ OBJECT, OBJECT]
        self.cohModel_lineEditParameters = []
        #_______________________________________________________________________

        # Coherence state dictionary+
        cohState_dict = {0:"Incoherent",1:"Coherent",2:"Partially Coherent"}

        # Coherence Models List
        self.cohModel_list = []

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
        self.gridLayout_7.addWidget(self.label, 0, 0, 1, 1)

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
        self.gridLayout_7.addWidget(self.label_saveFile, 1, 0, 1, 1)

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
        self.label_propQuant = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_propQuant.setPalette(palette_parSection)
        self.label_propQuant.setFont(font_normalLabel)
        self.label_propQuant.setObjectName("label_propQuant")
        self.gridLayout_7.addWidget(self.label_propQuant, 25, 0, 1, 1)

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

        # label Coherence State
        self.label_cohState = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_cohState.setPalette(palette_parSection)
        self.label_cohState.setFont(font_normalLabel)
        self.label_cohState.setObjectName("label_cohState")
        self.gridLayout_7.addWidget(self.label_cohState, 50, 0, 1, 1)

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

        # Label Distance 1
        self.label_distance1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_plane1)
        self.label_distance1.setPalette(palette_parSection)
        self.label_distance1.setFont(font_normalLabel)
        self.label_distance1.setObjectName("label_distance1")
        self.gridLayout_11.addWidget(self.label_distance1, 0, 0, 1, 1)

        # Label Focal length 1 Color palette
        self.label_focalLength1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_plane1)
        self.label_focalLength1.setPalette(palette_parSection)
        self.label_focalLength1.setFont(font_normalLabel)
        self.label_focalLength1.setObjectName("label_focalLength1")
        self.gridLayout_11.addWidget(self.label_focalLength1, 4, 0, 1, 1)

        # label pupil 1
        self.label_pupil1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_plane1)
        self.label_pupil1.setPalette(palette_parSection)
        self.label_pupil1.setFont(font_normalLabel)
        self.label_pupil1.setObjectName("label_pupil1")
        self.gridLayout_11.addWidget(self.label_pupil1, 2, 0, 1, 1)

        # label distance 2
        self.label_distance2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_plane2)
        self.label_distance2.setPalette(palette_parSection)
        self.label_distance2.setFont(font_normalLabel)
        self.label_distance2.setObjectName("label_distance2")
        self.gridLayout_10.addWidget(self.label_distance2, 1, 0, 1, 1)

        # Label Focal Length 2
        self.label_focalLength2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_plane2)
        self.label_focalLength2.setPalette(palette_parSection)
        self.label_focalLength2.setFont(font_normalLabel)
        self.label_focalLength2.setObjectName("label_focalLength2")
        self.gridLayout_10.addWidget(self.label_focalLength2, 9, 0, 1, 1)

        # Label Pupil 2
        self.label_pupil2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_plane2)
        self.label_pupil2.setPalette(palette_parSection)
        self.label_pupil2.setFont(font_normalLabel)
        self.label_pupil2.setObjectName("label_pupil2")
        self.gridLayout_10.addWidget(self.label_pupil2, 5, 0, 1, 1)

        # Label distance3
        self.label_distance3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_plane3)
        self.label_distance3.setPalette(palette_parSection)
        self.label_distance3.setFont(font_normalLabel)
        self.label_distance3.setObjectName("label_distance3")
        self.gridLayout_12.addWidget(self.label_distance3, 0, 0, 1, 1)

        # label_pupil3
        self.label_pupil3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_plane3)
        self.label_pupil3.setPalette(palette_parSection)
        self.label_pupil3.setFont(font_normalLabel)
        self.label_pupil3.setObjectName("label_pupil3")
        self.gridLayout_12.addWidget(self.label_pupil3, 2, 0, 1, 1)

        # label focal length 3
        self.label_focalLength3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_plane3)
        self.label_focalLength3.setPalette(palette_parSection)
        self.label_focalLength3.setFont(font_normalLabel)
        self.label_focalLength3.setObjectName("label_focalLength3")
        self.gridLayout_12.addWidget(self.label_focalLength3, 4, 0, 1, 1)

        # label Start Simulation
        self.label_startSim = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_startSim.setPalette(palette_titles)
        self.label_startSim.setFont(font_title)
        self.label_startSim.setAlignment(QtCore.Qt.AlignCenter)
        self.label_startSim.setObjectName("label_2")
        self.gridLayout_7.addWidget(self.label_startSim, 74, 0, 1, 2)

        # Label Insert Comments
        self.label_insertComments = QtWidgets.QLabel(self.scrollAreaWidgetContents_9)
        self.label_insertComments.setFont(font_normalLabel)
        self.label_insertComments.setObjectName("label_insertComments")
        self.gridLayout_4.addWidget(self.label_insertComments, 3, 0, 1, 1)

        # Label Output Messages
        self.label_outMessages = QtWidgets.QLabel(self.scrollAreaWidgetContents_9)
        self.label_outMessages.setFont(font_semititle)
        self.label_outMessages.setObjectName("label_outMessages")
        self.gridLayout_4.addWidget(self.label_outMessages, 0, 0, 1, 1)

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
        self.gridLayout_7.addWidget(self.line_comPar1, 3, 0, 1, 2)

        # horizontal line computation parameters 2
        self.line_compPar2 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_compPar2.setLineWidth(2)
        self.line_compPar2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_compPar2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_compPar2.setObjectName("line_compPar2")
        self.line_compPar2.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_compPar2, 5, 0, 1, 2)

        # Horizontal Line propagation quantities 1
        self.line_propQuant1 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_propQuant1.setLineWidth(2)
        self.line_propQuant1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_propQuant1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_propQuant1.setObjectName("line_propQuant1")
        self.line_propQuant1.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_propQuant1, 19, 0, 1, 2)

        # horizontal line propagation quantity 2
        self.line_propQuant2 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_propQuant2.setLineWidth(2)
        self.line_propQuant2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_propQuant2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_propQuant2.setObjectName("line_propQuant2")
        self.line_propQuant2.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_propQuant2, 24, 0, 1, 2)

        # horizontal line spectral parameters 1
        self.line_specPar1 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_specPar1.setLineWidth(2)
        self.line_specPar1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_specPar1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_specPar1.setObjectName("line_specPar1")
        self.line_specPar1.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_specPar1, 30, 0, 1, 2)

        # horizontal line spectral parameters 2
        self.line_specPar2 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_specPar2.setLineWidth(2)
        self.line_specPar2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_specPar2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_specPar2.setObjectName("line_specPar2")
        self.line_specPar2.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_specPar2, 33, 0, 1, 2)

        # horizontal line source parameter2 1
        self.line_sourcePar1 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_sourcePar1.setLineWidth(2)
        self.line_sourcePar1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_sourcePar1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_sourcePar1.setObjectName("line_sourcePar1")
        self.line_sourcePar1.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_sourcePar1, 43, 0, 1, 2)

        # Horizontal Line source parameters 2
        self.line_sourcePar2 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_sourcePar2.setLineWidth(2)
        self.line_sourcePar2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_sourcePar2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_sourcePar2.setObjectName("line_sourcePar2")
        self.line_sourcePar2.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_sourcePar2, 45, 0, 1, 2)

        # horizontal line propagation system 1
        self.line_propSys1 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_propSys1.setLineWidth(2)
        self.line_propSys1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_propSys1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_propSys1.setObjectName("line_propSys1")
        self.line_propSys1.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_propSys1, 60, 0, 1, 2)

        # Horizontal line propagation system 2
        self.line_propSys2 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_propSys2.setLineWidth(2)
        self.line_propSys2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_propSys2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_propSys2.setObjectName("line_propSys2")
        self.line_propSys2.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_propSys2, 62, 0, 1, 2)

        # horizontal line start sim 1
        self.line = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line_startSim1")
        self.line.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line, 73, 0, 1, 2)

        # horizontal line start sim 2
        self.line_2 = QtWidgets.QFrame(self.scrollAreaWidgetContents_numPlanes)
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_startSim2")
        self.line_2.setStyleSheet('background: '+colortxt_hor_line)
        self.gridLayout_7.addWidget(self.line_2, 75, 0, 1, 2)

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
        self.gridLayout_7.addWidget(self.lineEdit_simName, 0, 1, 1, 1)
        # setting size
        self.lineEdit_simName.setMaximumWidth(self.minwidth_combo)
        #self.lineEdit_simName.actionEvent()
        self.lineEdit_simName.textChanged.connect(self.update_titleProject)

        # line Save file txt
        self.lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_save)
        self.lineEdit.setFont(font_normalLabel)
        self.lineEdit.setObjectName("Save File")
        self.lineEdit.setStyleSheet('background: '+colortxt_textEdit)
        self.gridLayout_save.addWidget(self.lineEdit, 0, 1, 1, 1)
        results_directory = str(current_dir)+'\\results'
        self.saveDirName = results_directory
        self.lineEdit.setText(results_directory)
        # start at the line 0:
        self.lineEdit.setCursorPosition(0)
        # setting size
        self.lineEdit.setMaximumWidth(self.minwidth_combo)

        # text edit in N
        self.lineEdit_N = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_numPlanes)
        self.lineEdit_N.setFont(font_normalLabel)
        self.lineEdit_N.setObjectName("lineEdit_N")
        self.lineEdit_N.setStyleSheet('background: '+colortxt_textEdit)
        self.gridLayout_7.addWidget(self.lineEdit_N, 15, 1, 1, 1)
        self.lineEdit_N.setMaximumWidth(self.minwidth_combo)

        # line edit Central Frequency
        self.lineEdit_centralFreq = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_numPlanes)
        self.lineEdit_centralFreq.setObjectName("lineEdit_centralFreq")
        self.lineEdit_centralFreq.setStyleSheet('background: '+colortxt_textEdit)
        self.gridLayout_7.addWidget(self.lineEdit_centralFreq, 38, 1, 1, 1)
        # setting size
        self.lineEdit_centralFreq.setMaximumWidth(self.minwidth_combo)

        # line edit text source resolution
        self.lineEdit_souceRes = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_numPlanes)
        self.lineEdit_souceRes.setFont(font_normalLabel)
        self.lineEdit_souceRes.setObjectName("lineEdit_souceRes")
        self.lineEdit_souceRes.setStyleSheet('background: '+colortxt_textEdit)
        self.gridLayout_7.addWidget(self.lineEdit_souceRes, 47, 1, 1, 1)
        # setting size
        self.lineEdit_souceRes.setMaximumWidth(self.minwidth_combo)

        # line edit text distance 1
        self.lineEdit_distance1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_plane1)
        self.lineEdit_distance1.setObjectName("lineEdit_distance1")
        self.lineEdit_distance1.setStyleSheet('background: '+colortxt_textEdit)
        self.gridLayout_11.addWidget(self.lineEdit_distance1, 0, 1, 1, 1)
        # setting size
        self.lineEdit_distance1.setMaximumWidth(self.minwidth_combo)

        # line edit text focal length
        self.lineEdit_focalLength1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_plane1)
        self.lineEdit_focalLength1.setObjectName("lineEdit_focalLength1")
        self.gridLayout_11.addWidget(self.lineEdit_focalLength1, 4, 1, 1, 1)
        # setting size
        self.lineEdit_focalLength1.setMaximumWidth(self.minwidth_combo)

        # line edit text distance 2
        self.lineEdit_distance2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_plane2)
        self.lineEdit_distance2.setObjectName("lineEdit_distance2")
        self.gridLayout_10.addWidget(self.lineEdit_distance2, 1, 1, 1, 1)
        # setting size
        self.lineEdit_distance2.setMaximumWidth(self.minwidth_combo)

        # line edit text focal length 2
        self.lineEdit_focalLength2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_plane2)
        self.lineEdit_focalLength2.setObjectName("lineEdit_focalLength2")
        self.gridLayout_10.addWidget(self.lineEdit_focalLength2, 9, 1, 1, 1)
        # setting size
        self.lineEdit_focalLength2.setMaximumWidth(self.minwidth_combo)

        # line edit text distance 3
        self.lineEdit_distance3 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_plane3)
        self.lineEdit_distance3.setObjectName("lineEdit_distance3")
        self.gridLayout_12.addWidget(self.lineEdit_distance3, 0, 1, 1, 1)
        # setting size
        self.lineEdit_distance3.setMaximumWidth(self.minwidth_combo)

        # line edit focal length 3
        self.lineEdit_focalLength3 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_plane3)
        self.lineEdit_focalLength3.setObjectName("lineEdit_focalLength3")
        self.gridLayout_12.addWidget(self.lineEdit_focalLength3, 4, 1, 1, 1)
        # setting size
        self.lineEdit_focalLength3.setMaximumWidth(self.minwidth_combo)

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
        for i in range(0,len(list_platforms)):
            self.comboBox_platform.addItem(str(list_platforms[i]),platform_choices[str(list_platforms[i])])
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
        self.update_devices(output_txt)
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
        self.comboBox_propQuant = QtWidgets.QComboBox(self.scrollAreaWidgetContents_numPlanes)
        self.comboBox_propQuant.setFont(font_normalLabel)
        self.comboBox_propQuant.setObjectName("comboBox_propQuant")
        self.gridLayout_7.addWidget(self.comboBox_propQuant, 25, 1, 1, 1)
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

        # combo box coherent state
        self.comboBox_cohState = QtWidgets.QComboBox(self.scrollAreaWidgetContents_numPlanes)
        self.comboBox_cohState.setFont(font_normalLabel)
        self.comboBox_cohState.setObjectName("comboBox_cohState")
        self.gridLayout_7.addWidget(self.comboBox_cohState, 50, 1, 1, 1)
        for item in cohState_dict.items():
            self.comboBox_cohState.addItem(item[1],item[0])
        # setting size
        self.comboBox_cohState.setMaximumWidth(self.minwidth_combo)
        self.comboBox_cohState.setStyleSheet('''*
        QComboBox QAbstractItemView
            {
            min-width: '''+str(self.maxWidthView_combo)+'''px;
            }
        ''')

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

        # combo box pupil function 1
        self.comboBox_pupilFunc1 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_plane1)
        self.comboBox_pupilFunc1.setObjectName("comboBox_pupilFunc1")
        self.gridLayout_11.addWidget(self.comboBox_pupilFunc1, 2, 1, 1, 1)
        # setting size
        self.comboBox_pupilFunc1.setMaximumWidth(self.minwidth_combo)
        self.comboBox_pupilFunc1.setStyleSheet('''*
        QComboBox QAbstractItemView
            {
            min-width: '''+str(self.maxWidthView_combo)+'''px;
            }
        ''')

        # combo box pupil Func 2
        self.comboBox_pupilFunc2 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_plane2)
        self.comboBox_pupilFunc2.setObjectName("comboBox_pupilFunc2")
        self.gridLayout_10.addWidget(self.comboBox_pupilFunc2, 5, 1, 1, 1)
        # setting size
        self.comboBox_pupilFunc2.setMaximumWidth(self.minwidth_combo)
        self.comboBox_pupilFunc2.setStyleSheet('''*
        QComboBox QAbstractItemView
            {
            min-width: '''+str(self.maxWidthView_combo)+'''px;
            }
        ''')

        # combo box pupil func 3
        self.comboBox_pupilFunc3 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_plane3)
        self.comboBox_pupilFunc3.setObjectName("comboBox_pupilFunc3")
        self.gridLayout_12.addWidget(self.comboBox_pupilFunc3, 2, 1, 1, 1)
        # setting size
        self.comboBox_pupilFunc3.setMaximumWidth(self.minwidth_combo)
        self.comboBox_pupilFunc3.setStyleSheet('''*
        QComboBox QAbstractItemView
            {
            min-width: '''+str(self.maxWidthView_combo)+'''px;
            }
        ''')

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

        # checkbox save
        self.checkBox_save = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_save)
        self.checkBox_save.setFont(font_normalLabel)
        self.checkBox_save.setObjectName("checkBox_save")
        self.gridLayout_save.addWidget(self.checkBox_save, 0, 0, 1, 1)

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

        # checkbox debug
        self.checkBox_debug = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_numPlanes)
        self.checkBox_debug.setPalette(palette_parSection)
        self.checkBox_debug.setFont(font_normalLabel)
        self.checkBox_debug.setObjectName("checkBox_debug")
        self.gridLayout_7.addWidget(self.checkBox_debug, 14, 0, 1, 1)

        # CheckBox_farfield1 Color palette
        self.checkBox_farfield1 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_plane1)
        self.checkBox_farfield1.setFont(font_normalLabel)
        self.checkBox_farfield1.setPalette(palette_parSection)
        self.checkBox_farfield1.setObjectName("checkBox_farfield1")
        self.gridLayout_11.addWidget(self.checkBox_farfield1, 1, 0, 1, 1)

        # checkBoxfar-field 2
        self.checkBox_farfield2 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_plane2)
        self.checkBox_farfield2.setPalette(palette_parSection)
        self.checkBox_farfield2.setFont(font_normalLabel)
        self.checkBox_farfield2.setObjectName("checkBox_farfield2")
        self.gridLayout_10.addWidget(self.checkBox_farfield2, 2, 0, 1, 1)

        # CheckBox lens1
        self.checkBox_lens = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_plane1)
        self.checkBox_lens.setPalette(palette_parSection)
        self.checkBox_lens.setFont(font_normalLabel)
        self.checkBox_lens.setObjectName("checkBox_lens")
        self.gridLayout_11.addWidget(self.checkBox_lens, 3, 0, 1, 1)

        # checkbox lens 2
        self.checkBox_lens2 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_plane2)
        self.checkBox_lens2.setPalette(palette_parSection)
        self.checkBox_lens2.setFont(font_normalLabel)
        self.checkBox_lens2.setObjectName("checkBox_lens2")
        self.gridLayout_10.addWidget(self.checkBox_lens2, 6, 0, 1, 1)

        # label_focalLength3  Color palette
        self.checkBox_lens3 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_plane3)
        self.checkBox_lens3.setPalette(palette_parSection)
        self.checkBox_lens3.setFont(font_normalLabel)
        self.checkBox_lens3.setObjectName("checkBox_lens3")
        self.gridLayout_12.addWidget(self.checkBox_lens3, 3, 0, 1, 1)

        # check box far-field 3
        self.checkBox_farfield3 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_plane3)
        self.checkBox_farfield3.setPalette(palette_parSection)
        self.checkBox_farfield3.setFont(font_normalLabel)
        self.checkBox_farfield3.setObjectName("checkBox_farfield3")
        self.gridLayout_12.addWidget(self.checkBox_farfield3, 1, 0, 1, 1)

        # checkbox schedule simulation
        self.checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_numPlanes)
        self.checkBox.setFont(font_normalLabel)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_7.addWidget(self.checkBox, 84, 0, 1, 2)

        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        #=======================================================================
        # Radio buttons
        #=======================================================================
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
        self.gridLayout_save.addWidget(self.toolButton_saveFile, 1, 1, 1, 1)
        # action
        self.toolButton_saveFile.clicked.connect(self.openFileNameDialog_saveDir)

        # tool button source file
        self.toolButton_sourcefromfile = QtWidgets.QToolButton(self.scrollAreaWidgetContents_numPlanes)
        self.toolButton_sourcefromfile.setFont(font_normalLabel)
        self.toolButton_sourcefromfile.setObjectName("toolButton_sourcefromfile")
        self.gridLayout_7.addWidget(self.toolButton_sourcefromfile, 48, 1, 1, 1)

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
        self.gridLayout_7.addWidget(self.pushButton_start, 83, 0, 1, 2)

        # Update button
        self.pushButton_updatePlots = QtWidgets.QPushButton(self.scrollAreaWidgetContents_plots)
        self.pushButton_updatePlots.setFont(font_button)
        self.pushButton_updatePlots.setObjectName("pushButton_updatePlots")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.pushButton_updatePlots)

        #-----------------------------------------------------------------------
        #///////////////////////////////////////////////////////////////////////
        #-----------------------------------------------------------------------


        # Save
        self.scrollArea_save.setWidget(self.scrollAreaWidgetContents_save)
        self.gridLayout_7.addWidget(self.scrollArea_save,11, 0, 1, 2)

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
        self.gridLayout_project.addWidget(self.scrollArea_sectionParams, 0, 0, 2, 1)
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
        self.checkBox.setText(_translate("MainWindow", "Scheldule Simulation"))
        self.radioButton_poly.setText(_translate("MainWindow", "Polychromatic"))
        self.label_SourceParameters.setText(_translate("MainWindow", "Source Parameters"))
        self.label_distance1.setText(_translate("MainWindow", "Distance (m):"))
        self.checkBox_farfield1.setText(_translate("MainWindow", "Far-field"))
        self.label_pupil1.setText(_translate("MainWindow", "Pupil:"))
        self.checkBox_lens.setText(_translate("MainWindow", "Lens"))
        self.label_focalLength1.setText(_translate("MainWindow", "Focal Length (m):"))
        self.tabWidget_propsystem.setTabText(self.tabWidget_propsystem.indexOf(self.tab_plane1), _translate("MainWindow", "Plane 1"))
        self.label_distance2.setText(_translate("MainWindow", "Distance (m):"))
        self.label_focalLength2.setText(_translate("MainWindow", "Focal Length (m):"))
        self.label_pupil2.setText(_translate("MainWindow", "Pupil:"))
        self.checkBox_lens2.setText(_translate("MainWindow", "Lens"))
        self.checkBox_farfield2.setText(_translate("MainWindow", "Far-field"))
        self.tabWidget_propsystem.setTabText(self.tabWidget_propsystem.indexOf(self.tab_plane2), _translate("MainWindow", "Plane 2"))
        self.label_distance3.setText(_translate("MainWindow", "Distance (m):"))
        self.checkBox_farfield3.setText(_translate("MainWindow", "Far-field"))
        self.label_pupil3.setText(_translate("MainWindow", "Pupil:"))
        self.checkBox_lens3.setText(_translate("MainWindow", "Lens"))
        self.label_focalLength3.setText(_translate("MainWindow", "Focal Length (m):"))
        self.tabWidget_propsystem.setTabText(self.tabWidget_propsystem.indexOf(self.tab_plane3), _translate("MainWindow", "Plane 3"))
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
        self.label_cohState.setText(_translate("MainWindow", "Coherence State:"))
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
        self.showRAM(output_txt)
        self.search_specModel(current_dir,output_txt)
        self.search_cohModel(current_dir,output_txt)
        self.search_geometry(current_dir,output_txt)
        self.update_specPars()


    def update_devices(self,output_txt):
        #=======================================================================
        # Platform and Device Combo Boxes
        #=======================================================================
        global current_platform
        current_platform = self.comboBox_platform.currentIndex()
        self.comboBox_device.clear()
        for k in device_choices[current_platform].items():
            self.comboBox_device.addItem(k[0],device_choices[current_platform][k[0]])

        if self.comboBox_device.count()==0:
            new="\n[info] There is currently no device for that selected platform."
            self.textBrowser.append(str(new))
            self.textBrowser.update()
        #self.update_outputText(output_txt)
        #_______________________________________________________________________

    def update_outputText(self,text,output_txt):
        "Updates the Output Message box in the application"
        self.textBrowser.append("\n"+self.bar+"\n"+self.give_time()+"\n"+self.bar+"\n"+str(text)+"\n"+self.bar)
        self.textBrowser.update()

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

    def openFileNameDialog_saveDir(self,output_txt):
        "choose save directory"
        download_path = self.lineEdit.text()
        #options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        filename = None
        try:
            self.dirName = QFileDialog.getExistingDirectory(None,"Save Directory",download_path) # ,,options=options
            self.lineEdit.clear()
            self.lineEdit.setText(self.dirName)
        except:
            update_outputText("Something went wrong when choosing saving directory.",output_txt)

    def showRAM(self,output_txt):
        "Shows the ammount of RAM in the output Message Box"
        ram_info  = psutil.virtual_memory()
        total_ram = ram_info[0]
        avail_ram = ram_info[1]
        perc_ram  = ram_info[2]
        #new_txt=self.bar+"\n RAM info\n"+self.bar+"\n Total Ram: "+str(round(float(total_ram)/1073741824.0,1))+" GB\n Available Ram: "+str(round(float(avail_ram)/1073741824.0,1))+" GB ("+str(100-perc_ram)+" %)\n"+self.bar+"\n"
        new_txt = " Total Ram: "+str(round(float(total_ram)/1073741824.0,1))+" GB\n Available Ram: "+str(round(float(avail_ram)/1073741824.0,1))+" GB ("+str(100-perc_ram)+" %)"
        self.update_outputText(new_txt,output_txt)

    def addTime(self,output_txt):
        now = datetime.now()
        day_time = now.strftime("%d/%m/%Y %H:%M:%S")
        log_txt+="\n["+day_time+"]\n"
        new_txt = "\n\n["+str(dt_string)+"]"
        self.update_outputText(new_txt,output_txt)

    def search_specModel(self,current_dir,output_txt):
        spec_dir=current_dir+"\\specModels\\"
        os.chdir(spec_dir)
        sys.path.append(spec_dir)
        # cleaning combo box of spectrum models
        self.comboBox_specType.clear()
        new_file=None
        count=0
        for file_dir in glob.glob("*.py"):
            new_file = __import__(str(file_dir[:-3]))
            self.specModel_list.append([new_file.specModel_name,new_file])
            self.specModelPar_list.append(new_file.specModel_parameters)
            self.comboBox_specType.addItem(self.specModel_list[-1][0])
            count+=1
        if count!=0:
            self.updateSpecModelPars()
        else:
            temp_txt = "No Spectrum models were found in folder <specModels>"
            self.update_outputText(temp_txt,output_txt)

    def updateSpecModelPars(self):
        for i in range(0,len(self.specModelPar_list)):
            current_specModel = self.comboBox_specType.currentText()
            for i in range(0,len(self.specModel_list)):
                if current_specModel == self.specModel_list[i][0]:
                    # clearing
                    for lab in self.specModel_labelParameters:
                        self.clear_LabelText(lab)
                        lab.deleteLater()
                    for edits in self.specModel_lineEditParameters:
                        edits.deleteLater()
                    # clearing label parameters
                    self.specModel_labelParameters = []
                    self.specModel_lineEditParameters = []
                    # for each parameter:
                    for j in range(0,len(self.specModelPar_list[i])):
                        # adding label for each parameter
                        self.specModel_labelParameters.append(QtWidgets.QLabel(self.scrollAreaWidgetContents_spectrumModel))
                        self.specModel_labelParameters[-1].setPalette(palette_parSection)
                        self.specModel_labelParameters[-1].setFont(font_normalLabel)
                        self.specModel_labelParameters[-1].setObjectName(self.specModelPar_list[i][j])
                        self.gridLayout_specModel.addWidget(self.specModel_labelParameters[-1], 1+j, 0, 1, 1)
                        # adding line edit entries
                        self.specModel_lineEditParameters.append(QtWidgets.QLineEdit(self.scrollAreaWidgetContents_numPlanes))
                        self.specModel_lineEditParameters[-1].setFont(font_normalLabel)
                        self.specModel_lineEditParameters[-1].setObjectName("lineEdit_"+self.specModelPar_list[i][j])
                        self.specModel_lineEditParameters[-1].setStyleSheet('background: '+colortxt_textEdit)
                        self.gridLayout_specModel.addWidget(self.specModel_lineEditParameters[-1], 1+j, 1, 1, 1)
                        # setting size
                        self.specModel_lineEditParameters[-1].setMaximumWidth(self.minwidth_combo)
                        # Text in APP
                        self.add_labelsText(self.specModel_labelParameters[-1],self.specModelPar_list[i][j]+":")

    def add_labelsText(self,label,text):
        _translate = QtCore.QCoreApplication.translate
        label.setText(_translate("MainWindow", text))

    def clear_LabelText(self,label):
        label.clear()

    def search_geometry(self,current_dir,output_txt):
        "searchs for geometry models"
        geometry_dir=current_dir+"\\geometry\\"
        os.chdir(geometry_dir)
        sys.path.append(geometry_dir)
        # cleaning combo box of spectrum models
        self.comboBox_geometry.clear()
        new_file=None
        count=0
        for file_dir in glob.glob("*.py"):
            new_file = __import__(str(file_dir[:-3]))
            self.geometry_list.append([new_file.geometry_name,new_file])
            self.geometryPar_list.append(new_file.geometry_parameters)
            self.comboBox_geometry.addItem(self.geometry_list[-1][0])
            count+=1
        if count!=0:
            self.updateGeometryPars()
        else:
            temp_txt = "No Geometry models were found in folder <geometry>"
            self.update_outputText(temp_txt,output_txt)

    def updateGeometryPars(self):
        for i in range(0,len(self.geometryPar_list)):
            current_geometry = self.comboBox_geometry.currentText()
            for i in range(0,len(self.geometry_list)):
                if current_geometry == self.geometry_list[i][0]:
                    # clearing
                    for lab in self.geometry_labelParameters:
                        self.clear_LabelText(lab)
                        lab.deleteLater()
                    for edits in self.geometry_lineEditParameters:
                        edits.deleteLater()
                    # clearing label parameters
                    self.geometry_labelParameters = []
                    self.geometry_lineEditParameters = []
                    # for each parameter:
                    for j in range(0,len(self.geometryPar_list[i])):
                        # adding label for each parameter
                        self.geometry_labelParameters.append(QtWidgets.QLabel(self.scrollAreaWidgetContents_spectrumModel))
                        self.geometry_labelParameters[-1].setPalette(palette_parSection)
                        self.geometry_labelParameters[-1].setFont(font_normalLabel)
                        self.geometry_labelParameters[-1].setObjectName(self.specModelPar_list[i][j])
                        self.gridLayout_geometry.addWidget(self.geometry_labelParameters[-1], 1+j, 0, 1, 1)
                        # adding line edit entries
                        self.geometry_lineEditParameters.append(QtWidgets.QLineEdit(self.scrollAreaWidgetContents_numPlanes))
                        self.geometry_lineEditParameters[-1].setFont(font_normalLabel)
                        self.geometry_lineEditParameters[-1].setObjectName("lineEdit_"+self.geometryPar_list[i][j])
                        self.geometry_lineEditParameters[-1].setStyleSheet('background: '+colortxt_textEdit)
                        self.gridLayout_geometry.addWidget(self.geometry_lineEditParameters[-1], 1+j, 1, 1, 1)
                        # setting size
                        self.geometry_lineEditParameters[-1].setMaximumWidth(self.minwidth_combo)
                        # Text in APP
                        self.add_labelsText(self.geometry_labelParameters[-1],self.geometryPar_list[i][j]+":")

    def search_cohModel(self,current_dir,output_txt):
        coh_dir=current_dir+"\\cohModels\\"
        os.chdir(coh_dir)
        sys.path.append(coh_dir)
        # cleaning combo box of spectrum models
        self.comboBox_cohModel.clear()
        new_file=None
        count=0
        for file_dir in glob.glob("*.py"):
            new_file = __import__(str(file_dir[:-3]))
            self.cohModel_list.append([new_file.cohModel_name,new_file])
            self.cohModelPar_list.append(new_file.cohModel_parameters)
            self.comboBox_cohModel.addItem(self.cohModel_list[-1][0])
            count+=1
        if count!=0:
            self.updateCohModelPars()
        else:
            temp_txt = "No Coherence models were found in folder <cohModels>"
            self.update_outputText(temp_txt,output_txt)


    def updateCohModelPars(self):
        for i in range(0,len(self.cohModelPar_list)):
            current_cohModel = self.comboBox_cohModel.currentText()
            for i in range(0,len(self.cohModel_list)):
                if current_cohModel == self.cohModel_list[i][0]:
                    # clearing
                    for lab in self.cohModel_labelParameters:
                        self.clear_LabelText(lab)
                        lab.deleteLater()
                    for edits in self.cohModel_lineEditParameters:
                        edits.deleteLater()
                    # clearing label parameters
                    self.cohModel_labelParameters = []
                    self.cohModel_lineEditParameters = []
                    # for each parameter:
                    for j in range(0,len(self.cohModelPar_list[i])):
                        # adding label for each parameter
                        self.cohModel_labelParameters.append(QtWidgets.QLabel(self.scrollAreaWidgetContents_cohModel))
                        self.cohModel_labelParameters[-1].setPalette(palette_parSection)
                        self.cohModel_labelParameters[-1].setFont(font_normalLabel)
                        self.cohModel_labelParameters[-1].setObjectName(self.cohModelPar_list[i][j])
                        self.gridLayout_cohModel.addWidget(self.cohModel_labelParameters[-1], 1+j, 0, 1, 1)
                        # adding line edit entries
                        self.cohModel_lineEditParameters.append(QtWidgets.QLineEdit(self.scrollAreaWidgetContents_numPlanes))
                        self.cohModel_lineEditParameters[-1].setFont(font_normalLabel)
                        self.cohModel_lineEditParameters[-1].setObjectName("lineEdit_"+self.cohModelPar_list[i][j])
                        self.cohModel_lineEditParameters[-1].setStyleSheet('background: '+colortxt_textEdit)
                        self.gridLayout_cohModel.addWidget(self.cohModel_lineEditParameters[-1], 1+j, 1, 1, 1)
                        # setting size
                        self.cohModel_lineEditParameters[-1].setMaximumWidth(self.minwidth_combo)
                        # Text in APP
                        self.add_labelsText(self.cohModel_labelParameters[-1],self.cohModelPar_list[i][j]+":")

    def update_titleProject(self):
        _translate = QtCore.QCoreApplication.translate
        self.groupBox_project.setTitle(_translate("MainWindow", self.lineEdit_simName.text()))

    def update_specPars(self):
        if self.radioButton_poly.isChecked():
            # Spectrum Model
            self.scrollArea_spectrumModel.setWidget(self.scrollAreaWidgetContents_spectrumModel)
            self.gridLayout_7.addWidget(self.scrollArea_spectrumModel,39, 0, 1, 2)
            # remove label central frequency
            self.gridLayout_7.removeWidget(self.label_centralFreq)
            self.label_centralFreq.setParent(None)
            # remove line edit central frequency
            self.gridLayout_7.removeWidget(self.lineEdit_centralFreq)
            self.lineEdit_centralFreq.setParent(None)

        elif self.radioButton_quasi.isChecked():
            # Spectrum Model
            self.scrollArea_spectrumModel.setWidget(self.scrollAreaWidgetContents_spectrumModel)
            self.gridLayout_7.addWidget(self.scrollArea_spectrumModel,39, 0, 1, 2)
            # remove label central frequency
            self.gridLayout_7.removeWidget(self.label_centralFreq)
            self.label_centralFreq.setParent(None)
            # remove line edit central frequency
            self.gridLayout_7.removeWidget(self.lineEdit_centralFreq)
            self.lineEdit_centralFreq.setParent(None)

        elif self.radioButton_1freq.isChecked():
            self.gridLayout_7.removeWidget(self.scrollArea_spectrumModel)
            self.scrollArea_spectrumModel.setParent(None)
            # add label central frequency
            self.gridLayout_7.addWidget(self.label_centralFreq, 38, 0, 1, 1)
            #add line edit central frequency
            self.gridLayout_7.addWidget(self.lineEdit_centralFreq, 38, 1, 1, 1)
            # setting label for frequency
            _translate = QtCore.QCoreApplication.translate
            self.label_centralFreq.setText(_translate("MainWindow", "Angular Frequency (rad/s):"))
        else:
            # remove label central frequency
            self.gridLayout_7.removeWidget(self.label_centralFreq)
            self.label_centralFreq.setParent(None)
            # remove line edit central frequency
            self.gridLayout_7.removeWidget(self.lineEdit_centralFreq)
            self.lineEdit_centralFreq.setParent(None)
            self.gridLayout_7.removeWidget(self.scrollArea_spectrumModel)
            self.scrollArea_spectrumModel.setParent(None)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # initial parameters
    log_txt    = "" # log file
    debug      = True
    appname    = "PyWolf 1.0"

    # time
    now        = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    double_bar = "=========================================================="
    output_txt = double_bar+"\n >> "+str(appname)+""+" "*10+"\n"+ double_bar  # to be displayed in app
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
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow,appname,rect,current_dir,log_txt,output_txt)
    MainWindow.show()



    sys.exit(app.exec_())
