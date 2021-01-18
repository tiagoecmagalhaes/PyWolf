#-------------------------------------------------------------------------------
# Name:        Palettes
# Purpose:     PyWolf's Palettes
#
# Author:      Tiago E. C. Magalhaes
#
# Licence:     GNU GENERAL PUBLIC LICENSE Version 3
#-------------------------------------------------------------------------------


#===============================================================================
# Packages
#===============================================================================
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QLinearGradient, QColor
#_______________________________________________________________________________


#===============================================================================
# Colors
#===============================================================================
color_white = QtGui.QColor(255, 255, 255)
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Stylesheets
#===============================================================================
stylesheet = """
    QScrollBar:vertical {
        border: 1px solid #999999;
        background:white;
        width:17px;
        margin: 0px 0px 0px 0px;
    }
    QScrollBar::handle:vertical {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop: 0 rgb(90, 90, 90), stop: 0.5 rgb(102, 102, 102), stop:1 rgb(90, 90, 90));
        min-height: 10px;
    }
    QScrollBar::add-line:vertical {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));
        height: 0px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:vertical {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));
        height: 0 px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }
    ));
    """
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Size of entries
#===============================================================================
def size_entries(ui):
    return(ui.rect.width()/20)

def size_schedule(ui):
    return(ui.rect.width()/10)

def size_spinBox(ui):
    return(ui.rect.width()/35)
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# MainWindows Color palette
#===============================================================================
palette_mainwindow = QtGui.QPalette()

brush = QtGui.QBrush(color_white)
brush.setStyle(QtCore.Qt.SolidPattern)
palette_mainwindow.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)

brush = QtGui.QBrush(color_white)
brush.setStyle(QtCore.Qt.SolidPattern)
palette_mainwindow.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)

#p = QPalette()   (92, 1, 7)  (3, 31, 71)
gradient = QLinearGradient(0, 0, 0, 900)
gradient.setColorAt(0.0, QtGui.QColor(0, 0, 0))
gradient.setColorAt(0.5, QtGui.QColor(51, 23, 51))
gradient.setColorAt(1.0, QtGui.QColor(0, 0, 0))


#p.setBrush(QPalette.Window, QBrush(gradient))

brush = QtGui.QBrush(QtGui.QColor(92, 1, 7))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_mainwindow.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, gradient)

brush = QtGui.QBrush(color_white)
brush.setStyle(QtCore.Qt.SolidPattern)
palette_mainwindow.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)

brush = QtGui.QBrush(color_white)
brush.setStyle(QtCore.Qt.SolidPattern)
palette_mainwindow.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)

#brush = QtGui.QBrush(QtGui.QColor(0, 18, 54))
#brush.setStyle(QtCore.Qt.SolidPattern)
#palette_mainwindow.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)

brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_mainwindow.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)

brush = QtGui.QBrush(QtGui.QColor(0, 18, 54))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_mainwindow.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(0, 18, 54))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_mainwindow.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Message ScrollArea Color palette
#===============================================================================
palette_messageArea = QtGui.QPalette()
brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_messageArea.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(69, 69, 69))
brush = QtGui.QBrush(QtGui.QColor(3, 31, 71))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_messageArea.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_messageArea.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(69, 69, 69))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_messageArea.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)

brush = QtGui.QBrush(QtGui.QColor(69, 69, 69))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_messageArea.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(69, 69, 69))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_messageArea.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
#===============================================================================
#///////////////////////////////////////////////////////////////////////////////
#===============================================================================


#===============================================================================
# Title Labels
#===============================================================================
palette_titles = QtGui.QPalette()
brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_titles.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_titles.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_titles.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
#-------------------------------------------------------------------------------
#///////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------


#===============================================================================
# Text edit Color palette
#===============================================================================
palette_textEdit = QtGui.QPalette()

brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_textEdit.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_textEdit.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(0, 255, 0, 128))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_textEdit.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)

brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_textEdit.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_textEdit.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(0, 255, 0, 128))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_textEdit.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)

brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_textEdit.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)

brush = QtGui.QBrush(QtGui.QColor(69, 69, 69))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_textEdit.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_textEdit.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
#-------------------------------------------------------------------------------
#///////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------


#===============================================================================
# Text Browser Color palette
#===============================================================================
palette_outputText = QtGui.QPalette()

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_outputText.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)

brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_outputText.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_outputText.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_outputText.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)

brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_outputText.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_outputText.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)

brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_outputText.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)

brush = QtGui.QBrush(QtGui.QColor(69, 69, 69))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_outputText.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_outputText.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
#-------------------------------------------------------------------------------
#///////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------


#===============================================================================
# Matplot Scoll area Color palette
#===============================================================================
palette_matplotScroll = QtGui.QPalette()

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_matplotScroll.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(69, 69, 69))
brush = QtGui.QBrush(QtGui.QColor(3, 31, 71))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_matplotScroll.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_matplotScroll.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(69, 69, 69))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_matplotScroll.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)

brush = QtGui.QBrush(QtGui.QColor(69, 69, 69))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_matplotScroll.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(69, 69, 69))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_matplotScroll.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
#-------------------------------------------------------------------------------
#///////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------


#===============================================================================
# Tab Widget_plots Color palette
#===============================================================================
palette_TabPlots = QtGui.QPalette()

brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_TabPlots.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)

brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_TabPlots.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)

brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_TabPlots.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_TabPlots.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
#-------------------------------------------------------------------------------
#///////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------


#===============================================================================
# Scroll Area plotSource Color palette
#===============================================================================
palette_scrollPlotSource = QtGui.QPalette()

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_scrollPlotSource.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_scrollPlotSource.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_scrollPlotSource.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 127))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_scrollPlotSource.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 127))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_scrollPlotSource.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 127))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_scrollPlotSource.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
#-------------------------------------------------------------------------------
#///////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------


#=======================================================================
# Scroll Area plot Propagation Color palette
#=======================================================================
palette_scrollPlotProp = QtGui.QPalette()

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_scrollPlotProp.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 127))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_scrollPlotProp.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_scrollPlotProp.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 127))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_scrollPlotProp.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 127))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_scrollPlotProp.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 127))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_scrollPlotProp.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
#-------------------------------------------------------------------------------
#///////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------


#=======================================================================
# GroupBox project. Section Parameters Color palette
#=======================================================================
palette_groupBoxProject = QtGui.QPalette()

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_groupBoxProject.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)

#-------------------------------------------------------------------------------
#///////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------


#=======================================================================
# Scroll Area Section Parameters Color palette
#=======================================================================
palette_parSection = QtGui.QPalette()

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_parSection.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
palette_parSection.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)

#brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush = QtGui.QBrush(QtGui.QColor(3, 31, 71))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_parSection.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_parSection.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(69, 69, 69))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_parSection.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)

brush = QtGui.QBrush(QtGui.QColor(69, 69, 69))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_parSection.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(69, 69, 69))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_parSection.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
#-------------------------------------------------------------------------------
#///////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------

#===============================================================================
# PushButton_start Color palette
#===============================================================================
palette_buttonStart = QtGui.QPalette()

brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_buttonStart.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)

brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_buttonStart.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)

brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_buttonStart.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
#-------------------------------------------------------------------------------
#///////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------


#===============================================================================
# TabWidget Propagation System Color palette
#===============================================================================
palette_tabPropSys = QtGui.QPalette()


brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_tabPropSys.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)

brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_tabPropSys.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)

brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_tabPropSys.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)

#-------------------------------------------------------------------------------
#///////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------


#===============================================================================
# Scroll Area Plane 1 Color palette
#===============================================================================
palette_scrollAreaPlane1 = QtGui.QPalette()

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_scrollAreaPlane1.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(3, 31, 71))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_scrollAreaPlane1.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_scrollAreaPlane1.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_scrollAreaPlane1.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)

brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_scrollAreaPlane1.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_scrollAreaPlane1.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
#-------------------------------------------------------------------------------
#///////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------


#===============================================================================
# Tab Plane 1 Color palette
#===============================================================================
palette_tabPlane = QtGui.QPalette()

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_tabPlane.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_tabPlane.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)

brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_tabPlane.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_tabPlane.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)

brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_tabPlane.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)

brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
brush.setStyle(QtCore.Qt.SolidPattern)
palette_tabPlane.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
#-------------------------------------------------------------------------------
#///////////////////////////////////////////////////////////////////////////////
#-------------------------------------------------------------------------------
