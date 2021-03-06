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

import os
current_dir = os.getcwd()
up_dir = os.path.dirname(current_dir)
sys.path.insert(1, up_dir)
from palettes import *



class Canvas_propImage:

    def __init__(self,ui,W_matrix,N):

        ui.list_of_tabs.append(QtWidgets.QWidget())
        ui.list_of_tabs[-1].setObjectName("tab_plotPropImage") #self.tab_plotPropImage.setObjectName("tab_plotPropImage")

        # gridlayout TAB SourceImag
        ui.list_grid_tabs.append(QtWidgets.QGridLayout(ui.list_of_tabs[-1])) #self.gridLayout_TabPropImage = QtWidgets.QGridLayout(self.tab_plotPropImage)
        ui.list_grid_tabs[-1].setObjectName("gridLayout_TabPropImage") #self.gridLayout_TabPropImage.setObjectName("gridLayout_TabPropImage")

        # Scroll Area prop Image
        ui.scrollArea_propImage = QtWidgets.QScrollArea(ui.list_of_tabs[-1])
        ui.scrollArea_propImage.setPalette(palette_scrollPlotProp)
        ui.scrollArea_propImage.setWidgetResizable(True)
        ui.scrollArea_propImage.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)
        ui.scrollArea_propImage.setObjectName("scrollArea_propImage")

        # Scroll Area Options prop
        ui.scrollArea_propImageOpt = QtWidgets.QScrollArea(ui.list_of_tabs[-1])
        ui.scrollArea_propImageOpt.setWidgetResizable(True)
        ui.scrollArea_propImageOpt.setObjectName("scrollArea_propImageOpt")
        ui.scrollArea_propImageOpt.setPalette(palette_scrollPlotProp)

        ui.scrollAreaWidgetContents_propImageOpt = QtWidgets.QWidget()
        ui.scrollAreaWidgetContents_propImageOpt.setObjectName("scrollAreaWidgetContents_propImageOpt")
        ui.scrollArea_propImageOpt.setWidget(ui.scrollAreaWidgetContents_propImageOpt)

        ui.gridLayout_propImageOpt = QtWidgets.QGridLayout(ui.scrollAreaWidgetContents_propImageOpt)
        ui.gridLayout_propImageOpt.setObjectName("gridLayout_propImageOpt")

        ui.list_grid_tabs[-1].addWidget(ui.scrollArea_propImage, 1, 0, 1, 1)
        ui.list_grid_tabs[-1].addWidget(ui.scrollArea_propImageOpt, 3, 0, 1, 1)


        #=======================================================================
        # Parameters
        #=======================================================================
        # User interface
        self.ui = ui

        # parent
        self.parent = ui.scrollArea_propImage

        # parent optioncs
        self.parentOptions = ui.scrollArea_propImageOpt

        # grid parent options
        self.gridOptions = ui.gridLayout_propImageOpt
        #_______________________________________________________________________


        self.build_fig(W_matrix,N)


    def build_fig(self,W_matrix,N):

        #=======================================================================
        # Create the mpl Figure and FigCanvas objects.
        #=======================================================================
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)

        # Since we have only one plot, we can use add_axes
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        self.axes = self.fig.add_subplot(111)
        #_______________________________________________________________________


        #=======================================================================
        # Plotting 2D figure and configuring
        #=======================================================================
        #
        # creating image prop
        image_prop = zeros((N,N))
        for i in range(0,N):
            for j in range(0,N):
                image_prop[i,j]=W_matrix[i,j,i,j].real

        # PLOT
        self.im = self.axes.pcolormesh(image_prop)
        self.cbar = self.fig.colorbar(self.im)

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
        self.ui.list_grid_tabs[-1].addWidget(self.mpl_toolbar, 2, 0, 1, 3)     #gridLayout_TabPropImage.addWidget(self.mpl_toolbar, 2, 0, 1, 3)
        #_______________________________________________________________________


        #=======================================================================
        # Canvas in Scroll Area
        #=======================================================================
        self.label_opt = QtWidgets.QLabel()
        self.label_opt.setObjectName("label_opt")
        self.label_opt.setText("Plot Options:")
        #self.gridOptions.addWidget(self.label_opt, 3, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

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
        # Figure Options
        #=======================================================================

        # Options
        """
        self.label_opt = QtWidgets.QLabel(self.parentOptions)
        self.label_opt.setObjectName("label_opt")
        self.label_opt.setText("Plot Options:")
        self.gridOptions.addWidget(self.label_opt, 3, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)
        """

        # label title
        self.label_title = QtWidgets.QLabel(self.parentOptions)
        self.label_title.setObjectName("label_title")
        self.label_title.setText("Title")
        self.gridOptions.addWidget(self.label_title, 4, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit title label
        self.lineEdit_title = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_title.setObjectName("lineEdit_title")
        self.lineEdit_title.textChanged.connect(self.change_title)
        self.gridOptions.addWidget(self.lineEdit_title,4, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.change_title()
        self.lineEdit_title.setText("Propagation Image")

        # label x
        self.label_x = QtWidgets.QLabel(self.parentOptions)
        self.label_x.setObjectName("label_x")
        self.label_x.setText("Label x-axis")
        self.gridOptions.addWidget(self.label_x, 6, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit x label
        self.lineEdit_xLabel = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_xLabel.setObjectName("lineEdit_xlabel")
        self.lineEdit_xLabel.textChanged.connect(self.change_labelx)
        self.gridOptions.addWidget(self.lineEdit_xLabel,6, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.change_labelx()
        self.lineEdit_xLabel.setText("x")

        # label y
        self.label_y = QtWidgets.QLabel(self.parentOptions)
        self.label_y.setObjectName("label_y")
        self.label_y.setText("Label y-axis")
        self.gridOptions.addWidget(self.label_y, 8, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit y label
        self.lineEdit_yLabel = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_yLabel.setObjectName("lineEdit_ylabel")
        self.lineEdit_yLabel.textChanged.connect(self.change_labely)
        self.gridOptions.addWidget(self.lineEdit_yLabel,8, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.change_labely()
        self.lineEdit_yLabel.setText("y")

        # label xlim
        self.label_xlim = QtWidgets.QLabel(self.parentOptions)
        self.label_xlim.setObjectName("label_xlim")
        self.label_xlim.setText("xlim")
        self.gridOptions.addWidget(self.label_xlim, 10, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit xlim
        self.lineEdit_xlim = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_xlim.setObjectName("lineEdit_ylabel")
        self.lineEdit_xlim.textChanged.connect(self.change_xlim)
        self.gridOptions.addWidget(self.lineEdit_xlim,10, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_xlim.setText("(_,_)")
        self.change_xlim()

        # label ylim
        self.label_ylim = QtWidgets.QLabel(self.parentOptions)
        self.label_ylim.setObjectName("label_ylim")
        self.label_ylim.setText("ylim")
        self.gridOptions.addWidget(self.label_ylim, 12, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit ylim
        self.lineEdit_ylim = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_ylim.setObjectName("lineEdit_ylabel")
        self.lineEdit_ylim.textChanged.connect(self.change_ylim)
        self.gridOptions.addWidget(self.lineEdit_ylim,12, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_ylim.setText("(_,_)")
        self.change_ylim()

        # label cmap
        self.label_cmap = QtWidgets.QLabel(self.parentOptions)
        self.label_cmap.setObjectName("label_cmap")
        self.label_cmap.setText("Color Map")
        self.gridOptions.addWidget(self.label_cmap, 18, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit cmap
        self.lineEdit_cmap = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_cmap.setObjectName("lineEdit_cmap")
        self.lineEdit_cmap.textChanged.connect(self.change_cmap)
        self.gridOptions.addWidget(self.lineEdit_cmap,18, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_cmap.setText("hot")
        self.change_cmap()

        # label Font Size
        self.label_fsize = QtWidgets.QLabel(self.parentOptions)
        self.label_fsize.setObjectName("label_fsize")
        self.label_fsize.setText("Font Size")
        self.gridOptions.addWidget(self.label_fsize, 20, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit font size
        self.lineEdit_fsize = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_fsize.setObjectName("label_fsize")
        self.lineEdit_fsize.textChanged.connect(self.change_fsize)
        self.gridOptions.addWidget(self.lineEdit_fsize,20, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_fsize.setText(str(self.fsize))
        self.change_fsize()

        # label DPI
        self.label_dpi = QtWidgets.QLabel(self.parentOptions)
        self.label_dpi.setObjectName("label_dpi")
        self.label_dpi.setText("dpi (100-500)")
        self.gridOptions.addWidget(self.label_dpi, 22, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

        # line edit DPI
        self.lineEdit_dpi = QtWidgets.QLineEdit(self.parentOptions)
        self.lineEdit_dpi.setObjectName("label_dpi")
        self.lineEdit_dpi.textChanged.connect(self.change_dpi)
        self.gridOptions.addWidget(self.lineEdit_dpi,22, 1, 1, 1,alignment=QtCore.Qt.AlignLeft)
        self.lineEdit_dpi.setText(str(self.dpi))
        self.change_fsize()




    def update_draw(self):
        self.canvas.draw()
        self.canvas.updateGeometry()


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
