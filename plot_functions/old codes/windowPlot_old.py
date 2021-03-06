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
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QInputDialog, QFileDialog, QLabel, QHBoxLayout, QMainWindow, QApplication, QPushButton, QVBoxLayout

#from QtGui import QVBoxLayout

import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable

import numpy as np
from pylab import *

from numpy import zeros



class Canvas_source(FigureCanvas):
    def __init__(self, parent, ui, row, title, width = 5, height = 5, dpi = 100):

        self.parent = parent
        self.ui = ui
        self.title = title

        fig = Figure(figsize=(width, height), dpi=dpi)
        #self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        #self.plot_sourceImage(ui,title)
        self.fig = fig



    def plot_sourceImage(self,ui,W_matrix,N,title):

        # creating image source
        image_source = zeros((N,N))
        for i in range(0,N):
            for j in range(0,N):
                image_source[i,j]=W_matrix[i,j,i,j].real

        # plotting
        self.ax = self.figure.add_subplot()
        self.ax.set_title(self.title)
        newFig = self.ax.imshow(image_source,cmap="hot")

        # putting color bar...
        divider = make_axes_locatable(self.ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar =self.fig.colorbar(newFig,cax=cax)
        #rc('text', usetex=True) # latex


        # navigation bar
        self.nav = NavigationToolbar(self, self.parent, coordinates = False)
        self.nav.setMinimumWidth(300)
        self.nav.setStyleSheet("QToolBar { border: 0px }")
        self.nav.setMinimumWidth(300)
        self.nav.move(100,100)
        ui.tab_plotSourceImage.layout().addWidget(self.nav)
        #ui.gridLayout_tabPlotSource.addWidget(self.nav,0,0,1,3)

        # label title
        self.label_title = QtWidgets.QLabel(ui.scrollAreaWidgetContents_plotSourceImage)
        self.label_title.setObjectName("label_title")
        self.label_title.setText("Title")
        ui.gridLayout_plotSourceImage.addWidget(self.label_title, 4, 0, 1, 3,alignment=QtCore.Qt.AlignLeft)

        # line edit title label
        self.lineEdit_title = QtWidgets.QLineEdit(ui.scrollAreaWidgetContents_plotSourceImage)
        self.lineEdit_title.setObjectName("lineEdit_title")
        self.lineEdit_title.textChanged.connect(self.change_title)
        ui.gridLayout_plotSourceImage.addWidget(self.lineEdit_title,4, 1, 1, 3,alignment=QtCore.Qt.AlignLeft)
        self.change_title()
        self.lineEdit_title.setText("Source Image")

        # label x
        self.label_x = QtWidgets.QLabel(ui.scrollAreaWidgetContents_plotSourceImage)
        self.label_x.setObjectName("label_x")
        self.label_x.setText("Label x-axis")
        ui.gridLayout_plotSourceImage.addWidget(self.label_x, 6, 0, 1, 3,alignment=QtCore.Qt.AlignLeft)

        # line edit x label
        self.lineEdit_xLabel = QtWidgets.QLineEdit(ui.scrollAreaWidgetContents_plotSourceImage)
        self.lineEdit_xLabel.setObjectName("lineEdit_xlabel")
        self.lineEdit_xLabel.textChanged.connect(self.change_labelx)
        ui.gridLayout_plotSourceImage.addWidget(self.lineEdit_xLabel,6, 1, 1, 3,alignment=QtCore.Qt.AlignLeft)
        self.change_labelx()
        self.lineEdit_xLabel.setText("x")

        # label y
        self.label_y = QtWidgets.QLabel(ui.scrollAreaWidgetContents_plotSourceImage)
        self.label_y.setObjectName("label_y")
        self.label_y.setText("Label y-axis")
        ui.gridLayout_plotSourceImage.addWidget(self.label_y, 8, 0, 1, 3,alignment=QtCore.Qt.AlignLeft)


        # line edit y label
        self.lineEdit_yLabel = QtWidgets.QLineEdit(ui.scrollAreaWidgetContents_plotSourceImage)
        self.lineEdit_yLabel.setObjectName("lineEdit_ylabel")
        self.lineEdit_yLabel.textChanged.connect(self.change_labely)
        ui.gridLayout_plotSourceImage.addWidget(self.lineEdit_yLabel,8, 1, 1, 3,alignment=QtCore.Qt.AlignLeft)
        self.change_labely()
        self.lineEdit_yLabel.setText("y")

    def change_title(self):
        self.ax.set_title(self.lineEdit_title.text())
        self.ui.canvas_plotSourceImage.draw()

    def change_labelx(self):
        if self.lineEdit_xLabel.text()=="":
            self.ax.set_xlabel("")
        else:
            try:
                self.ax.set_xlabel(r"$"+self.lineEdit_xLabel.text()+"$")
                self.ui.canvas_plotSourceImage.draw()
            except Exception as error:
                self.ui.update_outputText(error)

    def change_labely(self):
        if self.lineEdit_yLabel.text()=="":
            self.ax.set_ylabel("")
        else:
            try:
                self.ax.set_ylabel(r"$"+self.lineEdit_yLabel.text()+"$")
                self.ui.canvas_plotSourceImage.draw()
            except:
                self.ui.update_outputText("Unable to update x-label.")

