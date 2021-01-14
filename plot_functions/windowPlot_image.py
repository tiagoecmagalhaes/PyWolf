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


#===============================================================================
# Importing Packages
#===============================================================================

# sys, os, random
import sys, os, random

# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Matplotlib
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# Numpy
from numpy import zeros
from numpy import arange
from numpy import float32
from numpy import flip

# Adding directories to import packages
current_dir = os.getcwd()
up_dir = os.path.dirname(current_dir)
sys.path.insert(1, up_dir)
sys.path.insert(1, up_dir+"\\styles\\")

# PyWolf packages
from palettes import *
from fonts import *
from color import *

#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Class Canvas Image
#===============================================================================

class Canvas_Image:

    def __init__(self,ui,W_image,N,dx,title="Image"):

        try:
            # reset stylesheet
            ui.tabWidget_plots.setStyleSheet("")
            ui.tabWidget_plots.setPalette(palette_TabPlots)
            ui.tabWidget_plots.setObjectName("tabWidget_plots")
            ui.tabWidget_plots.setMinimumHeight(2*ui.rect.height()/3)
            ui.tabWidget_plots.setFont(font_semititle)

            # tab
            ui.list_of_tabs.append(QtWidgets.QWidget())  # ui.gridLayout_TabSourceImage
            ui.list_of_tabs[-1].setObjectName("tab_plotSourceImage")

            # gridlayout TAB SourceImag
            ui.list_grid_tabs.append(QtWidgets.QGridLayout(ui.list_of_tabs[-1]))
            ui.list_grid_tabs[-1].setObjectName("gridLayout_TabSourceImage")

            # Scroll Area Source Image
            self.scrollArea_sourceImage = QtWidgets.QScrollArea(ui.list_of_tabs[-1])
            self.scrollArea_sourceImage.setPalette(palette_scrollPlotProp)
            self.scrollArea_sourceImage.setWidgetResizable(True)
            self.scrollArea_sourceImage.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)
            self.scrollArea_sourceImage.setObjectName("scrollArea_sourceImage")

            # Scroll Area Options Source
            self.scrollArea_sourceImageOpt = QtWidgets.QScrollArea(ui.list_of_tabs[-1])
            self.scrollArea_sourceImageOpt.setWidgetResizable(True)
            self.scrollArea_sourceImageOpt.setObjectName("scrollArea_sourceImageOpt")
            self.scrollArea_sourceImageOpt.setPalette(palette_scrollPlotProp)

            self.scrollAreaWidgetContents_sourceImageOpt = QtWidgets.QWidget()
            self.scrollAreaWidgetContents_sourceImageOpt.setObjectName("scrollAreaWidgetContents_sourceImageOpt")
            self.scrollArea_sourceImageOpt.setWidget(self.scrollAreaWidgetContents_sourceImageOpt)

            self.gridLayout_sourceImageOpt = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_sourceImageOpt)
            self.gridLayout_sourceImageOpt.setObjectName("gridLayout_sourceImageOpt")

            ui.list_grid_tabs[-1].addWidget(self.scrollArea_sourceImage, 1, 0, 1, 1)
            ui.list_grid_tabs[-1].addWidget(self.scrollArea_sourceImageOpt, 3, 0, 1, 1)

            #=======================================================================
            # Parameters
            #=======================================================================
            # N
            self.N = N

            # spatial resolution
            self.dx = dx

            # User interface
            self.ui = ui

            # title
            self.title = title

            # parent
            self.parent = self.scrollArea_sourceImage

            # parent optioncs
            self.parentOptions = self.scrollArea_sourceImageOpt

            # grid parent options
            self.gridOptions = self.gridLayout_sourceImageOpt
            #_______________________________________________________________________

            # calling function
            self.build_fig(W_image,N)

        except Exception as error:
            ui.update_outputText(str(error)+" in <windowPlot>: __init__")




    def build_fig(self,W_image,N):
        try:

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
            """
            # creating image source
            image_source = zeros((N,N))
            for i in range(0,N):
                for j in range(0,N):
                    image_source[i,j]=W_image[i,j,i,j].real
            """

            image_source = W_image

            # xy array
            self.x_array = arange(0,self.N,1,dtype=float32)
            self.x_array -= int(self.N/2)
            self.x_array *= self.dx

            # PLOT
            self.im = self.axes.pcolormesh(self.x_array,self.x_array,flip(image_source,0),shading="auto")
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

            #ui.gridLayout_TabSourceImage.addWidget(self.mpl_toolbar, 2, 0, 1, 3)
            self.ui.list_grid_tabs[-1].addWidget(self.mpl_toolbar, 2, 0, 1, 3) # self.ui.gridLayout_TabSourceImage
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
            self.lineEdit_title.setText(self.title)
            self.change_title()

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

        except Exception as error:
            self.ui.update_outputText(str(error)+" in <windowPlot>: build_fig")


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
            self.title = str(self.lineEdit_title.text())
        except:
            pass

    def change_labelx(self):
        if self.lineEdit_xLabel.text()=="":
            self.axes.set_xlabel("")
        else:
            try:
                self.axes.set_xlabel(self.lineEdit_xLabel.text(),fontsize = self.fsize)
                self.canvas.draw()
            except:
                pass
                #self.ui.update_outputText("Unable to update x-label.")

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


#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================