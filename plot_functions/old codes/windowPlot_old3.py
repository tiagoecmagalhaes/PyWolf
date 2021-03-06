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




class Canvas_sourceImage:

    def __init__(self,ui,parent,parentOptions,gridOptions,W_matrix,N):

        # SI = Source Image
        self.ui = ui

        self.parentOptions = parentOptions
        self.gridOptions = gridOptions

        self.frame_sourceImage = parent

        # Create the mpl Figure and FigCanvas objects.
        # 5x4 inches, 100 dots-per-inch
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)

        #



        #self.canvas.updateGeometry()


        #ui.gridLayout_sourceImage.addWidget(self.canvas)


        #self.frame_sourceImage.setWidget(self.canvas)
        #self.frame_sourceImage.setMaximumHeight(self.canvas.height()+10)
        #self.frame_sourceImage.setMaximumWidth(self.canvas.width()+10)

        #ui.gridLayout_sourceImage.addWidget(self.canvas, 1, 0, 1, 5)

        # Since we have only one plot, we can use add_axes
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        self.axes = self.fig.add_subplot(111)

        # creating image source
        image_source = zeros((N,N))
        for i in range(0,N):
            for j in range(0,N):
                image_source[i,j]=W_matrix[i,j,i,j].real

        # PLOT
        self.im = self.axes.pcolormesh(image_source)
        self.cbar = self.fig.colorbar(self.im)

        # font size
        self.fsize = 12

        # x,y Labels
        self.axes.set_xlabel("x (m)",fontsize = self.fsize)
        self.axes.set_ylabel("y (m)",fontsize = self.fsize)

        # Bind the 'pick' event for clicking on one of the bars
        self.canvas.mpl_connect('pick_event', ui.on_pick)
        #self.canvas.mpl_connect("scroll_event", ui.scrolling)

        #ui.scrollArea_sourceImage.setWidget(self.canvas)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.frame_sourceImage)
        ui.gridLayout_TabSourceImage.addWidget(self.mpl_toolbar, 2, 0, 1, 3)


        """

        # Other GUI controls
        #

        self.textbox = QLineEdit()
        self.textbox.setMinimumWidth(200)
        self.textbox.editingFinished.connect(ui.draw_sourceImage)

        self.draw_button = QPushButton("&Draw")
        self.draw_button.clicked.connect(ui.draw_sourceImage)

        self.grid_cb = QCheckBox("Show &Grid")
        self.grid_cb.setChecked(False)
        self.grid_cb.stateChanged.connect(ui.draw_sourceImage)

        slider_label = QLabel('Bar width (%):')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 100)
        self.slider.setValue(20)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(ui.draw_sourceImage)



        #
        # Layout with box sizers
        #

        hbox = QHBoxLayout()

        for w in [  self.textbox, self.draw_button, self.grid_cb,
                    slider_label, self.slider]:
            hbox.addWidget(w)
            hbox.setAlignment(w, Qt.AlignVCenter)

        """




        #self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)

        self.containerGraph = QWidget(parent)
        #self.containerGraph.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)

        self.vbox = QVBoxLayout(self.containerGraph)

        self.vbox.addWidget(self.canvas)

        #self.canvas.setParent(self.containerGraph)


        #

        #vbox.addWidget(self.mpl_toolbar)
        #vbox.addLayout(hbox)


        #parent.setLayout(vbox)
        #vbox.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)
        #ui.scrollArea_sourceImage.setLayout(vbox)





        #ui.gridLayout_sourceImage.addWidget(self.containerGraph)





        #ui.setCentralWidget(self.frame_sourceImage)

        #=======================================================================
        # Figure Options
        #=======================================================================

        # Options
        self.label_opt = QtWidgets.QLabel(self.parentOptions)
        self.label_opt.setObjectName("label_pot")
        self.label_opt.setText("Plot Options:")
        self.gridOptions.addWidget(self.label_opt, 3, 0, 1, 1,alignment=QtCore.Qt.AlignLeft)

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
        self.lineEdit_title.setText("Source Image")

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

        #self.ui.gridLayout_sourceImage.setRowMinimumHeight(1, int(2*self.canvas.height()))
        # update size
        #ui.scrollAreaWidgetContents_sourceImageOpt.setMaximumHeight(int(self.canvas.height()/2))


        #ui.scrollArea_sourceImage.setMinimumHeight(self.canvas.height()+500)


        #ui.gridLayout_TabSourceImage.setRowMinimumHeight(1, self.canvas.height()+10)
        self.canvas.updateGeometry()

    def update_gridSize(self):
        self.canvas.draw()
        self.ui.update_outputText(self.canvas.height())

    def change_fsize(self):
        try:
            self.fsize = int(self.lineEdit_fsize.text())
            self.change_title()
            self.change_labelx()
            self.change_labely()
            self.update_gridSize()
            print(self.fsize)

        except Exception as error:
            self.ui.update_outputText(error)


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
            self.ui.update_outputText(error)

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
            self.ui.update_outputText(error)

    def change_title(self):
        self.axes.set_title(self.lineEdit_title.text(),fontsize = self.fsize)
        self.canvas.draw()

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
