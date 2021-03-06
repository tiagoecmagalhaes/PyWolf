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

import os
current_dir = os.getcwd()
up_dir = os.path.dirname(current_dir)
sys.path.insert(1, up_dir)
from palettes import *
from fonts import *



class Canvas_propSpec:

    def __init__(self,ui,CSDA,CSDA_source,N):

        # tab
        ui.list_of_tabs.append(QtWidgets.QWidget())  # ui.gridLayout_TabSourceImage
        ui.list_of_tabs[-1].setObjectName("tab_plotSourceSpec")

        #ui.tab_plotSourceSpec = QtWidgets.QWidget()
        #ui.tab_plotSourceSpec.setObjectName("tab_plotSourceSpec")

        # gridlayout TAB Source Spectrum
        ui.list_grid_tabs.append(QtWidgets.QGridLayout(ui.list_of_tabs[-1]))
        ui.list_grid_tabs[-1].setObjectName("gridLayout_TabSourceSpec")
        #ui.gridLayout_TabSourceSpec = QtWidgets.QGridLayout(ui.list_of_tabs[-1])
        #ui.gridLayout_TabSourceSpec.setObjectName("gridLayout_TabSourceSpec")


        # Scroll Area Source Spectrum
        ui.scrollArea_sourceSpec = QtWidgets.QScrollArea(ui.list_of_tabs[-1])
        ui.scrollArea_sourceSpec.setPalette(palette_scrollPlotProp)
        ui.scrollArea_sourceSpec.setWidgetResizable(True)
        ui.scrollArea_sourceSpec.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)
        ui.scrollArea_sourceSpec.setObjectName("scrollArea_sourceSpec")

        # Scroll Area Options Source Spectrum
        ui.scrollArea_sourceSpecOpt = QtWidgets.QScrollArea(ui.list_of_tabs[-1])
        ui.scrollArea_sourceSpecOpt.setWidgetResizable(True)
        ui.scrollArea_sourceSpecOpt.setObjectName("scrollArea_sourceSpecOpt")
        ui.scrollArea_sourceSpecOpt.setPalette(palette_scrollPlotProp)

        ui.scrollAreaWidgetContents_sourceSpecOpt = QtWidgets.QWidget()
        ui.scrollAreaWidgetContents_sourceSpecOpt.setObjectName("scrollAreaWidgetContents_sourceSpecOpt")
        ui.scrollArea_sourceSpecOpt.setWidget(ui.scrollAreaWidgetContents_sourceSpecOpt)

        ui.gridLayout_sourceSpecOpt = QtWidgets.QGridLayout(ui.scrollAreaWidgetContents_sourceSpecOpt)
        ui.gridLayout_sourceSpecOpt.setObjectName("gridLayout_sourceSpecOpt")

        ui.list_grid_tabs[-1].addWidget(ui.scrollArea_sourceSpec, 3, 0, 1, 1)
        ui.list_grid_tabs[-1].addWidget(ui.scrollArea_sourceSpecOpt, 10, 0, 1, 1)


        #_______________________________________________________________________


        #=======================================================================
        # Parameters
        #=======================================================================
        # N
        self.N = N

        # W matrix
        self.CSDA = CSDA
        self.CSDA_source = CSDA_source

        # User interface
        self.ui = ui

        # parent
        self.parent = ui.scrollArea_sourceSpec

        # parent optioncs
        self.parentOptions = ui.scrollArea_sourceSpecOpt

        # grid parent options
        self.gridOptions = ui.gridLayout_sourceSpecOpt


        # first plot
        self.first_plot = False
        #_______________________________________________________________________

        # Initial points (middle)
        #self.P1x = int(N/2)
        #self.P1y = int(N/2)
        #self.P2x = int(N/2)

        self.build_fig()



    def build_fig(self):

        #=======================================================================
        # Create the mpl Figure and FigCanvas objects.
        #=======================================================================
        # magnitude
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)

        # axes
        self.axes = self.fig.add_subplot(111)
        #_______________________________________________________________________



        #=======================================================================
        # Plotting figure and configuring
        #=======================================================================

        # creating image prop
        spectrum        = self.CSDA.spectrum/self.CSDA.spectrum.max()
        source_spectrum = self.CSDA_source.spectrum/self.CSDA_source.spectrum.max()

        # b array
        b_array=self.CSDA.omega_array

        # PLOT magnitude
        self.im  = self.axes.plot(b_array,spectrum,marker="o",linewidth=1.0,label="Propagation Spectrum",color="blue")
        self.im2 = self.axes.plot(b_array,source_spectrum,marker="o",linewidth=1.0,label="Source Spectrum",color="red")

        #self.cbar = self.fig.colorbar(self.im)
        self.leg = self.axes.legend()

        # font size
        self.fsize = 12

        # x,y Labels
        self.axes.set_xlabel("x (m)",fontsize = self.fsize)
        self.axes.set_ylabel("y (m)",fontsize = self.fsize)


        #_______________________________________________________________________


        #=======================================================================
        # Tool bar
        #=======================================================================

        # Bind the 'pick' event for clicking on one of the bars
        self.canvas.mpl_connect('pick_event', self.ui.on_pick) #self.canvas.mpl_connect("scroll_event", ui.scrolling)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.parent)

        #ui.gridLayout_TabPropImage.addWidget(self.mpl_toolbar, 2, 0, 1, 3)
        self.ui.list_grid_tabs[-1].addWidget(self.mpl_toolbar, 8, 0, 1, 3,alignment=QtCore.Qt.AlignLeft)
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


        if not self.first_plot:
            self.figure_options()
            self.first_plot = True


    def figure_options(self):

        """
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

        """
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
        self.lineEdit_title.setText("Source Spectrum")

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
        self.lineEdit_xLabel.setText(r'$\omega\,(\mathrm{rad\,s^{-1})}$')

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
        self.lineEdit_yLabel.setText("Normalized Spectrum (a.u.)")

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
        self.lineEdit_legendText.setText(str("Spectrum"))
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
        #self.change_markers()

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


    #===========================================================================
    # Functions
    #===========================================================================

    def change_P1x(self):
        try:
            temp = self.lineEdit_P1x.text()
            if temp != "":
                new = int(temp)
                if new>=0 and new<self.N:
                    self.P1x = new
                    #self.update_pcolor()
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
                    #self.update_pcolor()
                    self.update_draw()
        except Except as error:
            self.ui.update_outputText(str(error))

    def update_draw(self):
        self.canvas.draw()
        self.canvas.updateGeometry()


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
            self.ui.update_outputText(error)

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
            self.ui.update_outputText(error)

    def change_legendLOC(self):
        try:
            new = self.lineEdit_legendLOC.text()
            if new != "":
                new = int(self.lineEdit_legendLOC.text())
                if new>=1 and new<=10:
                    self.axes.legend(loc=new)
                    self.canvas.draw()
        except Exception as error:
            self.ui.update_outputText(error)

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
            ##print(self.fsize)

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
            self.ui.update_outputText(error)


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


    #---------------------------------------------------------------------------
    #///////////////////////////////////////////////////////////////////////////
    #---------------------------------------------------------------------------
