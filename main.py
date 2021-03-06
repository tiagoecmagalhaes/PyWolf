"""
PyWolf version 1.0

*
Software to perform simulations of the propagation of partially coherent light
using parallel computing devices through PyOpenCL
*

Tiago E. C. Magalhaes
2021
"""


#===============================================================================
# Importing Packages
#===============================================================================

# PyQT5:
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QInputDialog, QFileDialog, QLabel, QHBoxLayout

# Numpy
import numpy
from numpy import ones

# Functools
import functools

# Decimal
from decimal import Decimal

# Matplotlib
from matplotlib import rc

# PyOpenCL
import pyopencl

# OS
import os
from os import getcwd, chdir

# Sys
import sys

# psutil - for RAM
import psutil

# Glob
import glob

# Adding directories to import packages
current_dir = os.getcwd()
sys.path.append(current_dir+"\\plot_functions\\")
sys.path.append(current_dir+"\\app_functions\\")
sys.path.append(current_dir+"\\styles\\")
sys.path.append(current_dir+"\\logos\\")

# PyWolf packages
from palettes import *
from fonts import *
from color import *
from platdev import *
from testPars import *
from startSim import *
from mainFunctions import *
from save_load import *
from windowPlot_sourceSpectrumPreview import *

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================



#===============================================================================
# Object - PyQT5 Window
#===============================================================================
class Ui_MainWindow(QMainWindow):

    def setupUi(self, MainWindow,appname,rect,current_dir,log_txt,output_txt):

        #=======================================================================
        # parameters
        #=======================================================================
        # version
        self.version = "PyWolf v1.00"

        # simulation successful
        self.sim = False

        # Spectrum Plot Showed
        self.source_spec_plot = False
        self.d_omega = None

        # load project
        self.final_list = None

        # messages
        self.warning_fresnel = False

        self.log_txt     = log_txt
        self.output_txt  = output_txt
        self.rect        = rect
        self.current_dir = current_dir

        self.simulationFinish = False

        # spatial resolution
        self.dx_list=[]

        # directories
        self.dir_examples = None

        # resize
        #self.resized.connect(self.update_resize)
        #self.resizeEvent(self.update_resize)

        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================

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


        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logos/wolf_icon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Central Widget
        #=======================================================================
        # MainWindow -> Central Widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # adding grid to central widget
        self.gridLayout_main = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_main.setObjectName("gridLayout_main")
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # groupBox
        #=======================================================================
        # MainWindow -> Central Widget -> groupBox Project

        # adding groupbox to central widget
        self.groupBox_project = QtWidgets.QGroupBox(self.centralwidget)

        # settings
        self.groupBox_project.setFont(font_title)
        self.groupBox_project.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_project.setCheckable(False)
        self.groupBox_project.setObjectName("groupBox_project")
        self.groupBox_project.setPalette(palette_groupBoxProject)

        # creating layout
        self.gridLayout_main_project = QtWidgets.QGridLayout(self.groupBox_project)
        self.gridLayout_main_project.setObjectName("gridLayout_main_project")

        # background color
        ##self.groupBox_project.setStyleSheet('QGroupBox:title {color: rgb(255, 255, 255);}')
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # gridLayout Project
        #=======================================================================
        # MainWindow -> Central Widget -> groupBox Project -> gridLayout Project

        # Creating grid layout for the project
        self.gridLayout_project = QtWidgets.QGridLayout()
        self.gridLayout_project.setObjectName("gridLayout_project")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_project.addItem(spacerItem, 1, 1, 1, 1)

        # Defines the height of line 1 of the layout
        ##self.gridLayout_project.setRowMinimumHeight(1, int(0.5*self.rect.height()))
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Message Scroll Area Color palette #
        #=======================================================================
        # MainWindow -> Central Widget -> groupBox project -> Message area

        # To define
        ###self.gridLayout_project.setRowStretch(1, int(self.rect.height()*0.7))

        # Creating Widget for Message area
        self.scrollArea_messages = QtWidgets.QScrollArea(self.groupBox_project)

        # Customizing
        self.scrollArea_messages.setPalette(palette_messageArea)
        self.scrollArea_messages.setWidgetResizable(True)
        self.scrollArea_messages.setObjectName("scrollArea_messages")
        ##*self.scrollArea_messages.setMaximumHeight(2*rect.height()/10)

        # Size
        percentage = 0.22
        self.scrollArea_messages.setMaximumHeight(int(MainWindow.frameGeometry().height())*percentage)

        # Scroll Area Message
        self.scrollAreaWidgetContents_messages = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_messages.setObjectName("scrollAreaWidgetContents_9")

        # Creating gridLayout in Scroll Area
        self.gridLayout_messages = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_messages)
        self.gridLayout_messages.setObjectName("gridLayout_messages")

        # Adding Scroll Area Messages do Project
        self.gridLayout_project.addWidget(self.scrollArea_messages, 0, 2, 1, 1)

        # scrollArea_messages -> scrollAreaWidgetContents_messages -> gridLayout_messages
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Output Text Box
        #=======================================================================
        # scrollArea_messages -> scrollAreaWidgetContents_messages -> textBrowser

        # Creating text browser
        self.textBrowser = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents_messages)
        self.textBrowser.setPalette(palette_outputText)
        ##*self.textBrowser.setMinimumHeight(2*rect.height()/14)
        ##*self.textBrowser.setMaximumHeight(2*rect.height()/12.5)

        # adding font
        self.textBrowser.setFont(font_outText)

        # adding to grid layout
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_messages.addWidget(self.textBrowser, 1, 0, 1, 1)

        # adding text
        self.textBrowser.append(str(output_txt))
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Adding Messages to Project Layout
        #=======================================================================
        # creatins spacers
        ##spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        ##spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        # adding spacer to gridLayout messages
        ##self.gridLayout_messages.addItem(spacerItem2, 2, 0, 1, 1)

        # set <scrollAreaWidgetContents_messages> to <scrollArea_messages>
        self.scrollArea_messages.setWidget(self.scrollAreaWidgetContents_messages)

        # adding things to gridLayout project
        ##self.gridLayout_project.addItem(spacerItem3, 0, 1, 1, 1)
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Matplotlib Scroll Area Color Palette
        #=======================================================================
        stylesheet_pywolf = """

            background-image: url(logos/wolf.png);

            background-position: upper center;
            background-repeat: no-repeat;
        """

        # Creating Scroll Area Matplotlib
        self.scrollArea_matplot = QtWidgets.QScrollArea(self.groupBox_project)

        # Customizing
        self.scrollArea_matplot.setPalette(palette_matplotScroll)
        self.scrollArea_matplot.setWidgetResizable(True)
        self.scrollArea_matplot.setObjectName("scrollArea_matplot")

        # Creating Widget
        self.scrollAreaWidgetContents_plots = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_plots.setObjectName("scrollAreaWidgetContents_plots")

        # Setting Widget to scrollArea_matplot
        self.scrollArea_matplot.setWidget(self.scrollAreaWidgetContents_plots)

        # Grid Layout matplot
        self.gridLayout_matplot = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_plots)
        self.gridLayout_matplot.setObjectName("gridLayout_matplot")

        # Adding Grid Layout
        self.gridLayout_project.addWidget(self.scrollArea_matplot, 1, 2, 4, 1)

        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Table with Plots - Widget
        #=======================================================================

        # scrollAreaWidgetContents_plots -> tabWidget_plots

        # Creating Tav Widget
        self.tabWidget_plots = QtWidgets.QTabWidget(self.scrollAreaWidgetContents_plots)

        # Customizing
        self.tabWidget_plots.setPalette(palette_TabPlots)
        self.tabWidget_plots.setObjectName("tabWidget_plots")
        #self.tabWidget_plots.setMinimumHeight(2*self.rect.height()/3)
        self.tabWidget_plots.setFont(font_semititle)

        # adding tabWidget plots to gridlayout matplot
        self.gridLayout_matplot.addWidget(self.tabWidget_plots, 10,0,20,20)

        self.tabWidget_plots.setStyleSheet(stylesheet_pywolf)
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # List of tables in Tab Plots
        #=======================================================================

        # list of tabs
        self.list_of_tabs = []

        # list of grids of tabs
        self.list_grid_tabs = []
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Scroll Area Section Parameters
        #=======================================================================
        # Scroll Area section parameters - Creation
        self.scrollArea_sectionParams = QtWidgets.QScrollArea(self.groupBox_project)

        # Customizing
        self.scrollArea_sectionParams.setPalette(palette_parSection)
        self.scrollArea_sectionParams.setWidgetResizable(True)
        self.scrollArea_sectionParams.setObjectName("scrollArea_sectionParams")
        self.scrollArea_sectionParams.setMaximumWidth(int(rect.width()*0.30))

        # Widget Contents
        self.scrollAreaWidgetContents_numPlanes = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_numPlanes.setGeometry(QtCore.QRect(0, 0, 445, 1780))
        self.scrollAreaWidgetContents_numPlanes.setObjectName("scrollAreaWidgetContents_numPlanes")

        # Grid Layout
        self.gridLayout_7 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_numPlanes)
        self.gridLayout_7.setObjectName("gridLayout_7")
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


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
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Text Box to Write
        #=======================================================================
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
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Scroll Area FFT ZEROP PADDING
        #=======================================================================
        self.scrollArea_FFT = QtWidgets.QScrollArea(self.scrollAreaWidgetContents_numPlanes)
        self.scrollArea_FFT.setWidgetResizable(True)
        self.scrollArea_FFT.setObjectName("ScrollArea_FFT")
        self.scrollArea_FFT.setMinimumHeight(rect.height()/6.)

        self.scrollAreaWidgetContents_FFT = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_FFT.setGeometry(QtCore.QRect(0, 0, 421, 85))
        self.scrollAreaWidgetContents_FFT.setObjectName("scrollAreaWidgetContents_FFT")

        self.gridLayout_FFT = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_FFT)
        self.gridLayout_FFT.setObjectName("gridLayout_FFT")
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


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
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


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
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


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
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Scroll Area CSDA from file
        #=======================================================================
        self.scrollArea_fromFile = QtWidgets.QScrollArea(self.scrollAreaWidgetContents_numPlanes)
        self.scrollArea_fromFile.setWidgetResizable(True)
        self.scrollArea_fromFile.setObjectName("ScrollArea_fromFile")
        self.scrollArea_fromFile.setMinimumHeight(rect.height()/6.)

        self.scrollAreaWidgetContents_fromFile = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_fromFile.setGeometry(QtCore.QRect(0, 0, 421, 85))
        self.scrollAreaWidgetContents_fromFile.setObjectName("scrollAreaWidgetContents_fromFile")

        self.gridLayout_fromFile = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_fromFile)
        self.gridLayout_fromFile.setObjectName("gridLayout_fromFile")
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


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
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


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
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Scroll Spectral Density
        #=======================================================================
        self.scrollArea_SpecDensity = QtWidgets.QScrollArea(self.scrollAreaWidgetContents_numPlanes)
        self.scrollArea_SpecDensity.setWidgetResizable(True)
        self.scrollArea_SpecDensity.setObjectName("ScrollArea_geometry")
        self.scrollArea_SpecDensity.setMinimumHeight(rect.height()/6.)

        self.scrollAreaWidgetContents_SpecDensity = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_SpecDensity.setGeometry(QtCore.QRect(0, 0, 421, 85))
        self.scrollAreaWidgetContents_SpecDensity.setObjectName("scrollAreaWidgetContents_SpecDensity")

        self.gridLayout_SpecDensity = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_SpecDensity)
        self.gridLayout_SpecDensity.setObjectName("gridLayout_SpecDensity")
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


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
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


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
        # Optics Function and Parameters | area, widget contents and gridlayout
        #-----------------------------------------------------------------------
        # list of scrollArea for optical device functions and parameters
        self.scrollArea_optics_list = []

        # list of scroll area widgets contents for optics
        self.scrollAreaWidgetContents_optics_list = []

        # list of gridlayout for optics
        self.gridLayout_optics_list=[]
        #_______________________________________________________________________


        #-----------------------------------------------------------------------
        # Spin Box
        #-----------------------------------------------------------------------
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
        """
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.scrollAreaWidgetContents_numPlanes)
        self.dateTimeEdit.setFont(font_normalLabel)
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.gridLayout_7.addWidget(self.dateTimeEdit, 85, 0, 1, 2)
        self.dateTimeEdit.setMaximumWidth(size_schedule(self))
        self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        """
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Computational Variables
        #=======================================================================

        self.list_filesGeom = [] # list containing information on geometry functions [module name and dir]
        self.list_filesCoh = []  # list containing information on coherence functions [module name and dir]

        # directories
        self.dirName       = None  # saved results directory
        self.dirSourceGeo  = None  # directory with source image
        self.dirSourceCSDA  = None # directory with source CSDA

        # present time
        self.nowTime = datetime.now()

        # directory name
        self.saveDirName = None

        # minimum size for combo boxes
        self.minwidth_combo = rect.width()/7

        # max width size for combo boxes when VIEWING
        self.maxWidthView_combo = rect.width()/2
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #-----------------------------------------------------------------------
        # Spectrum Models and parameters | list, line Edit
        #-----------------------------------------------------------------------
        self.specModelsFunc = []

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

        # Coherence Models Parameters ex: [ ["a"],["a","b"] ]
        self.cohModelPar_list = []

        # Coherence Models Line Edit Parameters  ex. [ OBJECT, OBJECT]
        self.cohModel_lineEditParameters = []
        #_______________________________________________________________________


        #-----------------------------------------------------------------------
        # Spectral Density Models and parameters | list, line Edit
        #-----------------------------------------------------------------------

        # Spectral Density Models List ex: [ ["GSM", OBJECT] , ["GSM2", OBJECT] ]
        self.specDenModel_list = []

        # Spectral Density Models Parameters ex: [ ["a"],["a","b"] ]
        self.specDenPar_list = []

        # Spectral Density Models Line Edit Parameters  ex. [ OBJECT, OBJECT]
        self.specDen_lineEditParameters = []
        #_______________________________________________________________________


        #-----------------------------------------------------------------------
        # Pupil Geometry Function and Parameters | list, Line Edits
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
        # Optical Devices Function, Parameters and Line Edits
        #-----------------------------------------------------------------------
        # Optical Devices Models List
        self.optDeviceFunc_list = []

        for i in range(0,self.max_numPlanes):
            self.optDeviceFunc_list.append([])

        # Optical Device Parameters Models List
        ## self.optDevicePars_list
        self.optDeviceFuncPars_list = []
        for i in range(0,self.max_numPlanes):
            self.optDeviceFuncPars_list.append([])

        # Pupil Geometry Line Edit Parameters  ex. [ OBJECT, OBJECT]
        self.optDevicePars_lineEditParameters = []
        for i in range(0,self.max_numPlanes):
            self.optDevicePars_lineEditParameters.append([])
        #_______________________________________________________________________


        #=======================================================================
        # Labels
        #=======================================================================

        # just a bar
        self.bar = "------------------------------------------------"

        # label simulation name
        self.label_projName = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_projName.setFont(font_normalLabel)
        self.label_projName.setObjectName("label")
        self.gridLayout_7.addWidget(self.label_projName, 0, 0, 1, 1)

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
        self.gridLayout_save.addWidget(self.label_saveFile, 6, 0, 1, 1)

        # Label N
        self.label_N = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_N.setFont(font_normalLabel)
        self.label_N.setObjectName("label_N")
        self.gridLayout_7.addWidget(self.label_N, 15, 0, 1, 1)

        # Label NZ
        self.label_NZ = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_NZ.setFont(font_normalLabel)
        self.label_NZ.setObjectName("label_NZ")
        self.gridLayout_FFT.addWidget(self.label_NZ, 1, 0, 1, 1)
        self.label_NZ.setText("Total matrix size (>N): ")
        self.label_NZ.setVisible(False)

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

        # label Prop Spec Model
        self.label_propSpecModel = QtWidgets.QLabel(self.scrollAreaWidgetContents_propQuantity)
        self.label_propSpecModel.setPalette(palette_parSection)
        self.label_propSpecModel.setFont(font_normalLabel)
        self.label_propSpecModel.setObjectName("label_propSpecModel")
        self.gridLayout_propQuantity.addWidget(self.label_propSpecModel, 2, 0, 1, 3)

        # label Theta
        self.label_theta = QtWidgets.QLabel(self.scrollAreaWidgetContents_propQuantity)
        self.label_theta.setPalette(palette_parSection)
        self.label_theta.setFont(font_normalLabel)
        self.label_theta.setObjectName("label_theta")
        self.gridLayout_propQuantity.addWidget(self.label_theta, 3, 0, 1, 3)

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

        # label use Spectral Density?
        self.label_useSpecDen = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_useSpecDen.setPalette(palette_parSection)
        self.label_useSpecDen.setFont(font_normalLabel)
        self.label_useSpecDen.setObjectName("label_useSpecDen")
        self.gridLayout_7.addWidget(self.label_useSpecDen, 55, 0, 1, 1)

        # label spectral density model
        self.label_specDenModel = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_specDenModel.setPalette(palette_parSection)
        self.label_specDenModel.setFont(font_normalLabel)
        self.label_specDenModel.setObjectName("label_specDenModel")
        self.gridLayout_SpecDensity.addWidget(self.label_specDenModel, 2, 0, 1, 1)
        self.label_specDenModel.setText("Spectral Density Model: ")
        self.specDenModel_labelParameters = []

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

        # labels for optical device function
        self.label_optDeviceFunc_list = []

        # labels pupil geometric model
        self.optDeviceFunc_labelParameters = []
        for i in range(0,self.max_numPlanes):
            self.optDeviceFunc_labelParameters.append([])

        """
        # label Start Simulation
        self.label_startSim = QtWidgets.QLabel(self.scrollAreaWidgetContents_numPlanes)
        self.label_startSim.setPalette(palette_titles)
        self.label_startSim.setFont(font_title)
        self.label_startSim.setAlignment(QtCore.Qt.AlignCenter)
        self.label_startSim.setObjectName("label_2")
        self.gridLayout_7.addWidget(self.label_startSim, 74, 0, 1, 2)
        """

        # Label Insert Comments
        self.label_insertComments = QtWidgets.QLabel(self.scrollAreaWidgetContents_textBox)
        self.label_insertComments.setFont(font_normalLabel)
        self.label_insertComments.setObjectName("label_insertComments")
        self.gridLayout_textBox.addWidget(self.label_insertComments, 0, 0, 1, 1)
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


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

        """
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
        """
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Spaces
        #=======================================================================

        # space 5
        ##spacerItem0 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        ##self.gridLayout_7.addItem(spacerItem0, 3, 0, 1, 2)

        # space 4
        ##spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        ##self.gridLayout_7.addItem(spacerItem4, 52, 0, 1, 2)

        # space 5
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem5, 58, 0, 1, 2)

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
        #spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.gridLayout_7.addItem(spacerItem13, 10, 0, 1, 2)

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
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


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
        self.lineEdit_saveFiles = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_save)
        self.lineEdit_saveFiles.setFont(font_normalLabel)
        self.lineEdit_saveFiles.setObjectName("Save File")
        self.lineEdit_saveFiles.setStyleSheet('background: '+colortxt_textEdit)
        self.gridLayout_save.addWidget(self.lineEdit_saveFiles, 6, 1, 1, 1)
        results_directory = str(current_dir)+'\\results'
        self.saveDirName = results_directory
        self.lineEdit_saveFiles.setText(results_directory)
        # start at the line 0:
        self.lineEdit_saveFiles.setCursorPosition(0)
        # setting size
        self.lineEdit_saveFiles.setMaximumWidth(self.minwidth_combo)

        # line open geometry matrix source
        self.lineEdit_dirGeoMatrix = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_fromFile)
        self.lineEdit_dirGeoMatrix.setFont(font_normalLabel)
        self.lineEdit_dirGeoMatrix.setObjectName("Save File")
        self.lineEdit_dirGeoMatrix.setStyleSheet('background: '+colortxt_textEdit)
        self.gridLayout_fromFile.addWidget(self.lineEdit_dirGeoMatrix, 0, 1, 1, 1)
        self.lineEdit_dirGeoMatrix.setText(results_directory)
        # start at the line 0:
        self.lineEdit_dirGeoMatrix.setCursorPosition(0)
        # setting size
        self.lineEdit_dirGeoMatrix.setMaximumWidth(self.minwidth_combo)

        # line open CSDA matrix source
        self.lineEdit_dirCSDAmatrix = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_fromFile)
        self.lineEdit_dirCSDAmatrix.setFont(font_normalLabel)
        self.lineEdit_dirCSDAmatrix.setObjectName("dirCSDAmatrix")
        self.lineEdit_dirCSDAmatrix.setStyleSheet('background: '+colortxt_textEdit)
        self.gridLayout_fromFile.addWidget(self.lineEdit_dirCSDAmatrix, 2, 1, 1, 1)
        self.lineEdit_dirCSDAmatrix.setText(results_directory)
        # start at the line 0:
        self.lineEdit_dirCSDAmatrix.setCursorPosition(0)
        # setting size
        self.lineEdit_dirCSDAmatrix.setMaximumWidth(self.minwidth_combo)

        # text edit Angle
        self.lineEdit_theta = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_propQuantity)
        self.lineEdit_theta.setFont(font_normalLabel)
        self.lineEdit_theta.setObjectName("lineEdit_N")
        self.lineEdit_theta.setStyleSheet('background: '+colortxt_textEdit)
        self.gridLayout_propQuantity.addWidget(self.lineEdit_theta, 3, 1, 1, 1)
        self.lineEdit_theta.setMaximumWidth(size_entries(self))
        self.lineEdit_theta.textChanged.connect(self.updateSpaceRes)
        self.lineEdit_theta.setText("1e-3")

        # text edit in N
        self.lineEdit_N = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_numPlanes)
        self.lineEdit_N.setFont(font_normalLabel)
        self.lineEdit_N.setObjectName("lineEdit_N")
        self.lineEdit_N.setStyleSheet('background: '+colortxt_textEdit)
        self.gridLayout_7.addWidget(self.lineEdit_N, 15, 1, 1, 1)
        self.lineEdit_N.setMaximumWidth(size_entries(self))
        self.lineEdit_N.textChanged.connect(self.updateSpaceRes)
        self.lineEdit_N.setText("80")

        # text edit in NZ
        self.lineEdit_NZ = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_FFT)
        self.lineEdit_NZ.setFont(font_normalLabel)
        self.lineEdit_NZ.setObjectName("lineEdit_NZ")
        self.lineEdit_NZ.setStyleSheet('background: '+colortxt_textEdit)
        self.gridLayout_FFT.addWidget(self.lineEdit_NZ, 1, 1, 1, 1)
        self.lineEdit_NZ.setMaximumWidth(size_entries(self))
        self.lineEdit_NZ.setText("256")
        self.lineEdit_NZ.setVisible(False)
        self.lineEdit_NZ.textChanged.connect(self.updateSpaceRes)

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
        self.lineEdit_sourceRes = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_numPlanes)
        self.lineEdit_sourceRes.setFont(font_normalLabel)
        self.lineEdit_sourceRes.setObjectName("lineEdit_sourceRes")
        self.lineEdit_sourceRes.setStyleSheet('background: '+colortxt_textEdit)
        self.gridLayout_7.addWidget(self.lineEdit_sourceRes, 47, 1, 1, 1)
        # setting size
        self.lineEdit_sourceRes.textChanged.connect(self.updateSpaceRes)
        self.lineEdit_sourceRes.setText("1e-3")
        self.lineEdit_sourceRes.setMaximumWidth(size_entries(self))

        # line edit text distance for propagation planes
        self.lineEdit_distances_list = []
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


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
        self.comboBox_propQuant.addItem("Degree of coherence & Intensity",1)
        ##self.comboBox_propQuant.addItem("Spectrum",2)
        # setting size
        #self.comboBox_propQuant.setMaximumWidth(self.minwidth_combo)
        """
        self.comboBox_propQuant.setStyleSheet('''*
        QComboBox QAbstractItemView
            {
            min-width: '''+str(self.maxWidthView_combo)+'''px;
            }
        ''')
        """
        self.comboBox_propQuant.currentIndexChanged.connect(self.updatePropQuantity)

        # combo box spectral model
        self.comboBox_specType = QtWidgets.QComboBox(self.scrollAreaWidgetContents_spectrumModel)
        self.comboBox_specType.setFont(font_normalLabel)
        self.comboBox_specType.setObjectName("comboBox_specType")
        self.gridLayout_specModel.addWidget(self.comboBox_specType, 0, 1, 1, 1)
        # setting size
        #self.comboBox_specType.setMaximumWidth(self.minwidth_combo)
        """
        self.comboBox_specType.setStyleSheet('''*
        QComboBox QAbstractItemView
            {
            min-width: '''+str(self.maxWidthView_combo)+'''px;
            }
        ''')
        """
        # action
        self.comboBox_specType.currentIndexChanged.connect(self.updateSpecModelPars)

        # combo box coherence model
        self.comboBox_cohModel = QtWidgets.QComboBox(self.scrollAreaWidgetContents_cohModel)
        self.comboBox_cohModel.setFont(font_normalLabel)
        self.comboBox_cohModel.setObjectName("comboBox_cohModel")
        self.gridLayout_cohModel.addWidget(self.comboBox_cohModel, 0, 1, 1, 1)
        # setting size
        #self.comboBox_cohModel.setMaximumWidth(self.minwidth_combo)
        """
        self.comboBox_cohModel.setStyleSheet('''*
        QComboBox QAbstractItemView
            {
            min-width: '''+str(self.maxWidthView_combo)+'''px;
            }
        ''')
        """
        self.comboBox_cohModel.currentIndexChanged.connect(self.updateCohModelPars)

        # combo box geometry
        self.comboBox_geometry = QtWidgets.QComboBox(self.scrollAreaWidgetContents_geometry)
        self.comboBox_geometry.setFont(font_normalLabel)
        self.comboBox_geometry.setObjectName("comboBox_geometry")
        self.gridLayout_geometry.addWidget(self.comboBox_geometry, 0, 1, 1, 1)
        # setting size
        #self.comboBox_geometry.setMaximumWidth(self.minwidth_combo)
        """
        self.comboBox_geometry.setStyleSheet('''*
        QComboBox QAbstractItemView
            {
            min-width: '''+str(self.maxWidthView_combo)+'''px;
            }
        ''')
        """
        # action
        self.comboBox_geometry.currentIndexChanged.connect(self.updateGeometryPars)


        # combo box Spectral Density Model
        self.comboBox_specDenModel = QtWidgets.QComboBox(self.scrollAreaWidgetContents_SpecDensity)
        self.comboBox_specDenModel.setFont(font_normalLabel)
        self.comboBox_specDenModel.setObjectName("comboBox_geometry")
        self.gridLayout_SpecDensity.addWidget(self.comboBox_specDenModel, 2, 1, 1, 1)
        # setting size
        #self.comboBox_specDenModel.setMaximumWidth(self.minwidth_combo)
        """
        self.comboBox_specDenModel.setStyleSheet('''*
        QComboBox QAbstractItemView
            {
            min-width: '''+str(self.maxWidthView_combo)+'''px;
            }
        ''')
        """
        # action
        self.comboBox_specDenModel.currentIndexChanged.connect(self.updateSpecDenPars)

        # list of comboBoxes with pupil functions for propagation planes
        self.comboBox_pupilGeom_list = []

        # list of comboBoxes with optical devices functions for propagation planes
        self.comboBox_optDeviceFunc_list = []
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


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
        ##self.gridLayout_7.addItem(spacerItem8, 2, 0, 1, 2)
        # setting checked by default
        self.checkBox_pyopencl.setChecked(True)

        # checkbox fft zero padding
        self.checkBox_FFT = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_FFT)
        self.checkBox_FFT.setFont(font_normalLabel)
        self.checkBox_FFT.setObjectName("checkBox_FFT")
        self.gridLayout_FFT.addWidget(self.checkBox_FFT, 0, 0, 1, 1)
        self.checkBox_FFT.setChecked(False)
        self.checkBox_FFT.setText("Use FFT Zero Padding?")
        self.checkBox_FFT.stateChanged.connect(self.zeroPadingOptions)

        # checkbox save
        self.checkBox_save = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_save)
        self.checkBox_save.setFont(font_normalLabel)
        self.checkBox_save.setObjectName("checkBox_save")
        self.gridLayout_save.addWidget(self.checkBox_save, 0, 0, 1, 1)
        self.checkBox_save.setChecked(False)

        # checkbox save source CSDA
        self.checkBox_saveSourceCSDA = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_save)
        self.checkBox_saveSourceCSDA.setFont(font_normalLabel)
        self.checkBox_saveSourceCSDA.setObjectName("checkBox_saveSourceCSDA")
        self.gridLayout_save.addWidget(self.checkBox_saveSourceCSDA, 2, 0, 1, 1)

        # checkbox save propagation CSDA
        self.checkBox_savePropCSDA = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_save)
        self.checkBox_savePropCSDA.setFont(font_normalLabel)
        self.checkBox_savePropCSDA.setObjectName("checkBox_saveSourceCSDA")
        self.gridLayout_save.addWidget(self.checkBox_savePropCSDA, 4, 0, 1, 1)

        # checkBox_geoFromFile
        self.checkBox_geoFromFile = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_fromFile)
        self.checkBox_geoFromFile.setPalette(palette_parSection)
        self.checkBox_geoFromFile.setFont(font_normalLabel)
        self.checkBox_geoFromFile.setObjectName("checkBox_geoFromFile")
        self.gridLayout_fromFile.addWidget(self.checkBox_geoFromFile, 0, 0, 1, 1)
        self.checkBox_geoFromFile.stateChanged.connect(self.updateGeoFromFile)

        # checkBox_CSDAFromFile
        self.checkBox_CSDAFromFile = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_fromFile)
        self.checkBox_CSDAFromFile.setPalette(palette_parSection)
        self.checkBox_CSDAFromFile.setFont(font_normalLabel)
        self.checkBox_CSDAFromFile.setObjectName("checkBox_CSDAFromFile")
        self.gridLayout_fromFile.addWidget(self.checkBox_CSDAFromFile, 2, 0, 1, 1)
        self.checkBox_CSDAFromFile.stateChanged.connect(self.updateCSDAFromFile)
        self.checkBox_CSDAFromFile.setText("CSDA from File (4D array '.npy')")

        # checkbox debug
        self.checkBox_debug = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_numPlanes)
        self.checkBox_debug.setPalette(palette_parSection)
        self.checkBox_debug.setFont(font_normalLabel)
        self.checkBox_debug.setObjectName("checkBox_debug")
        self.gridLayout_7.addWidget(self.checkBox_debug, 14, 0, 1, 1)

        # combo box Spectrum Propagation Models
        self.comboBox_specPropModels = QtWidgets.QComboBox(self.scrollAreaWidgetContents_propQuantity)
        self.comboBox_specPropModels.setFont(font_normalLabel)
        self.comboBox_specPropModels.setObjectName("comboBox_specPropModels")
        self.gridLayout_propQuantity.addWidget(self.comboBox_specPropModels, 2, 1, 1, 3)
        self.comboBox_specPropModels.addItem("Frequency-Independent Model",0)
        # setting size
        #self.comboBox_specPropModels.setMaximumWidth(self.minwidth_combo)
        """
        self.comboBox_specPropModels.setStyleSheet('''*
        QComboBox QAbstractItemView
            {
            min-width: '''+str(self.maxWidthView_combo)+'''px;
            }
        ''')
        """
        #self.comboBox_specPropModels.currentIndexChanged.connect(self.updatePropQuantity)

        # checkBox for Spectral Density
        self.checkBox_specDen = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_numPlanes)
        self.checkBox_specDen.setPalette(palette_parSection)
        self.checkBox_specDen.setFont(font_normalLabel)
        self.checkBox_specDen.setObjectName("checkBox_specDen")
        self.gridLayout_7.addWidget(self.checkBox_specDen, 55, 1, 1, 1)
        self.checkBox_specDen.stateChanged.connect(self.update_specDenArea)

        # CheckBox for far-field of planes
        self.checkBox_farfied_list = []

        # CheckBox for Pupil
        self.checkBox_pupil_list = []

        # CheckBox for Optics for all planes
        self.checkBox_optics_list = []

        """
        # checkbox schedule simulation
        self.checkBox_schedule = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_numPlanes)
        self.checkBox_schedule.setFont(font_normalLabel)
        self.checkBox_schedule.setObjectName("checkBox")
        self.gridLayout_7.addWidget(self.checkBox_schedule, 84, 0, 1, 2)
        """
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Radio buttons
        #=======================================================================

        # -- Radio Button Quasi-monochromatic --
        self.radioButton_quasi = QtWidgets.QRadioButton(self.scrollAreaWidgetContents_numPlanes)
        self.radioButton_quasi.setFont(font_normalLabel)
        self.radioButton_quasi.setObjectName("radioButton_quasi")
        self.gridLayout_7.addWidget(self.radioButton_quasi, 36, 0, 1, 1)
        self.radioButton_quasi.toggled.connect(self.update_specPars)
        self.radioButton_quasi.setHidden(True)

        # -- Radio Button Polychromatic --
        self.radioButton_poly = QtWidgets.QRadioButton(self.scrollAreaWidgetContents_numPlanes)
        self.radioButton_poly.setFont(font_normalLabel)
        self.radioButton_poly.setObjectName("radioButton_2")
        self.gridLayout_7.addWidget(self.radioButton_poly, 37, 0, 1, 1)
        self.radioButton_poly.toggled.connect(self.update_specPars)
        # hide
        self.radioButton_poly.setHidden(True)

        # -- Radio Button Single Frequency --
        self.radioButton_1freq = QtWidgets.QRadioButton(self.scrollAreaWidgetContents_numPlanes)
        self.radioButton_1freq.setFont(font_normalLabel)
        self.radioButton_1freq.setObjectName("radioButton_1freq")
        self.gridLayout_7.addWidget(self.radioButton_1freq, 35, 0, 1, 1)
        self.radioButton_1freq.toggled.connect(self.update_specPars)
        self.radioButton_1freq.setChecked(True)
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Tool buttons
        #=======================================================================

        # tool button save file
        self.toolButton_saveFile = QtWidgets.QToolButton(self.scrollAreaWidgetContents_save)
        self.toolButton_saveFile.setFont(font_normalLabel)
        self.toolButton_saveFile.setObjectName("toolButton_saveFile")
        self.gridLayout_save.addWidget(self.toolButton_saveFile, 6, 2, 1, 1)
        # action
        self.toolButton_saveFile.clicked.connect(self.openFileNameDialog_saveDir)

        # tool button source file
        self.toolButton_geoFromFile = QtWidgets.QToolButton(self.scrollAreaWidgetContents_fromFile)
        self.toolButton_geoFromFile.setFont(font_normalLabel)
        self.toolButton_geoFromFile.setObjectName("toolButton_geoFromFile")
        self.gridLayout_fromFile.addWidget(self.toolButton_geoFromFile, 0, 3, 1, 1)
        self.toolButton_geoFromFile.clicked.connect(self.openFileNameDialog_openGeo)

        # tool button CSDA from file
        self.toolButton_CSDAfromfile = QtWidgets.QToolButton(self.scrollAreaWidgetContents_fromFile)
        self.toolButton_CSDAfromfile.setFont(font_normalLabel)
        self.toolButton_CSDAfromfile.setObjectName("toolButton_CSDAfromfile")
        self.gridLayout_fromFile.addWidget(self.toolButton_CSDAfromfile, 2, 3, 1, 1)
        self.toolButton_CSDAfromfile.clicked.connect(self.openFileNameDialog_openCSDA)
        self.toolButton_CSDAfromfile.setText("...")
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Push buttons
        #=======================================================================


        #***********************************************************************
        # Button Start
        #***********************************************************************
        ##self.pushButton_start = QtWidgets.QPushButton(self.scrollAreaWidgetContents_numPlanes)
        self.pushButton_start = QtWidgets.QPushButton(self.groupBox_project)
        ##self.pushButton_start = QtWidgets.QPushButton(self.gridLayout_main_project)

        # info
        self.pushButton_start.setToolTip('Click here to start the simulation')

        # style
        self.pushButton_start.setPalette(palette_buttonStart)
        self.pushButton_start.setFont(font_button)
        self.pushButton_start.setObjectName("pushButton_start")
        self.pushButton_start.setMaximumHeight(self.rect.height()/25)
        stylesheet_start = """
        QPushButton{
            background-color: #FFF3C4;
            border-style: outset;
            border-width: 5px;
            /*border-radius: 10px;*/
            border-color: #C29A00;
            font: bold 16px;
            color: #00234C;
            padding: 0px; /* 6px*/
        }
        QPushButton::pressed{
                             background-color : #C29A00;
        }
        """
        self.pushButton_start.setStyleSheet(stylesheet_start)


        # add to grid
        ##self.gridLayout_7.addWidget(self.pushButton_start, 83, 0, 1, 3,alignment=QtCore.Qt.AlignCenter)
        self.gridLayout_project.addWidget(self.pushButton_start, 2, 0, 1, 2)

        # Function
        self.pushButton_start.clicked.connect(self.start_simulation)
        #_______________________________________________________________________


        # Show source spectrum
        self.pushButton_showSpec = QtWidgets.QPushButton(self.scrollAreaWidgetContents_spectrumModel)
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Add itesm to main grid Layout (7)
        #=======================================================================

        # textBox
        self.scrollArea_textBox.setWidget(self.scrollAreaWidgetContents_textBox)
        self.gridLayout_7.addWidget(self.scrollArea_textBox, 2, 0, 1, 2)

        # FFT
        self.scrollArea_FFT.setWidget(self.scrollAreaWidgetContents_FFT)
        self.gridLayout_7.addWidget(self.scrollArea_FFT,17, 0, 1, 2)

        # Save
        self.scrollArea_save.setWidget(self.scrollAreaWidgetContents_save)
        self.gridLayout_7.addWidget(self.scrollArea_save,11, 0, 1, 2)

        # Propagation quantity
        self.scrollArea_propQuantity.setWidget(self.scrollAreaWidgetContents_propQuantity)
        self.gridLayout_7.addWidget(self.scrollArea_propQuantity,25, 0, 1, 2)

        # Geometry Model
        self.scrollArea_geometry.setWidget(self.scrollAreaWidgetContents_geometry)
        self.gridLayout_7.addWidget(self.scrollArea_geometry,49, 0, 1, 2)

        # From File
        self.scrollArea_fromFile.setWidget(self.scrollAreaWidgetContents_fromFile)
        self.gridLayout_7.addWidget(self.scrollArea_fromFile,48, 0, 1, 2)

        # Coherence Model
        self.scrollArea_cohModel.setWidget(self.scrollAreaWidgetContents_cohModel)
        self.gridLayout_7.addWidget(self.scrollArea_cohModel,51, 0, 1, 2)

        # Spectral Density
        self.scrollArea_SpecDensity.setWidget(self.scrollAreaWidgetContents_SpecDensity)
        self.gridLayout_7.addWidget(self.scrollArea_SpecDensity,56, 0, 1, 2)

        # Spectrum Model
        self.scrollArea_spectrumModel.setWidget(self.scrollAreaWidgetContents_spectrumModel)
        self.gridLayout_7.addWidget(self.scrollArea_spectrumModel,39, 0, 1, 2)

        # Simulation Parameters
        self.scrollArea_sectionParams.setWidget(self.scrollAreaWidgetContents_numPlanes)
        self.gridLayout_project.addWidget(self.scrollArea_sectionParams, 0, 0, 2, 2)

        # Main Project
        self.gridLayout_main_project.addLayout(self.gridLayout_project, 0, 0, 1, 1)

        # Main
        self.gridLayout_main.addWidget(self.groupBox_project, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


        #=======================================================================
        # Menu Bar
        #=======================================================================
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1017, 26))
        self.menubar.setObjectName("menubar")

        # File
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        # Edit
        ##self.menuEdit = QtWidgets.QMenu(self.menubar)
        ##self.menuEdit.setObjectName("menuEdit")

        # Export
        self.menuExport = QtWidgets.QMenu(self.menubar)
        self.menuExport.setObjectName("menuExport")

        # Help
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)

        # File -> New Project
        self.actionNew_Project = QtWidgets.QAction(MainWindow)
        self.actionNew_Project.setObjectName("actionNew_Project")

        # File -> Load Project
        self.actionLoad_Project = QtWidgets.QAction(MainWindow)
        self.actionLoad_Project.setObjectName("actionLoad_Project")
        self.actionLoad_Project.triggered.connect(self.load_project)

        # File -> Save Project
        self.actionSave_Project = QtWidgets.QAction(MainWindow)
        self.actionSave_Project.setObjectName("actionSave_Project")
        self.actionSave_Project.triggered.connect(self.save_project)

        # File -> Examples
        self.subMenu_Examples = QtWidgets.QMenu(self.menubar)
        self.subMenu_Examples.setObjectName("actionNew_Examples")
        self.subMenu_Examples.setTitle("Examples")
        self.action_examples_list = []

        # File -> Exit
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.triggered.connect(self.close_application)

        # Edit -> undo
        ##self.actionUndo = QtWidgets.QAction(MainWindow)
        ##self.actionUndo.setObjectName("actionUndo")
        ##self.actionUndo.setShortcut("Ctrl+Z")

        # Edit -> redo
        ##self.actionRedo = QtWidgets.QAction(MainWindow)
        ##self.actionRedo.setObjectName("actionRedo")
        ##self.actionRedo.setShortcut("Ctrl+Y")

        # Edit -> cut
        ##self.actionCut = QtWidgets.QAction(MainWindow)
        ##self.actionCut.setObjectName("actionCut")
        ##self.actionCut.setShortcut("Ctrl+D")

        # Edit -> copy
        ##self.actionCopy = QtWidgets.QAction(MainWindow)
        ##self.actionCopy.setObjectName("actionCopy")
        ##self.actionCopy.setShortcut("Ctrl+C")
        ##self.actionCopy.triggered.connect(QtWidgets.QLineEdit.copy(self))

        # Edit -> delete
        ##self.actionDelete = QtWidgets.QAction(MainWindow)
        ##self.actionDelete.setObjectName("actionDelete")

        # Edit -> Paste
        ##self.actionPaste = QtWidgets.QAction(MainWindow)
        ##self.actionPaste.setObjectName("actionPaste")
        ##self.actionPaste.setShortcut("Ctrl+V")

        # About -> Manual
        self.actionManual = QtWidgets.QAction(MainWindow)
        self.actionManual.setObjectName("actionManual")

        # About -> About
        self.actionAbout = self.create_action("&About",shortcut='F1',slot=self.on_about,tip='About this software')
        self.actionGet_Citation = self.create_action("&About",shortcut='F2',slot=self.on_citation,tip='Citation')

        # Export Data
        self.actionExport_Data = QtWidgets.QAction(MainWindow)
        self.actionExport_Data.setObjectName("actionExport_Data")
        self.actionExport_Data.triggered.connect(self.save_results)

        # Export source image
        self.actionExport_sourceImage = QtWidgets.QAction(MainWindow)
        self.actionExport_sourceImage.setObjectName("actionExport_sourceImage")
        self.actionExport_sourceImage.setText("Export Source Image")
        self.actionExport_sourceImage.triggered.connect(self.save_sourceImage)

        # Export source CSDA
        self.actionExport_sourceCSDA = QtWidgets.QAction(MainWindow)
        self.actionExport_sourceCSDA.setObjectName("actionExport_sourceCSDA")
        self.actionExport_sourceCSDA.setText("Export Source CSDA")
        self.actionExport_sourceCSDA.triggered.connect(self.save_sourceCSDA)

        # Export propagation image
        self.actionExport_propImage = QtWidgets.QAction(MainWindow)
        self.actionExport_propImage.setObjectName("actionExport_propImage")
        self.actionExport_propImage.setText("Export Propagation Image")
        self.actionExport_propImage.triggered.connect(self.save_propImage)

        # Export prop CSDA
        self.actionExport_propCSDA = QtWidgets.QAction(MainWindow)
        self.actionExport_propCSDA.setObjectName("actionExport_propCSDA")
        self.actionExport_propCSDA.setText("Export Propagated CSDA")
        self.actionExport_propCSDA.triggered.connect(self.save_propCSDA)

        # Adding to File Menu
        self.menuFile.addAction(self.actionNew_Project)
        self.menuFile.addAction(self.actionLoad_Project)
        self.menuFile.addAction(self.actionSave_Project)
        self.menuFile.addSeparator()
        self.menuFile.addMenu(self.subMenu_Examples)
        self.search_examples()
        self.menuFile.addSeparator()
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)

        # Adding to Edit Menu
        ##self.menuEdit.addSeparator()
        ##self.menuEdit.addAction(self.actionUndo)
        ##self.menuEdit.addAction(self.actionRedo)
        ##self.menuEdit.addAction(self.actionCut)
        ##self.menuEdit.addAction(self.actionCopy)
        ##self.menuEdit.addAction(self.actionPaste)
        ##self.menuEdit.addAction(self.actionDelete)

        # Adding to Export Menu
        self.menuExport.addAction(self.actionExport_sourceImage)
        self.menuExport.addAction(self.actionExport_sourceCSDA)
        self.menuExport.addSeparator()
        self.menuExport.addSeparator()
        self.menuExport.addAction(self.actionExport_propCSDA)
        self.menuExport.addAction(self.actionExport_propImage)
        self.menuExport.addSeparator()
        self.menuExport.addSeparator()
        self.menuExport.addAction(self.actionExport_Data)

        # Adding to Help Menu
        self.menuHelp.addAction(self.actionManual)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionGet_Citation)
        self.menubar.addAction(self.menuFile.menuAction())
        ##self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        # last functions:
        self.retranslateUi(MainWindow)
        self.tabWidget_plots.setCurrentIndex(0)
        self.tabWidget_propsystem.setCurrentIndex(0)
        self.updateSpaceRes()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #=======================================================================
        #///////////////////////////////////////////////////////////////////////
        #=======================================================================


    #===========================================================================
    # Methods
    #===========================================================================


    #***************************************************************************
    # Tetting text and titles
    #***************************************************************************

    def retranslateUi(self, MainWindow):
        "Setting text and titles"
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", appname))
        self.groupBox_project.setTitle(_translate("MainWindow", "New Project"))
        self.label_insertComments.setText(_translate("MainWindow", "Insert Comments: "))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "# Write your comments here. They are saved after the simulation.\n"""))
        ##self.label_outMessages.setText(_translate("MainWindow", "Output Messages:"))
        ##self.label_opticalSys.setText(_translate("MainWindow", "Optical System:"))
        ##self.label_Plots.setText(_translate("MainWindow", "Plots"))
        ##self.pushButton_updatePlots.setText(_translate("MainWindow", "Update"))
        ##self.tabWidget_plots.setTabText(self.tabWidget_plots.indexOf(self.tab_plotSourceImage), _translate("MainWindow", "Source Image"))
        ##self.tabWidget_plots.setTabText(self.tabWidget_plots.indexOf(self.tab_plotProp), _translate("MainWindow", "Propagation"))
        self.radioButton_quasi.setText(_translate("MainWindow", "Quasi-monochromatic"))
        self.label_N.setText(_translate("MainWindow", "Matrix size N:"))
        self.pushButton_start.setText(_translate("MainWindow", "Start Simulation"))
        self.checkBox_save.setText(_translate("MainWindow", "Save Results"))
        self.checkBox_saveSourceCSDA.setText(_translate("MainWindow", "Save Source Matrix"))
        self.checkBox_savePropCSDA.setText(_translate("MainWindow", "Save Propagation Matrix"))
        self.label_geometry.setText(_translate("MainWindow", "Geometry:"))
        self.label_SpectrumParameters.setText(_translate("MainWindow", "Spectrum Parameters"))
        self.label_projName.setText(_translate("MainWindow", "Project Name: "))
        ##self.checkBox_schedule.setText(_translate("MainWindow", "Scheldule Simulation"))
        self.radioButton_poly.setText(_translate("MainWindow", "Polychromatic"))
        self.label_SourceParameters.setText(_translate("MainWindow", "Source Parameters"))
        self.label_specType.setText(_translate("MainWindow", "Spectrum model:"))
        self.checkBox_debug.setText(_translate("MainWindow", "Debug"))
        self.checkBox_pyopencl.setText(_translate("MainWindow", "Use PyOpenCL"))
        ##self.label_startSim.setText(_translate("MainWindow", "Start Simulation"))
        self.label_PropgationSystem.setText(_translate("MainWindow", "Propagation System"))
        self.label_device.setText(_translate("MainWindow", "Device:"))
        self.label_cohModel.setText(_translate("MainWindow", "Coherence Model:"))
        self.label_useSpecDen.setText(_translate("MainWindow", "Use Custom Spectral Density?"))
        self.label_PropagationQuantities.setText(_translate("MainWindow", "Propagation Quantities"))
        self.label_saveFile.setText(_translate("MainWindow", "Save File:"))
        self.label_numPlanes.setText(_translate("MainWindow", "Number of Propagation Planes:"))
        self.label_platform.setText(_translate("MainWindow", "Platform:"))
        self.toolButton_geoFromFile.setText(_translate("MainWindow", "..."))
        self.radioButton_1freq.setText(_translate("MainWindow", "Single Frequency"))
        self.lineEdit_simName.setText(_translate("MainWindow", "New Project"))
        self.label_sourceRes.setText(_translate("MainWindow", "Source Spatial Resolution (m):"))
        self.label_comParams.setText(_translate("MainWindow", "Options"))
        self.checkBox_geoFromFile.setText(_translate("MainWindow", "Geometry from File (2D array '.npy')"))
        self.label_propQuant.setText(_translate("MainWindow", "Propagation Quantity:"))
        self.label_theta.setText(_translate("MainWindow", "Angle (rad):"))
        self.label_propSpecModel.setText(_translate("MainWindow", "Model:"))
        self.toolButton_saveFile.setText(_translate("MainWindow", "..."))
        self.label_centralFreq.setText(_translate("MainWindow", "Angular Frequency (rad/s):"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuExport.setTitle(_translate("MainWindow", "Export"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionNew_Project.setText(_translate("MainWindow", "New Project"))
        self.actionLoad_Project.setText(_translate("MainWindow", "Load Project"))
        self.actionSave_Project.setText(_translate("MainWindow", "Save Project"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        ##self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        ##self.actionUndo.setText(_translate("MainWindow", "Undo"))
        ##self.actionRedo.setText(_translate("MainWindow", "Redo"))
        ##self.actionCut.setText(_translate("MainWindow", "Cut"))
        ##self.actionCopy.setText(_translate("MainWindow", "Copy"))
        ##self.actionDelete.setText(_translate("MainWindow", "Delete"))
        ##self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionManual.setText(_translate("MainWindow", "Manual"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionGet_Citation.setText(_translate("MainWindow", "Get Citation"))
        self.actionExport_Data.setText(_translate("MainWindow", "Export Results"))

        # initial running functions
        self.showRAM()               # show RAM memory available
        self.search_specModel()      # searching for spectrum profile models
        self.update_specPars()       # updating spectrum profile parameters
        self.search_cohModel()       # searching for coherence models
        self.search_geometry()       # searching for geometry models
        self.search_specDenModels()  # searching for spectral density models
        self.updatePropPlanePars()   # updating propagation plane paramenters
        self.update_numPlanes()      # updating number of propagation planes
        self.update_specDenArea()    # updating custom spectral density area

        # pupil geometry
        self.searchPupilGeom()       # searching for pupil geometry functions
        self.updatePupilArea()       # updating pupil scroll area
        for i in range(0,self.max_numPlanes):
            self.updatePupilGeomPars(i)

        # optics
        self.update_opticsArea()     # updating optica scroll area
        self.searchOpticsFunc()
        for i in range(0,self.max_numPlanes):
            self.updateOpticsFuncPars(i)
        self.updatePropQuantity()

    #***************************************************************************
    #///////////////////////////////////////////////////////////////////////////
    #***************************************************************************


    def update_devices(self):
        "Updates OpenCL devices"
        update_devices2(self)


    def add_logfile(self,actual_time,text):
        "adds time and text to log file"
        self.log_txt += actual_time + "\t" + str(text) + "\n"
        QtWidgets.qApp.processEvents()


    def update_outputText(self,text):
        "Updates the Output Message box in the application"
        actual_time = self.give_time()
        self.textBrowser.append("\n"+ actual_time +"  | >> "+str(text))
        self.textBrowser.update()

        # adding to log file
        self.add_logfile(actual_time,text)

        # updating window
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
        "Show Citation for PyWolf"
        mydialog = QDialog()
        mydialog.setModal(True)
        mydialog.exec()


    #***************************************************************************
    # Functions stored in <app_functions\mainFunctions>
    #***************************************************************************
    def openFileNameDialog_saveDir(self):
        openFileNameDialog_saveDir2(self)

    def openFileNameDialog_exportSourceCSDA(self):
        "choose export directory for source CSDA"
        download_path = ui.lineEdit_saveFiles.text()
        #options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        filename = None
        try:
            pass
            """
            ui.dirName = QFileDialog.getExistingDirectory(None,"Save Directory",download_path) # ,,options=options
            ui.lineEdit_saveFiles.clear()
            ui.lineEdit_saveFiles.setText(ui.dirName)
            """
        except:
            update_outputText("Something went wrong when choosing saving directory.")

    def openFileNameDialog_openGeo(self):
        openFileNameDialog_openGeo2(self)

    def openFileNameDialog_openCSDA(self):
        openFileNameDialog_openCSDA2(self)

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
        label.setVisible(False)
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
        self.updateSpaceRes()

    def updatePropPlanePars(self):
        updatePropPlanePars2(self)

    def update_opticsArea(self):
        update_opticsArea2(self)

    def update_specDenArea(self):
        update_specDenArea2(self)

    def updateSpaceRes(self):
        updateSpaceRes2(self)

    def updateOmegaRes(self):
        updateOmegaRes2(self)

    def updatePupilArea(self):
        updatePupilArea2(self)

    def searchPupilGeom(self):
        searchPupilGeom2(self)

    def updatePupilGeomPars(self,Plane):
        updatePupilGeomPars2(self,Plane)

    def searchOpticsFunc(self):
        searchOpticsFunc2(self)

    def updateOpticsFuncPars(self,Plane):
        updateOpticsFuncPars2(self,Plane)

    def updateGeoFromFile(self):
        updateGeoFromFile2(self)

    def updateCSDAFromFile(self):
        updateCSDAFromFile2(self)

    def updatePropQuantity(self):
        updatePropQuantity2(self)

    def update_OpticsMod(self):
        update_OpticsMod2(self)
    #***************************************************************************
    #///////////////////////////////////////////////////////////////////////////
    #***************************************************************************


    def create_action(self, text, slot=None, shortcut=None,icon=None, tip=None, checkable=False):
        action = QtWidgets.QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action


    def on_about(self):
        msg = """ PyWolf version 1.0

This software is licensed to you under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

         * This software is not commercial and cannot be sold.
         * If you find this software useful for you research, please help by citing using the reference provided (F2).
         * If you have any suggestions or comments, please send it to ___

        """
        QtWidgets.QMessageBox.about(self, "About", msg.strip())


    def on_citation(self):
        msg = """ Please cite:

         Tiago E. C. Magalhaes, "PyWolf"
         """
        QtWidgets.QMessageBox.about(self, "Citation", msg.strip())


    def on_pick(self, event):
        # The event received here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        #
        box_points = event.artist.get_bbox().get_points()
        msg = "You've clicked on a bar with coords:\n %s" % box_points

        QMessageBox.information(self, "Click!", msg)


    def draw_sourceImage(self):
        """ Redraws the figure
        """
        """
        str = self.textbox.text().encode('utf-8')
        self.data = [int(s) for s in str.split()]

        x = range(len(self.data))

        # clear the axes and redraw the plot anew
        #
        self.axes.clear()
        self.axes.grid(self.grid_cb.isChecked())

        self.axes.bar(
            x=x,
            height=self.data,
            width=self.slider.value() / 100.0,
            align='center',
            alpha=0.44,
            picker=5)
        """

        self.canvasSI.canvas.draw()


    def scrolling(self, event):
        val = self.scrollArea_sourceImage.verticalScrollBar().value()
        if event.button =="down":
            self.scrollAreaWidgetContents_sourceImage.verticalScrollBar().setValue(val+100)
        else:
            self.scrollAreaWidgetContents_sourceImage.verticalScrollBar().setValue(val-100)


    def zeroPadingOptions(self):
        self.updateSpaceRes()
        if ui.checkBox_FFT.isChecked():
            self.label_NZ.setVisible(True)
            self.lineEdit_NZ.setVisible(True)
        else:
            self.label_NZ.setVisible(False)
            self.lineEdit_NZ.setVisible(False)


    #***************************************************************************
    # Saving & Loading functions
    #***************************************************************************
    def save_sourceImage(self):
        "Saves the source Image into the desired location"
        if self.sim:
            try:
                download_path = self.lineEdit_saveFiles.text()
                dirName = QFileDialog.getExistingDirectory(None,"Save Source Image",download_path)
                if dirName:
                    save(dirName+"\\CSDA_source_image",ui.CSDA_source.image)
                    self.update_outputText("[Info] Source image saved in "+str(dirName)+"/CSDA_source_image.npy")
            except Exception as error:
                update_outputText("[Error] "+str(error))
        else:
            self.update_outputText("[Warning] "+"You can only export the source image after the simulation.")

    def save_propImage(self):
        "Saves the propagation Image into the desired location"
        if self.sim:
            try:
                download_path = self.lineEdit_saveFiles.text()
                dirName = QFileDialog.getExistingDirectory(None,"Save Propagation Image",download_path)
                if dirName:
                    save(dirName+"\\CSDA_prop_image",ui.CSDA_prop.image)
                    self.update_outputText("[Info] Propagation image saved in "+str(dirName)+"/CSDA_prop_image.npy")
            except Exception as error:
                update_outputText("[Error] "+str(error))
        else:
            self.update_outputText("[Warning] "+"You can only export the propagation image after the simulation.")

    def save_sourceCSDA(self):
        "Saves the source CSDA into the desired location"
        if self.sim:
            try:
                download_path = self.lineEdit_saveFiles.text()
                dirName = QFileDialog.getExistingDirectory(None,"Save Source CSDA",download_path)
                if dirName:
                    save(dirName+"\\CSDA_source",ui.CSDA_source.matrix)
                    self.update_outputText("[Info] Source CSDA saved in "+str(dirName)+"/CSDA_source.npy")
            except Exception as error:
                update_outputText("[Error] "+str(error))
        else:
            self.update_outputText("[Warning] "+"You can only export the CSDA matrix after the simulation.")

    def save_propCSDA(self):
        "Saves the propagated CSDA into the desired location"
        if self.sim:
            try:
                download_path = self.lineEdit_saveFiles.text()
                dirName = QFileDialog.getExistingDirectory(None,"Save Propagation CSDA",download_path)
                if dirName:
                    save(dirName+"\\CSDA_propagation",ui.CSDA_prop.matrix)
                    self.update_outputText("[Info] Propagation CSDA saved in "+str(dirName)+"/CSDA_propagation.npy")
            except Exception as error:
                self.update_outputText("[Error] "+str(error))
        else:
            self.update_outputText("[Warning] "+"You can only export the CSDA matrix after the simulation.")

    def save_results(self):
        "Saves results into directory <dirName>"
        if self.sim:
            try:
                download_path = self.lineEdit_saveFiles.text()
                dirName = QFileDialog.getExistingDirectory(None,"Save Results Folder",download_path)
                if dirName:
                    self.save_results_file(dirName)
            except:
                pass
        else:
            self.update_outputText("[Warning] "+"You can only export the CSDA matrix after the simulation.")

    def save_results_file(self,dirName,spec=False):
        "Saves results into directory <dirName>"
        save_results_file2(self,dirName,spec=False)

    def save_project(self):
        "Saves Project in a <.wolf> file"
        try:
            save_path = self.current_dir+"\\"+self.lineEdit_simName.text()
            print(save_path)
            dirName = QFileDialog.getSaveFileName(None,"Save Project Folder",save_path,"PyWolf Files (*.wolf)")

            if dirName:
                self.save_project_file(dirName[0])
        except:
            pass

    def save_project_file(self,dirName):
        "Saves Project into user-defined File"
        save_project_file2(self,dirName)

    def load_project(self):
        "Loads project in <.wolf> file"
        try:
            filename = None
            proj_path = QFileDialog.getOpenFileName(None,"Open Project File","", "PyWolf Files (*.wolf)") # ,,options=options
            if proj_path[0]:
                self.dirProj = proj_path[0]
                self.load_project_file(self.dirProj)
        except:
            pass

    def new_project(self):
        "Reset all values"
        try:
            filename = None
            proj_path = QFileDialog.getOpenFileName(None,"Open Project File","", "PyWolf Files (*.wolf)") # ,,options=options
            if proj_path[0]:
                self.dirProj = proj_path[0]
                self.load_project_file(self.dirProj)
        except:
            pass

    def load_project_file(self,dirProj):
        load_project_file2(self,dirProj)

    #***************************************************************************
    #///////////////////////////////////////////////////////////////////////////
    #***************************************************************************


    #***************************************************************************
    # Examples
    #***************************************************************************
    def search_examples(self):
        current_dir = os.getcwd() +"\examples"
        self.dir_examples = current_dir
        sys.path.insert(1, current_dir+"\examples")

        saved = getcwd()
        chdir(current_dir)
        res = glob.glob('*.' + "wolf")
        chdir(saved)

        for x in range(0,len(res)):
            self.action_examples_list.append(QtWidgets.QAction(MainWindow))
            self.action_examples_list[-1].setText(res[x][:-5])
            self.subMenu_Examples.addAction(self.action_examples_list[-1])
            self.action_examples_list[-1].triggered.connect(functools.partial(self.load_examples,self.action_examples_list[-1].text()))

            #self.action_Examples.addAction(self.action_examples_list[-1])

    def load_examples(self,name):
        self.load_project_file(self.dir_examples+"\\"+name+".wolf")

    #***************************************************************************
    #///////////////////////////////////////////////////////////////////////////
    #***************************************************************************


    def remove_lastSpaces_title(self):
        "Removes last Spaces from a text"
        sim_name = self.lineEdit_simName.text()
        if sim_name[-1]==" ":
            N = len(sim_name)
            last = False
            count = 0
            for i in range(N-1,0,-1):
                if sim_name[i] == " ":
                    if not last:
                        count+=1
                else:
                    last = True
            self.lineEdit_simName.setText(sim_name[:-count])


    def show_source_spectrum(self):
        try:
            if not self.source_spec_plot:
                N = int(self.lineEdit_N.text())
                self.canvasSourceSpec = Canvas_sourceSpecPreview(self,N)
                self.tabWidget_plots.addTab(self.list_of_tabs[-1], "Source Spectrum Preview")
                QtWidgets.qApp.processEvents()
                self.source_spec_plot = True
            else:
                # clean all tabs
                N_tabs = len(self.list_of_tabs)
                for i in range(N_tabs-1,-1,-1):
                    self.tabWidget_plots.removeTab(i)
                    self.list_grid_tabs[i].deleteLater()
                    self.list_of_tabs[i].deleteLater()
                    del self.list_of_tabs[i]
                    del self.list_grid_tabs[i]
                N = int(self.lineEdit_N.text())
                self.canvasSourceSpec = Canvas_sourceSpecPreview(self,N)
                self.tabWidget_plots.addTab(self.list_of_tabs[-1], "Source Spectrum Preview")
                QtWidgets.qApp.processEvents()
                self.source_spec_plot = True

        except Exception as error:
            self.update_outputText(error)

    def search_specDenModels(self):
        search_specDenModels2(self)

    def updateSpecDenPars(self):
        updateSpecDenPars2(self)


    #***************************************************************************
    # Starts the Simulation
    #***************************************************************************

    def start_simulation(self):
        # [ [Options], [Propagation Quantities], [Spectrum Parameters], [Source Parameters], [Propagation System]  ]
        self.update_outputText("We will first test the parameters. Please wait...")

        # updating text
        QtWidgets.qApp.processEvents()

        #-----------------------------------------------------------------------
        # Testing parameters
        #-----------------------------------------------------------------------
        # removing extra last spaces in <Simulation Name>
        self.remove_lastSpaces_title()

        # call test function
        test = func_testPars(self)

        all_ok=None
        self.all_parameters_list = None

        if test:
            all_ok = test[0]
            self.all_parameters_list = test[1]

        #_______________________________________________________________________

        #-----------------------------------------------------------------------
        # Starting Simulation
        #-----------------------------------------------------------------------
        try:
            # clean all tabs
            N_tabs = len(self.list_of_tabs)
            for i in range(N_tabs-1,-1,-1):
                self.tabWidget_plots.removeTab(i)

                self.list_grid_tabs[i].deleteLater()
                self.list_of_tabs[i].deleteLater()

                del self.list_of_tabs[i]
                del self.list_grid_tabs[i]

            if test:
                if all_ok:
                    self.sim = func_startSim(self,self.all_parameters_list)

                # if simulation was successful
                if self.sim:
                    pass

        except Exception as error:
            self.update_outputText(str(error)+" in <Main>: starting simulation.")
        #_______________________________________________________________________

    #***************************************************************************
    #///////////////////////////////////////////////////////////////////////////
    #***************************************************************************


    #____Exit___________________________________________________________________
    def close_application(self):
        "Closes the application"
        app.closeAllWindows()
    #___________________________________________________________________________


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # initial parameters
    log_txt    = "" # log file
    debug      = False
    appname    = "PyWolf v1.0"
    cr = "Copyright (C) 2020 Tiago E. C. Magalhaes under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version."

    # time
    from datetime import datetime
    now        = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    double_bar = "="*40
    output_txt = ""+">> "+str(appname)+"\n"+""  # to be displayed in app
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

    # global variables
    global CSDA_prop

    # creating main window
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow,appname,rect,current_dir,log_txt,output_txt)
    MainWindow.show()

    # Exit
    sys.exit(app.exec_())
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================