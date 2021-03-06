#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Tiago
#
# Created:     25/01/2020
# Copyright:   (c) Tiago 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys, os, random

from PyQt5 import QtCore, QtGui, QtWidgets



from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from numpy import zeros
from numpy import sqrt
from numpy import angle

import os
current_dir = os.getcwd()
up_dir = os.path.dirname(current_dir)
sys.path.insert(1, up_dir)
from palettes import *

import copy



class Canvas_sourceSDC2D:

    def __init__(self,ui,W_matrix,N):

        # Scroll Area Source Image
        ui.scrollArea_sourceSDC = QtWidgets.QScrollArea(ui.tab_plotSourceSDC2D)
        ui.scrollArea_sourceSDC.setPalette(palette_scrollPlotProp)
        ui.scrollArea_sourceSDC.setWidgetResizable(True)
        ui.scrollArea_sourceSDC.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)
        ui.scrollArea_sourceSDC.setObjectName("scrollArea_sourceSDC")

        # Scroll Area Options prop
        ui.scrollArea_sourceSDCOpt = QtWidgets.QScrollArea(ui.tab_plotSourceSDC2D)
        ui.scrollArea_sourceSDCOpt.setWidgetResizable(True)
        ui.scrollArea_sourceSDCOpt.setObjectName("scrollArea_propImageOpt")
        ui.scrollArea_sourceSDCOpt.setPalette(palette_scrollPlotProp)

        ui.scrollAreaWidgetContents_sourceSDCOpt = QtWidgets.QWidget()
        ui.scrollAreaWidgetContents_sourceSDCOpt.setObjectName("scrollAreaWidgetContents_sourceSDCOpt")
        ui.scrollArea_sourceSDCOpt.setWidget(ui.scrollAreaWidgetContents_sourceSDCOpt)

        ui.gridLayout_sourceSDCOpt = QtWidgets.QGridLayout(ui.scrollAreaWidgetContents_sourceSDCOpt)
        ui.gridLayout_sourceSDCOpt.setObjectName("gridLayout_sourceSDCOpt")

        ui.gridLayout_TabSourceSDC2D.addWidget(ui.scrollArea_sourceSDC, 3, 0, 1, 1)
        ui.gridLayout_TabSourceSDC2D.addWidget(ui.scrollArea_sourceSDCOpt, 10, 0, 1, 1)

        # Scroll Area Source SDC Phase
        ui.scrollArea_sourceSDC_phase = QtWidgets.QScrollArea(ui.tab_plotSourceSDC2D)
        ui.scrollArea_sourceSDC_phase.setPalette(palette_scrollPlotProp)
        ui.scrollArea_sourceSDC_phase.setWidgetResizable(True)
        ui.scrollArea_sourceSDC_phase.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)
        ui.scrollArea_sourceSDC_phase.setObjectName("scrollArea_sourceSDC_phase")

        # Scroll Area Options Source SDC Phase
        ui.scrollArea_sourceSDCOpt_phase = QtWidgets.QScrollArea(ui.tab_plotSourceSDC2D)
        ui.scrollArea_sourceSDCOpt_phase.setWidgetResizable(True)
        ui.scrollArea_sourceSDCOpt_phase.setObjectName("scrollArea_propImageOpt_phase")
        ui.scrollArea_sourceSDCOpt_phase.setPalette(palette_scrollPlotProp)

        ui.scrollAreaWidgetContents_sourceSDCOpt_phase = QtWidgets.QWidget()
        ui.scrollAreaWidgetContents_sourceSDCOpt_phase.setObjectName("scrollAreaWidgetContents_sourceSDCOpt_phase")
        ui.scrollArea_sourceSDCOpt_phase.setWidget(ui.scrollAreaWidgetContents_sourceSDCOpt_phase)

        ui.gridLayout_sourceSDCOpt_phase = QtWidgets.QGridLayout(ui.scrollAreaWidgetContents_sourceSDCOpt_phase)
        ui.gridLayout_sourceSDCOpt_phase.setObjectName("gridLayout_sourceSDCOpt_phase")

        ui.gridLayout_TabSourceSDC2D.addWidget(ui.scrollArea_sourceSDC_phase, 3, 1, 1, 1)
        ui.gridLayout_TabSourceSDC2D.addWidget(ui.scrollArea_sourceSDCOpt_phase, 10, 1, 1, 1)
        #_______________________________________________________________________


        #=======================================================================
        # Parameters
        #=======================================================================
        # N
        self.N = N

        # W matrix
        self.W_matrix = copy.copy(W_matrix)

        # User interface
        self.ui = ui

        # parent
        self.parent = ui.scrollArea_sourceSDC
        self.parent_phase = ui.scrollArea_sourceSDC_phase

        # parent optioncs
        self.parentOptions = ui.scrollArea_sourceSDCOpt
        self.parentOptions_phase = ui.scrollArea_sourceSDCOpt_phase

        # grid parent options
        self.gridOptions = ui.gridLayout_sourceSDCOpt
        self.gridOptions_phase = ui.gridLayout_sourceSDCOpt_phase

        # first plot
        self.first_plot = False
        #_______________________________________________________________________

        # Initial points (middle)
        self.P1x = int(N/2)
        self.P1y = int(N/2)

        self.build_fig()


    def build_fig(self):

        #=======================================================================
        # Create the mpl Figure and FigCanvas objects.
        #=======================================================================
        # magnitude
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)

        # phase
        self.dpi_phase = 100
        self.fig_phase = Figure((5.0, 4.0), dpi=self.dpi_phase)
        self.canvas_phase = FigureCanvas(self.fig_phase)

        # axes
        self.axes = self.fig.add_subplot(111)
        self.axes_phase = self.fig_phase.add_subplot(111)
        #_______________________________________________________________________


        #=======================================================================
        # Plotting 2D figure and configuring
        #=======================================================================

        # creating image prop
        self.sourceSDC_mag   = sqrt(self.W_matrix[self.P1x,self.P1y].real**2+self.W_matrix[self.P1x,self.P1y].imag**2)
        self.sourceSDC_phase = angle(self.W_matrix[self.P1y,self.P1y])

        # PLOT magnitude
        self.im = self.axes.imshow(self.sourceSDC_mag)
        self.cbar = self.fig.colorbar(self.im)

        # PLOT phase
        self.im_phase = self.axes_phase.imshow(self.sourceSDC_phase)
        self.cbar_phase = self.fig_phase.colorbar(self.im_phase)

        # font size
        self.fsize = 12
        self.fsize_phase = 12

        # x,y Labels
        self.axes.set_xlabel("x (m)",fontsize = self.fsize)
        self.axes.set_ylabel("y (m)",fontsize = self.fsize)
        #_______________________________________________________________________


        #=======================================================================
        # Tool bar
        #=======================================================================

        # Bind the 'pick' event for clicking on one of the bars
        self.canvas.mpl_connect('pick_event', self.ui.on_pick) #self.canvas.mpl_connect("scroll_event", ui.scrolling)
        # Bind the 'pick' event for clicking on one of the bars
        self.canvas_phase.mpl_connect('pick_event', self.ui.on_pick) #self.canvas.mpl_connect("scroll_event", ui.scrolling)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.parent)
        self.mpl_toolbar_phase = NavigationToolbar(self.canvas_phase, self.parent_phase)

        #ui.gridLayout_TabPropImage.addWidget(self.mpl_toolbar, 2, 0, 1, 3)
        self.ui.gridLayout_TabSourceSDC2D.addWidget(self.mpl_toolbar, 8, 0, 1, 3,alignment=QtCore.Qt.AlignLeft)
        self.ui.gridLayout_TabSourceSDC2D.addWidget(self.mpl_toolbar_phase, 8, 1, 1, 3,alignment=QtCore.Qt.AlignLeft)

        #_______________________________________________________________________


        #=======================================================================
        # Canvas in Scroll Area - magnitude
        #=======================================================================

        #self.canvas.draw()
        #self.canvas.setParent(parent)
        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)

        # Container for VBOX
        self.containerGraph = QWidget(self.parent)
        self.containerGraph.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)

        self.containerGraph.setMinimumWidth(self.canvas.width())
        self.containerGraph.setMinimumHeight(self.canvas.height())

        self.containerGraph.setMaximumWidth(self.canvas.width()+5)
        self.containerGraph.setMaximumHeight(self.canvas.height()+5)

        # VBOX for canvas
        self.vbox = QVBoxLayout(self.containerGraph)
        #self.vbox.setGeometry(QRect(0, 0, self.canvas.width(), self.canvas.height()))
        self.vbox.addWidget(self.canvas)

        self.parent.setWidget(self.containerGraph)

        #_______________________________________________________________________


        #=======================================================================
        # Canvas in Scroll Area - phase
        #=======================================================================
        self.canvas_phase.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)

        # Container for VBOX
        self.containerGraph_phase = QWidget(self.parent_phase)
        self.containerGraph_phase.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)

        self.containerGraph_phase.setMinimumWidth(self.canvas_phase.width())
        self.containerGraph_phase.setMinimumHeight(self.canvas_phase.height())

        self.containerGraph_phase.setMaximumWidth(self.canvas_phase.width()+5)
        self.containerGraph_phase.setMaximumHeight(self.canvas_phase.height()+5)

        # VBOX for canvas
        self.vbox_phase = QVBoxLayout(self.containerGraph_phase)
        #self.vbox.setGeometry(QRect(0, 0, self.canvas.width(), self.canvas.height()))
        self.vbox_phase.addWidget(self.canvas_phase)

        self.parent_phase.setWidget(self.containerGraph_phase)
        #_______________________________________________________________________



        if not self.first_plot:
            self.figure_options()
            self.figure_options_phase()
            self.first_plot = True






    def figure_options(self):

        # label Point P1x
        self.label_P1x = QtWidgets.QLabel(self.parentOptions)
        self.label_P1x.setObjectName("label_P1x")
        self.label_P1x.setText("Point ")
        self.gridOptions.addWidget(self.label_P1x, 2, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit Point P1x
        self.lineEdit_P1x = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_P1x.setObjectName("lineEdit_P1x")
        self.gridOptions.addWidget(self.lineEdit_P1x,2, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_P1x.setText(str(int(self.N/2)))
        self.lineEdit_P1x.textChanged.connect(self.change_P1x)

        # label Point P1y
        self.label_P1y = QtWidgets.QLabel(self.parentOptions)
        self.label_P1y.setObjectName("label_P1y")
        self.label_P1y.setText('$Point$')
        self.gridOptions.addWidget(self.label_P1y, 4, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit Point P1x
        self.lineEdit_P1y = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_P1y.setObjectName("lineEdit_P1y")
        self.gridOptions.addWidget(self.lineEdit_P1y,4, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_P1y.setText(str(int(self.N/2)))
        self.lineEdit_P1y.textChanged.connect(self.change_P1y)


        # label title
        self.label_title = QtWidgets.QLabel(self.parentOptions)
        self.label_title.setObjectName("label_title")
        self.label_title.setText("Title")
        self.gridOptions.addWidget(self.label_title, 6, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit title label
        self.lineEdit_title = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_title.setObjectName("lineEdit_title")
        self.lineEdit_title.textChanged.connect(self.change_title)
        self.gridOptions.addWidget(self.lineEdit_title,6, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.change_title()
        self.lineEdit_title.setText("Source SDC")

        # label x
        self.label_x = QtWidgets.QLabel(self.parentOptions)
        self.label_x.setObjectName("label_x")
        self.label_x.setText("Label x-axis")
        self.gridOptions.addWidget(self.label_x, 8, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit x label
        self.lineEdit_xLabel = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_xLabel.setObjectName("lineEdit_xlabel")
        self.lineEdit_xLabel.textChanged.connect(self.change_labelx)
        self.gridOptions.addWidget(self.lineEdit_xLabel,8, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.change_labelx()
        self.lineEdit_xLabel.setText("x")

        # label y
        self.label_y = QtWidgets.QLabel(self.parentOptions)
        self.label_y.setObjectName("label_y")
        self.label_y.setText("Label y-axis")
        self.gridOptions.addWidget(self.label_y, 10, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit y label
        self.lineEdit_yLabel = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_yLabel.setObjectName("lineEdit_ylabel")
        self.lineEdit_yLabel.textChanged.connect(self.change_labely)
        self.gridOptions.addWidget(self.lineEdit_yLabel,10, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.change_labely()
        self.lineEdit_yLabel.setText("y")

        # label xlim
        self.label_xlim = QtWidgets.QLabel(self.parentOptions)
        self.label_xlim.setObjectName("label_xlim")
        self.label_xlim.setText("xlim")
        self.gridOptions.addWidget(self.label_xlim, 12, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit xlim
        self.lineEdit_xlim = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_xlim.setObjectName("lineEdit_ylabel")
        self.lineEdit_xlim.textChanged.connect(self.change_xlim)
        self.gridOptions.addWidget(self.lineEdit_xlim,12, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_xlim.setText("(_,_)")
        self.change_xlim()

        # label ylim
        self.label_ylim = QtWidgets.QLabel(self.parentOptions)
        self.label_ylim.setObjectName("label_ylim")
        self.label_ylim.setText("ylim")
        self.gridOptions.addWidget(self.label_ylim, 14, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit ylim
        self.lineEdit_ylim = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_ylim.setObjectName("lineEdit_ylabel")
        self.lineEdit_ylim.textChanged.connect(self.change_ylim)
        self.gridOptions.addWidget(self.lineEdit_ylim,14, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_ylim.setText("(_,_)")
        self.change_ylim()

        # label cmap
        self.label_cmap = QtWidgets.QLabel(self.parentOptions)
        self.label_cmap.setObjectName("label_cmap")
        self.label_cmap.setText("Color Map")
        self.gridOptions.addWidget(self.label_cmap, 20, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit cmap
        self.lineEdit_cmap = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_cmap.setObjectName("lineEdit_cmap")
        self.lineEdit_cmap.textChanged.connect(self.change_cmap)
        self.gridOptions.addWidget(self.lineEdit_cmap,20, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_cmap.setText("hot")
        self.change_cmap()

        # label Font Size
        self.label_fsize = QtWidgets.QLabel(self.parentOptions)
        self.label_fsize.setObjectName("label_fsize")
        self.label_fsize.setText("Font Size")
        self.gridOptions.addWidget(self.label_fsize, 22, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit font size
        self.lineEdit_fsize = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_fsize.setObjectName("label_fsize")
        self.lineEdit_fsize.textChanged.connect(self.change_fsize)
        self.gridOptions.addWidget(self.lineEdit_fsize,22, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_fsize.setText(str(self.fsize))
        self.change_fsize()

        # label DPI
        self.label_dpi = QtWidgets.QLabel(self.parentOptions)
        self.label_dpi.setObjectName("label_dpi")
        self.label_dpi.setText("dpi (100-500)")
        self.gridOptions.addWidget(self.label_dpi, 24, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit DPI
        self.lineEdit_dpi = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_dpi.setObjectName("label_dpi")
        self.lineEdit_dpi.textChanged.connect(self.change_dpi)
        self.gridOptions.addWidget(self.lineEdit_dpi,24, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_dpi.setText(str(self.dpi))
        self.change_fsize()
        #_______________________________________________________________________




    def figure_options_phase(self):
        try:
            # label title_phase
            self.label_title_phase = QtWidgets.QLabel(self.parentOptions)
            self.label_title_phase.setObjectName("label_title")
            self.label_title_phase.setText("Title")
            self.gridOptions_phase.addWidget(self.label_title_phase, 6, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

            # line edit title label_phase
            self.lineEdit_title_phase = QtWidgets.QLineEdit(self.parentOptions)
            self.lineEdit_title_phase.setObjectName("lineEdit_title_phase")
            self.lineEdit_title_phase.textChanged.connect(self.change_title_phase)
            self.gridOptions_phase.addWidget(self.lineEdit_title_phase,6, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
            self.lineEdit_title_phase.setText("Source SDC Phase")
            self.change_title_phase()

            # label x_phase
            self.label_x_phase = QtWidgets.QLabel(self.parentOptions)
            self.label_x_phase.setObjectName("label_xv")
            self.label_x_phase.setText("Label x-axis")
            self.gridOptions_phase.addWidget(self.label_x_phase, 8, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

            # line edit x label_phase_phase
            self.lineEdit_xLabel_phase = QtWidgets.QLineEdit(self.parentOptions)
            self.lineEdit_xLabel_phase.setObjectName("lineEdit_xlabel_phase")
            self.lineEdit_xLabel_phase.textChanged.connect(self.change_labelx_phase)
            self.gridOptions_phase.addWidget(self.lineEdit_xLabel_phase,8, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
            self.change_labelx_phase()
            self.lineEdit_xLabel_phase.setText("x")

            # label y_phase
            self.label_y_phase = QtWidgets.QLabel(self.parentOptions)
            self.label_y_phase.setObjectName("label_y_phase")
            self.label_y_phase.setText("Label y-axis")
            self.gridOptions_phase.addWidget(self.label_y_phase, 10, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

            # line edit y label_phase
            self.lineEdit_yLabel_phase = QtWidgets.QLineEdit(self.parentOptions)
            self.lineEdit_yLabel_phase.setObjectName("lineEdit_ylabel_phase")
            self.lineEdit_yLabel_phase.textChanged.connect(self.change_labely_phase)
            self.gridOptions_phase.addWidget(self.lineEdit_yLabel_phase,10, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
            self.change_labely_phase()
            self.lineEdit_yLabel_phase.setText("y")

            # label xlim_phase
            self.label_xlim_phase = QtWidgets.QLabel(self.parentOptions)
            self.label_xlim_phase.setObjectName("label_xlim_phase")
            self.label_xlim_phase.setText("xlim")
            self.gridOptions_phase.addWidget(self.label_xlim_phase, 12, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

            # line edit xlim_phase
            self.lineEdit_xlim_phase = QtWidgets.QLineEdit(self.parentOptions)
            self.lineEdit_xlim_phase.setObjectName("lineEdit_ylabel_phase")
            self.lineEdit_xlim_phase.textChanged.connect(self.change_xlim_phase)
            self.gridOptions_phase.addWidget(self.lineEdit_xlim_phase,12, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
            self.lineEdit_xlim_phase.setText("(_,_)")
            self.change_xlim_phase()

            # label ylim_phase
            self.label_ylim_phase = QtWidgets.QLabel(self.parentOptions)
            self.label_ylim_phase.setObjectName("label_ylim_phase")
            self.label_ylim_phase.setText("ylim")
            self.gridOptions_phase.addWidget(self.label_ylim_phase, 14, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

            # line edit ylim_phase
            self.lineEdit_ylim_phase = QtWidgets.QLineEdit(self.parentOptions)
            self.lineEdit_ylim_phase.setObjectName("lineEdit_ylabel_phase")
            self.lineEdit_ylim_phase.textChanged.connect(self.change_ylim_phase)
            self.gridOptions_phase.addWidget(self.lineEdit_ylim_phase,14, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
            self.lineEdit_ylim_phase.setText("(_,_)")
            self.change_ylim_phase()

            # label cmap_phase
            self.label_cmap_phase = QtWidgets.QLabel(self.parentOptions)
            self.label_cmap_phase.setObjectName("label_cmap_phase")
            self.label_cmap_phase.setText("Color Map")
            self.gridOptions_phase.addWidget(self.label_cmap_phase, 20, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

            # line edit cmap_phase
            self.lineEdit_cmap_phase = QtWidgets.QLineEdit(self.parentOptions)
            self.lineEdit_cmap_phase.setObjectName("lineEdit_cmap_phase")
            self.lineEdit_cmap_phase.textChanged.connect(self.change_cmap_phase)
            self.gridOptions_phase.addWidget(self.lineEdit_cmap_phase,20, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
            self.lineEdit_cmap_phase.setText("hot")
            self.change_cmap_phase()

            # label Font Size_phase
            self.label_fsize_phase = QtWidgets.QLabel(self.parentOptions)
            self.label_fsize_phase.setObjectName("label_fsize")
            self.label_fsize_phase.setText("Font Size")
            self.gridOptions_phase.addWidget(self.label_fsize_phase, 22, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

            # line edit font size_phase
            self.lineEdit_fsize_phase = QtWidgets.QLineEdit(self.parentOptions)
            self.lineEdit_fsize_phase.setObjectName("label_fsize_phase")
            self.lineEdit_fsize_phase.textChanged.connect(self.change_fsize)
            self.gridOptions_phase.addWidget(self.lineEdit_fsize_phase,22, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
            self.lineEdit_fsize_phase.setText(str(self.fsize))
            self.change_fsize_phase()

            # label DPI_phase
            self.label_dpi_phase = QtWidgets.QLabel(self.parentOptions)
            self.label_dpi_phase.setObjectName("label_dpi_phase")
            self.label_dpi_phase.setText("dpi (100-500)")
            self.gridOptions_phase.addWidget(self.label_dpi_phase, 24, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

            # line edit DPI_phase
            self.lineEdit_dpi_phase = QtWidgets.QLineEdit(self.parentOptions)
            self.lineEdit_dpi_phase.setObjectName("label_dpi_phase")
            self.lineEdit_dpi_phase.textChanged.connect(self.change_dpi_phase)
            self.gridOptions_phase.addWidget(self.lineEdit_dpi_phase,24, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
            self.lineEdit_dpi_phase.setText(str(self.dpi_phase))
            self.change_fsize_phase()
            #_______________________________________________________________________

        except Exception as error:
            self.ui.update_outputText(str(error))



    def change_P1x(self):
        try:
            temp = self.lineEdit_P1x.text()
            if temp != "":
                new = int(temp)
                if new>=0 and new<self.N:
                    self.P1x = new
                    self.update_pcolor()
                    self.update_draw()
        except Except as error:
            self.ui.update_outputText(str(error))

    def change_P1y(self):
        try:
            temp = self.lineEdit_P1y.text()
            if temp != "":
                new = int(temp)
                if new>=0 and new<self.N:
                    self.P1y = new
                    self.update_pcolor()
                    self.update_draw()
        except Except as error:
            self.ui.update_outputText(str(error))

    def update_pcolor(self):
        try:
            # creating image prop
            self.sourceSDC_mag   = sqrt(self.W_matrix[self.P1x,self.P1y].real**2+self.W_matrix[self.P1x,self.P1y].imag**2)
            self.sourceSDC_phase = angle(self.W_matrix[self.P1y,self.P1y])

            self.im.set_array(self.sourceSDC_mag)
            self.im_phase.set_array(self.sourceSDC_phase)

        except Exception as error:
            self.ui.update_outputText(str(error))

    def update_draw(self):
        self.canvas.draw()
        self.canvas.updateGeometry()
        self.canvas_phase.draw()
        self.canvas_phase.updateGeometry()




    #===========================================================================
    # Magnitude
    #===========================================================================
    def change_dpi(self):
        try:
            new = int(self.lineEdit_dpi.text())
            if new>=100 and new<=500:
                self.dpi = new
                self.fig.set_dpi(new)
                self.update_draw()
        except:
            pass

    def change_fsize(self):
        try:
            self.fsize = int(self.lineEdit_fsize.text())
            self.change_title()
            self.change_labelx()
            self.change_labely()
            self.update_draw()
            print(self.fsize)

        except Exception as error:
            pass #self.ui.update_outputText(error)


    def change_cmap(self):
        try:
            self.im.set_cmap(self.lineEdit_cmap.text())
            self.canvas.draw()
        except Exception as error:
            pass
            #self.ui.update_outputText(error)


    def change_xlim(self):
        try:
            temp_txt = self.lineEdit_xlim.text()
            Ntxt     = len(temp_txt)
            numList = []
            if temp_txt[0]=="(" and temp_txt[-1]==")":
                actual=""
                for i in range(1,Ntxt-1):
                    if temp_txt[i] == ",":
                        numList.append(float(actual))
                        actual = ""
                    elif i==Ntxt-2:
                        actual+=temp_txt[i]
                        numList.append(float(actual))
                    else:
                        actual+=temp_txt[i]
            self.axes.set_xlim(numList[0],numList[1])
        except Exception as error:
            pass
            #self.ui.update_outputText(error)

    def change_ylim(self):
        try:
            temp_txt = self.lineEdit_ylim.text()
            Ntxt     = len(temp_txt)
            numList = []
            if temp_txt[0]=="(" and temp_txt[-1]==")":
                actual=""
                for i in range(1,Ntxt-1):
                    if temp_txt[i] == ",":
                        numList.append(float(actual))
                        actual = ""
                    elif i==Ntxt-2:
                        actual+=temp_txt[i]
                        numList.append(float(actual))
                    else:
                        actual+=temp_txt[i]
            self.axes.set_ylim(numList[0],numList[1])
            self.canvas.draw()
        except Exception as error:
            pass
            #self.ui.update_outputText(error)

    def change_title(self):
        try:
            self.axes.set_title(self.lineEdit_title.text(),fontsize = self.fsize)
            self.canvas.draw()
        except:
            pass

    def change_labelx(self):
        if self.lineEdit_xLabel.text()=="":
            self.axes.set_xlabel("")
        else:
            try:
                self.axes.set_xlabel(self.lineEdit_xLabel.text(),fontsize = self.fsize)
                self.canvas.draw()
            except Exception as error:

                self.ui.update_outputText(str(error))

    def change_labely(self):
        if self.lineEdit_yLabel.text()=="":
            self.axes.set_ylabel("")
        else:
            try:
                self.axes.set_ylabel(self.lineEdit_yLabel.text(),fontsize = self.fsize)
                self.canvas.draw()
            except:
                pass
                #self.ui.update_outputText("Unable to update y-label.")

    #___________________________________________________________________________


    #===========================================================================
    # Phase
    #===========================================================================
    try:
        def change_dpi_phase(self):
            try:
                new = int(self.lineEdit_dpi_phase.text())
                if new>=100 and new<=500:
                    self.dpi_phase = new
                    self.fig_phase.set_dpi(new)
                    self.update_draw()
            except:
                pass

        def change_fsize_phase(self):
            try:
                self.fsize_phase = int(self.lineEdit_fsize.text())
                self.change_title_phase()
                self.change_labelx_phase()
                self.change_labely_phase()
                self.update_draw()

            except Exception as error:
                pass #self.ui.update_outputText(error)


        def change_cmap_phase(self):
            try:
                self.im_phase.set_cmap(self.lineEdit_cmap_phase.text())
                self.canvas_phase.draw()
            except Exception as error:
                pass
                #self.ui.update_outputText(error)


        def change_xlim_phase(self):
            try:
                temp_txt = self.lineEdit_xlim_phase.text()
                Ntxt     = len(temp_txt)
                numList = []
                if temp_txt[0]=="(" and temp_txt[-1]==")":
                    actual=""
                    for i in range(1,Ntxt-1):
                        if temp_txt[i] == ",":
                            numList.append(float(actual))
                            actual = ""
                        elif i==Ntxt-2:
                            actual+=temp_txt[i]
                            numList.append(float(actual))
                        else:
                            actual+=temp_txt[i]
                self.axes_phase.set_xlim(numList[0],numList[1])
            except Exception as error:
                pass
                #self.ui.update_outputText(error)

        def change_ylim_phase(self):
            try:
                temp_txt = self.lineEdit_ylim_phase.text()
                Ntxt     = len(temp_txt)
                numList = []
                if temp_txt[0]=="(" and temp_txt[-1]==")":
                    actual=""
                    for i in range(1,Ntxt-1):
                        if temp_txt[i] == ",":
                            numList.append(float(actual))
                            actual = ""
                        elif i==Ntxt-2:
                            actual+=temp_txt[i]
                            numList.append(float(actual))
                        else:
                            actual+=temp_txt[i]
                self.axes_phase.set_ylim(numList[0],numList[1])
                self.canvas.draw()
            except Exception as error:
                pass
                #self.ui.update_outputText(error)

        def change_title_phase(self):
            try:
                self.axes_phase.set_title(self.lineEdit_title_phase.text(),fontsize = self.fsize_phase)
                self.canvas_phase.draw()
            except:
                pass

        def change_labelx_phase(self):
            if self.lineEdit_xLabel_phase.text()=="":
                self.axes_phase.set_xlabel("")
            else:
                try:
                    self.axes_phase.set_xlabel(self.lineEdit_xLabel_phase.text(),fontsize = self.fsize_phase)
                    self.canvas_phase.draw()
                except Exception as error:
                    self.ui.update_outputText(str(error))

        def change_labely_phase(self):
            if self.lineEdit_yLabel_phase.text()=="":
                self.axes_phase.set_ylabel("")
            else:
                try:
                    self.axes_phase.set_ylabel(self.lineEdit_yLabel_phase.text(),fontsize = self.fsize_phase)
                    self.canvas_phase.draw()
                except:
                    pass
                    #self.ui.update_outputText("Unable to update y-label.")

    except Exception as error:
        self.ui.update_outputText(error)
    #___________________________________________________________________________
