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
from numpy import arange
from numpy import float32

import os
current_dir = os.getcwd()
up_dir = os.path.dirname(current_dir)
sys.path.insert(1, up_dir)
from palettes import *
from fonts import *



class Canvas_propSDC:

    def __init__(self,ui,W_matrix,N):

        #=======================================================================
        # Scroll Area SDC Points
        #=======================================================================
        self.scrollArea_points = QtWidgets.QScrollArea(ui.tab_plotPropSDC)
        self.scrollArea_points.setWidgetResizable(True)
        self.scrollArea_points.setObjectName("scrollArea_points")
        self.scrollArea_points.setPalette(palette_scrollPlotProp)

        self.scrollAreaWidgetContents_points = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_points.setObjectName("scrollAreaWidgetContents_points")
        self.scrollArea_points.setWidget(self.scrollAreaWidgetContents_points)

        self.gridLayout_points = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_points)
        self.gridLayout_points.setObjectName("gridLayout_points")

        ui.gridLayout_TabPropSDC.addWidget(self.scrollArea_points, 1, 0, 1, 2)
        #_______________________________________________________________________


        #=======================================================================
        # Button update point
        #=======================================================================
        self.pushButton_updatePoint = QtWidgets.QPushButton(ui.tab_plotPropSDC)
        self.pushButton_updatePoint.setPalette(palette_buttonStart)
        self.pushButton_updatePoint.setFont(font_button)
        self.pushButton_updatePoint.setObjectName("pushButton_updatePoint")
        self.gridLayout_points.addWidget(self.pushButton_updatePoint, 2, 8, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.pushButton_updatePoint.setMinimumWidth(ui.rect.width()/8)
        self.pushButton_updatePoint.setText("Update Point")
        self.pushButton_updatePoint.clicked.connect(self.change_point)
        #_______________________________________________________________________


        #=======================================================================
        # Scroll Area PLOT SDC
        #=======================================================================
        self.scrollArea_propSDC = QtWidgets.QScrollArea(ui.tab_plotPropSDC)
        self.scrollArea_propSDC.setPalette(palette_scrollPlotProp)
        self.scrollArea_propSDC.setWidgetResizable(True)
        self.scrollArea_propSDC.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)
        self.scrollArea_propSDC.setObjectName("scrollArea_propSDC")

        # Scroll Area Options prop
        self.scrollArea_propSDCOpt = QtWidgets.QScrollArea(ui.tab_plotPropSDC)
        self.scrollArea_propSDCOpt.setWidgetResizable(True)
        self.scrollArea_propSDCOpt.setObjectName("scrollArea_propImageOpt")
        self.scrollArea_propSDCOpt.setPalette(palette_scrollPlotProp)

        self.scrollAreaWidgetContents_propSDCOpt = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_propSDCOpt.setObjectName("scrollAreaWidgetContents_propSDCOpt")
        self.scrollArea_propSDCOpt.setWidget(self.scrollAreaWidgetContents_propSDCOpt)

        self.gridLayout_propSDCOpt = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_propSDCOpt)
        self.gridLayout_propSDCOpt.setObjectName("gridLayout_propSDCOpt")

        ui.gridLayout_TabPropSDC.addWidget(self.scrollArea_propSDC, 3, 0, 1, 1)
        ui.gridLayout_TabPropSDC.addWidget(self.scrollArea_propSDCOpt, 10, 0, 1, 1)

        # Scroll Area Propagation SDC Phase
        self.scrollArea_propSDC_phase = QtWidgets.QScrollArea(ui.tab_plotPropSDC)
        self.scrollArea_propSDC_phase.setPalette(palette_scrollPlotProp)
        self.scrollArea_propSDC_phase.setWidgetResizable(True)
        self.scrollArea_propSDC_phase.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)
        self.scrollArea_propSDC_phase.setObjectName("scrollArea_propSDC_phase")

        # Scroll Area Options Propagation SDC Phase
        self.scrollArea_propSDCOpt_phase = QtWidgets.QScrollArea(ui.tab_plotPropSDC)
        self.scrollArea_propSDCOpt_phase.setWidgetResizable(True)
        self.scrollArea_propSDCOpt_phase.setObjectName("scrollArea_propImageOpt_phase")
        self.scrollArea_propSDCOpt_phase.setPalette(palette_scrollPlotProp)

        self.scrollAreaWidgetContents_propSDCOpt_phase = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_propSDCOpt_phase.setObjectName("scrollAreaWidgetContents_propSDCOpt_phase")
        self.scrollArea_propSDCOpt_phase.setWidget(self.scrollAreaWidgetContents_propSDCOpt_phase)

        self.gridLayout_propSDCOpt_phase = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_propSDCOpt_phase)
        self.gridLayout_propSDCOpt_phase.setObjectName("gridLayout_propSDCOpt_phase")

        ui.gridLayout_TabPropSDC.addWidget(self.scrollArea_propSDC_phase, 3, 1, 1, 1)
        ui.gridLayout_TabPropSDC.addWidget(self.scrollArea_propSDCOpt_phase, 10, 1, 1, 1)
        #_______________________________________________________________________


        #=======================================================================
        # Parameters
        #=======================================================================
        # N
        self.N = N

        # W matrix
        self.W_matrix = W_matrix

        # User interface
        self.ui = ui

        # parent
        self.parent = self.scrollArea_propSDC
        self.parent_phase = self.scrollArea_propSDC_phase

        # parent optioncs
        self.parentOptions = self.scrollArea_propSDCOpt
        self.parentOptions_phase = self.scrollArea_propSDCOpt_phase

        # grid parent options
        self.gridOptions = self.gridLayout_propSDCOpt
        self.gridOptions_phase = self.gridLayout_propSDCOpt_phase

        # first plot
        self.first_plot = False
        #_______________________________________________________________________

        # Initial points (middle)
        self.P1x = int(N/2)
        self.P1y = int(N/2)
        self.P2x = int(N/2)

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
        # Plotting figure and configuring
        #=======================================================================

        # creating image prop
        self.propSDC_mag   = sqrt(self.W_matrix[self.P1x,self.P1y,self.P2x].real**2+self.W_matrix[self.P1x,self.P1y,self.P2x].imag**2)
        self.propSDC_phase = angle(self.W_matrix[self.P1y,self.P1y,self.P2x])

        # b array
        b_array = arange(0,self.N,1,dtype=float32)
        b_array -= int(self.N/2)
        b_array *= self.ui.dx_list[-1]

        # PLOT magnitude
        self.im, = self.axes.plot(b_array,self.propSDC_mag,marker="o",linewidth=1.0,label="SDC Mag")
        #self.cbar = self.fig.colorbar(self.im)
        self.leg = self.axes.legend()

        # PLOT phase
        self.im_phase, = self.axes_phase.plot(b_array,self.propSDC_phase,marker="o",linewidth=1.0,label="SDC Phase")
        #self.cbar_phase = self.fig_phase.colorbar(self.im_phase)
        self.leg_phase = self.axes_phase.legend()

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
        self.ui.gridLayout_TabPropSDC.addWidget(self.mpl_toolbar, 8, 0, 1, 3,alignment=QtCore.Qt.AlignLeft)
        self.ui.gridLayout_TabPropSDC.addWidget(self.mpl_toolbar_phase, 8, 1, 1, 3,alignment=QtCore.Qt.AlignLeft)

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
            self.matrix_points()
            self.figure_options()
            self.figure_options_phase()
            self.first_plot = True


    def matrix_points(self):

        # label Point P1x
        self.label_P1x = QtWidgets.QLabel(self.parentOptions)
        self.label_P1x.setObjectName("label_P1x")
        self.label_P1x.setText("x_1, y_1, x_2:")
        self.gridLayout_points.addWidget(self.label_P1x, 2, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit Point P1x
        self.lineEdit_P1x = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_P1x.setObjectName("lineEdit_P1x")
        self.gridLayout_points.addWidget(self.lineEdit_P1x,2, 2, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_P1x.setText(str(int(self.N/2)))
        #self.lineEdit_P1x.textChanged.connect(self.change_P1x)

        # line edit Point P1x
        self.lineEdit_P1y = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_P1y.setObjectName("lineEdit_P1y")
        self.gridLayout_points.addWidget(self.lineEdit_P1y,2, 4, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_P1y.setText(str(int(self.N/2)))
        #self.lineEdit_P1y.textChanged.connect(self.change_P1y)

        # line edit Point P2x
        self.lineEdit_P2x = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_P2x.setObjectName("lineEdit_P2x")
        self.gridLayout_points.addWidget(self.lineEdit_P2x,2, 6, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_P2x.setText(str(int(self.N/2)))
        #self.lineEdit_P2x.textChanged.connect(self.change_P2x)




    def figure_options(self):

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
        self.lineEdit_title.setText("Propagation SDC")

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
        self.lineEdit_xLabel.setText("x (m)")

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

        # checkbox grid
        self.checkBox_grid = QtWidgets.QCheckBox(self.parentOptions)
        self.checkBox_grid.setObjectName("Grid")
        self.gridOptions.addWidget(self.checkBox_grid, 30, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.checkBox_grid.setText("Grid")
        self.checkBox_grid.stateChanged.connect(self.change_grid)
        self.checkBox_grid.setChecked(True)

        # checkbox legend
        self.checkBox_legend = QtWidgets.QCheckBox(self.parentOptions)
        self.checkBox_legend.setObjectName("legend")
        self.gridOptions.addWidget(self.checkBox_legend, 32, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.checkBox_legend.setText("Legend")
        self.checkBox_legend.stateChanged.connect(self.change_legend)
        self.checkBox_legend.setChecked(True)

        # label legend font size
        self.label_legendFS = QtWidgets.QLabel(self.parentOptions)
        self.label_legendFS.setObjectName("label_legendFS")
        self.label_legendFS.setText("Legend Font Size")
        self.gridOptions.addWidget(self.label_legendFS, 34, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit legend font size
        self.lineEdit_legendFS = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_legendFS.setObjectName("label_legendFS")
        self.lineEdit_legendFS.textChanged.connect(self.change_legendFS)
        self.gridOptions.addWidget(self.lineEdit_legendFS,34, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_legendFS.setText(str(self.fsize))

        # label legend loc
        self.label_legendLOC = QtWidgets.QLabel(self.parentOptions)
        self.label_legendLOC.setObjectName("label_legendLOC")
        self.label_legendLOC.setText("Legend Location (1-10)")
        self.gridOptions.addWidget(self.label_legendLOC, 36, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit legend loc
        self.lineEdit_legendLOC = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_legendLOC.setObjectName("label_legendLOC")
        self.lineEdit_legendLOC.textChanged.connect(self.change_legendLOC)
        self.gridOptions.addWidget(self.lineEdit_legendLOC,36, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_legendLOC.setText(str(self.fsize))

        # label legend Text
        self.label_legendText = QtWidgets.QLabel(self.parentOptions)
        self.label_legendText.setObjectName("label_legendText")
        self.label_legendText.setText("Legend Text")
        self.gridOptions.addWidget(self.label_legendText, 37, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit legend Text
        self.lineEdit_legendText = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_legendText.setObjectName("label_legendText")
        self.lineEdit_legendText.textChanged.connect(self.change_legendText)
        self.gridOptions.addWidget(self.lineEdit_legendText,37, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_legendText.setText(str("SDC Magnitude"))
        self.change_legendText()

        # label combobox markers
        self.label_markerStyle = QtWidgets.QLabel(self.parentOptions)
        self.label_markerStyle.setObjectName("label_markerStyle")
        self.label_markerStyle.setText("Marker Style")
        self.gridOptions.addWidget(self.label_markerStyle, 38, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # combobox markers
        self.markers_dict = {"None":0, "o":1, ".":2, ",":3, "v":4, "^":5, "<":6, ">":7, "1":8, "2":9, "3":10, "4":11, "8":12, "s":13, "p":14, "P":15, "*":16, "h":17, "H":18, "+":19, "x": 20, "X":21, "D":22, "d":23, "|":24, "_":25}
        self.comboBox_markers = QtWidgets.QComboBox(self.parentOptions)
        self.comboBox_markers.setObjectName("comboBox_markers")
        self.comboBox_markers.addItems(self.markers_dict)
        self.gridOptions.addWidget(self.comboBox_markers, 38, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.comboBox_markers.currentIndexChanged.connect(self.change_markers)
        self.change_markers()

        # label Marker Size
        self.label_markerSize = QtWidgets.QLabel(self.parentOptions)
        self.label_markerSize.setObjectName("label_markerSize")
        self.label_markerSize.setText("Marker Size (10-30)")
        self.gridOptions.addWidget(self.label_markerSize, 40, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit Marker Size
        self.lineEdit_markerSize= QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_markerSize.setObjectName("label_markersize")
        self.lineEdit_markerSize.textChanged.connect(self.change_markerSize)
        self.gridOptions.addWidget(self.lineEdit_markerSize,40, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_markerSize.setText(str(6))
        self.change_markerSize()

        # label linewidth
        self.label_linewidth = QtWidgets.QLabel(self.parentOptions)
        self.label_linewidth.setObjectName("label_linewidth")
        self.label_linewidth.setText("Linewidth (1.0-12.0)")
        self.gridOptions.addWidget(self.label_linewidth, 42, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit linewidth
        self.lineEdit_linewidth = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_linewidth.setObjectName("label_linewidth")
        self.lineEdit_linewidth.textChanged.connect(self.change_linewidth)
        self.gridOptions.addWidget(self.lineEdit_linewidth,42, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_linewidth.setText(str(1.0))

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
            self.lineEdit_title_phase.setText("Prop SDC Phase")
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
            self.lineEdit_yLabel_phase.setText("y (m)")

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

            # checkbox grid_phase
            self.checkBox_grid_phase = QtWidgets.QCheckBox(self.parentOptions)
            self.checkBox_grid_phase.setObjectName("Grid_phase")
            self.gridOptions_phase.addWidget(self.checkBox_grid_phase, 30, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)
            self.checkBox_grid_phase.setText("Grid")
            self.checkBox_grid_phase.stateChanged.connect(self.change_grid_phase)
            self.checkBox_grid_phase.setChecked(True)

            # label Font Size_phase
            self.label_fsize_phase = QtWidgets.QLabel(self.parentOptions)
            self.label_fsize_phase.setObjectName("label_fsize")
            self.label_fsize_phase.setText("Font Size")
            self.gridOptions_phase.addWidget(self.label_fsize_phase, 22, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

            # checkbox legend_phase
            self.checkBox_legend_phase = QtWidgets.QCheckBox(self.parentOptions)
            self.checkBox_legend_phase.setObjectName("legend_phase")
            self.gridOptions_phase.addWidget(self.checkBox_legend_phase, 32, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)
            self.checkBox_legend_phase.setText("Legend")
            self.checkBox_legend_phase.stateChanged.connect(self.change_legend_phase)
            self.checkBox_legend_phase.setChecked(True)

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

            # label legend font size phase
            self.label_legendFS_phase = QtWidgets.QLabel(self.parentOptions)
            self.label_legendFS_phase.setObjectName("label_legendFS_phase")
            self.label_legendFS_phase.setText("Legend Font Size")
            self.gridOptions_phase.addWidget(self.label_legendFS_phase, 34, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

            # line edit legend font size phase
            self.lineEdit_legendFS_phase = QtWidgets.QLineEdit(self.parentOptions)
            self.lineEdit_legendFS_phase.setObjectName("label_legendFS")
            self.lineEdit_legendFS_phase.textChanged.connect(self.change_legendFS_phase)
            self.gridOptions_phase.addWidget(self.lineEdit_legendFS_phase,34, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
            self.lineEdit_legendFS_phase.setText(str(self.fsize))

            # label legend loc phase
            self.label_legendLOC_phase = QtWidgets.QLabel(self.parentOptions)
            self.label_legendLOC_phase.setObjectName("label_legendLOC_phase")
            self.label_legendLOC_phase.setText("Legend Location (1-10)")
            self.gridOptions_phase.addWidget(self.label_legendLOC_phase, 36, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

            # line edit legend loc phase
            self.lineEdit_legendLOC_phase = QtWidgets.QLineEdit(self.parentOptions)
            self.lineEdit_legendLOC_phase.setObjectName("label_legendLOC")
            self.lineEdit_legendLOC_phase.textChanged.connect(self.change_legendLOC)
            self.gridOptions_phase.addWidget(self.lineEdit_legendLOC_phase,36, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
            self.lineEdit_legendLOC_phase.setText(str(self.fsize))

            # label legend Text Phase
            self.label_legendText_phase = QtWidgets.QLabel(self.parentOptions)
            self.label_legendText_phase.setObjectName("label_legendText_phase")
            self.label_legendText_phase.setText("Legend Text")
            self.gridOptions_phase.addWidget(self.label_legendText_phase, 37, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

            # line edit legend Text Phase
            self.lineEdit_legendText_phase = QtWidgets.QLineEdit(self.parentOptions)
            self.lineEdit_legendText_phase.setObjectName("label_legendText_phase")
            self.lineEdit_legendText_phase.textChanged.connect(self.change_legendText_phase)
            self.gridOptions_phase.addWidget(self.lineEdit_legendText_phase,37, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
            self.lineEdit_legendText_phase.setText(str("SDC Phase"))
            self.change_legendText_phase()

            # label combobox markers phase
            self.label_markerStyle_phase = QtWidgets.QLabel(self.parentOptions)
            self.label_markerStyle_phase.setObjectName("label_markerStyle_phase")
            self.label_markerStyle_phase.setText("Marker Style")
            self.gridOptions_phase.addWidget(self.label_markerStyle_phase, 38, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

            # combobox markers
            self.comboBox_markers_phase = QtWidgets.QComboBox(self.parentOptions)
            self.comboBox_markers_phase.setObjectName("comboBox_markers_phase")
            self.comboBox_markers_phase.addItems(self.markers_dict)
            self.gridOptions_phase.addWidget(self.comboBox_markers_phase, 38, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
            self.comboBox_markers_phase.currentIndexChanged.connect(self.change_markers_phase)
            self.change_markers_phase()

            # label Marker Size Phase
            self.label_markerSize_phase = QtWidgets.QLabel(self.parentOptions)
            self.label_markerSize_phase.setObjectName("label_markerSize_phase")
            self.label_markerSize_phase.setText("Marker Size (10-30)")
            self.gridOptions_phase.addWidget(self.label_markerSize_phase, 40, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

            # line edit Marker Size Phase
            self.lineEdit_markerSize_phase= QtWidgets.QLineEdit(self.parentOptions)
            self.lineEdit_markerSize_phase.setObjectName("label_markersize_phase")
            self.lineEdit_markerSize_phase.textChanged.connect(self.change_markerSize_phase)
            self.gridOptions_phase.addWidget(self.lineEdit_markerSize_phase,40, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
            self.lineEdit_markerSize_phase.setText(str(6))
            self.change_markerSize_phase()

            # label linewidth Phase
            self.label_linewidth_phase = QtWidgets.QLabel(self.parentOptions)
            self.label_linewidth_phase.setObjectName("label_linewidth_phase")
            self.label_linewidth_phase.setText("Linewidth (1.0-12.0)")
            self.gridOptions_phase.addWidget(self.label_linewidth_phase, 42, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

            # line edit linewidth Phase
            self.lineEdit_linewidth_phase = QtWidgets.QLineEdit(self.parentOptions)
            self.lineEdit_linewidth_phase.setObjectName("label_linewidth_phase")
            self.lineEdit_linewidth_phase.textChanged.connect(self.change_linewidth_phase)
            self.gridOptions_phase.addWidget(self.lineEdit_linewidth_phase,42, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
            self.lineEdit_linewidth_phase.setText(str(1.0))
            #_______________________________________________________________________

        except Exception as error:
            self.ui.update_outputText(str(error))

    #===========================================================================
    # Functions
    #===========================================================================

    def change_point(self):
        try:
            self.P1x = int(self.lineEdit_P1x.text())
            self.P1y = int(self.lineEdit_P1y.text())
            self.P2x = int(self.lineEdit_P2x.text())

            if self.P1x>=0 and self.P1x<self.N:
                if self.P1y>=0 and self.P1y<self.N:
                    if self.P2x>=0 and self.P2x<self.N:
                        self.propSDC_mag   = sqrt(self.W_matrix[self.P1x,self.P1y,self.P2x].real**2+self.W_matrix[self.P1x,self.P1y,self.P2x].imag**2)
                        self.propSDC_phase = angle(self.W_matrix[self.P1y,self.P1y,self.P2x])

                        self.im.set_ydata(self.propSDC_mag)
                        self.im_phase.set_ydata(self.propSDC_phase)

                        self.update_draw()
                        #self.fig.canvas.flush_events()


        except Except as error:
            self.ui.update_outputText("Insert valid points.")
            #if debug:
                #self.ui.update_outputText(str(error)+" at <windowPlot_propSDC> in <change_point> function.")

    def update_draw(self):
        self.canvas.draw()
        self.canvas.updateGeometry()
        self.canvas_phase.draw()
        self.canvas_phase.updateGeometry()



    #---------------------------------------------------------------------------
    # Magnitude
    #---------------------------------------------------------------------------
    def change_linewidth(self):
        try:
            self.axes.lines[0].set_linewidth(float(self.lineEdit_linewidth.text()))
            self.canvas.draw()
        except Exception as error:
            pass

    def change_legendText(self):
        try:
            self.axes.legend(labels=[str(self.lineEdit_legendText.text())])
            self.canvas.draw()
        except Exception as error:
            pass
            #self.ui.update_outputText(error)

    def change_markerSize(self):
        try:
            self.axes.lines[0].set_markersize(int(self.lineEdit_markerSize.text()))
            self.canvas.draw()
        except Exception as error:
            pass

    def change_markers(self):
        try:
            if self.comboBox_markers.currentIndex()==0:
                self.axes.lines[0].set_marker(None)
                self.canvas.draw()
            else:
                self.axes.lines[0].set_marker(str(self.comboBox_markers.currentText()))
                self.canvas.draw()
        except Exception as error:
            pass
            #self.ui.update_outputText(error)

    def change_legendLOC(self):
        try:
            new = self.lineEdit_legendLOC.text()
            if new != "":
                new = int(self.lineEdit_legendLOC.text())
                if new>=1 and new<=10:
                    self.axes.legend(loc=new)
                    self.canvas.draw()
        except Exception as error:
            pass
            #self.ui.update_outputText(error)

    def change_legendFS(self):
        try:
            new = self.lineEdit_legendFS.text()
            if new != "":
                new = int(self.lineEdit_legendFS.text())
                self.axes.legend(fontsize=new)
                self.canvas.draw()
        except Exception as error:
            pass #self.ui.update_outputText(error)

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

        except Exception as error:
            pass #self.ui.update_outputText(error)


    def change_grid(self):
        try:
            if self.checkBox_grid.checkState():
                self.axes.grid(True)
                self.canvas.draw()
            else:
                self.axes.grid(False)
                self.canvas.draw()
        except Exception as error:
            pass
            #self.ui.update_outputText(error)


    def change_legend(self):
        try:
            if self.checkBox_legend.checkState():
                self.axes.legend().set_visible(True)
                self.canvas.draw()
            else:
                self.axes.legend().set_visible(False)
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
                for i in range(1,Ntxt):
                    if temp_txt[i] == ",":
                        numList.append(float(actual))
                        actual = ""
                    elif temp_txt[i]==")":
                        numList.append(float(actual))
                    else:
                        actual+=temp_txt[i]
            self.axes.set_xlim(numList[0],numList[1])
            self.canvas.draw()
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
                for i in range(1,Ntxt):
                    if temp_txt[i] == ",":
                        numList.append(float(actual))
                        actual = ""
                    elif temp_txt[i]==")":
                        numList.append(float(actual))
                    else:
                        actual+=temp_txt[i]
            self.axes.set_ylim(numList[0],numList[1])
            self.canvas.draw()
        except Exception as error:
            pass #self.ui.update_outputText(error)

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
                pass #self.ui.update_outputText(str(error))

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


    #---------------------------------------------------------------------------
    # Phase
    #---------------------------------------------------------------------------
    def change_linewidth_phase(self):
        try:
            self.axes_phase.lines[0].set_linewidth(float(self.lineEdit_linewidth_phase.text()))
            self.canvas_phase.draw()
        except Exception as error:
            pass

    def change_legendText_phase(self):
        try:
            self.axes_phase.legend(labels=[str(self.lineEdit_legendText_phase.text())])
            self.canvas_phase.draw()
        except Exception as error:
            pass #self.ui.update_outputText(error)

    def change_markerSize_phase(self):
        try:
            self.axes_phase.lines[0].set_markersize(int(self.lineEdit_markerSize_phase.text()))
            self.canvas_phase.draw()
        except Exception as error:
            pass

    def change_markers_phase(self):
        try:
            if self.comboBox_markers_phase.currentIndex()==0:
                self.axes_phase.lines[0].set_marker(None)
                self.canvas_phase.draw()
            else:
                self.axes_phase.lines[0].set_marker(str(self.comboBox_markers_phase.currentText()))
                self.canvas_phase.draw()
        except Exception as error:
            pass #self.ui.update_outputText(error)

    def change_legendLOC_phase(self):
        try:
            new = self.lineEdit_legendLOC_phase.text()
            if new != "":
                new = int(self.lineEdit_legendLOC_phase.text())
                if new>=1 and new<=10:
                    self.axes_phase.legend(loc=new)
                    self.canvas_phase.draw()
        except Exception as error:
            pass #self.ui.update_outputText(error)

    def change_legendFS_phase(self):
        try:
            new = self.lineEdit_legendFS_phase.text()
            if new != "":
                new = int(self.lineEdit_legendFS_phase.text())
                self.axes_phase.legend(fontsize=new)
                self.canvas_phase.draw()
        except Exception as error:
            pass #self.ui.update_outputText(error)

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


    def change_grid_phase(self):
        try:
            if self.checkBox_grid_phase.checkState():
                self.axes_phase.grid(True)
                self.canvas_phase.draw()
            else:
                self.axes_phase.grid(False)
                self.canvas_phase.draw()
        except Exception as error:
            pass
            #self.ui.update_outputText(error)

    def change_legend_phase(self):
        try:
            if self.checkBox_legend_phase.checkState():
                self.axes_phase.legend().set_visible(True)
                self.canvas_phase.draw()
            else:
                self.axes_phase.legend().set_visible(False)
                self.canvas_phase.draw()

        except Exception as error:
            pass #self.ui.update_outputText(error)


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
                pass #self.ui.update_outputText(str(error))

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

    #___________________________________________________________________________



    #---------------------------------------------------------------------------
    #///////////////////////////////////////////////////////////////////////////
    #---------------------------------------------------------------------------
