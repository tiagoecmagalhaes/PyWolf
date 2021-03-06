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
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from numpy import zeros




class Canvas_sourceImage:
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



def plot_sourceImage(ui,parent,W_matrix,N):

    # SI = Source Image

    ui.frame_sourceImage = parent

    # Create the mpl Figure and FigCanvas objects.
    # 5x4 inches, 100 dots-per-inch
    ui.dpi_SI = 100
    ui.fig_SI = Figure((5.0, 4.0), dpi=ui.dpi_SI)
    ui.canvas_SI = FigureCanvas(ui.fig_SI)
    ui.canvas_SI.setParent(ui.frame_sourceImage)

    # Since we have only one plot, we can use add_axes
    # instead of add_subplot, but then the subplot
    # configuration tool in the navigation toolbar wouldn't
    # work.
    #
    ui.axes_SI = ui.fig_SI.add_subplot(111)

    # creating image source
    image_source = zeros((N,N))
    for i in range(0,N):
        for j in range(0,N):
            image_source[i,j]=W_matrix[i,j,i,j].real

    # PLOT
    im = ui.axes_SI.pcolormesh(image_source)
    cbar = ui.fig_SI.colorbar(im)

    # x,y Labels
    ui.axes_SI.set_xlabel("x (m)")
    ui.axes_SI.set_ylabel("y (m)")

    # Bind the 'pick' event for clicking on one of the bars
    ui.canvas_SI.mpl_connect('pick_event', ui.on_pick)

    # Create the navigation toolbar, tied to the canvas
    ui.mpl_toolbar_SI = NavigationToolbar(ui.canvas_SI, ui.frame_sourceImage)


    # Other GUI controls
    #

    ui.textbox = QLineEdit()
    ui.textbox.setMinimumWidth(200)
    ui.textbox.editingFinished.connect(ui.draw_sourceImage)

    ui.draw_button = QPushButton("&Draw")
    ui.draw_button.clicked.connect(ui.draw_sourceImage)

    ui.grid_cb = QCheckBox("Show &Grid")
    ui.grid_cb.setChecked(False)
    ui.grid_cb.stateChanged.connect(ui.draw_sourceImage)

    slider_label = QLabel('Bar width (%):')
    ui.slider = QSlider(Qt.Horizontal)
    ui.slider.setRange(1, 100)
    ui.slider.setValue(20)
    ui.slider.setTracking(True)
    ui.slider.setTickPosition(QSlider.TicksBothSides)
    ui.slider.valueChanged.connect(ui.draw_sourceImage)








    #
    # Layout with box sizers
    #

    hbox = QHBoxLayout()

    for w in [  ui.textbox, ui.draw_button, ui.grid_cb,
                slider_label, ui.slider]:
        hbox.addWidget(w)
        hbox.setAlignment(w, Qt.AlignVCenter)

    vbox = QVBoxLayout()
    vbox.addWidget(ui.canvas_SI)
    vbox.addWidget(ui.mpl_toolbar_SI)
    vbox.addLayout(hbox)


    ui.frame_sourceImage.setLayout(vbox)



    ui.setCentralWidget(ui.frame_sourceImage)



