#! /usr/bin/env python
# -*- coding: utf-8 -*-

# import 
import sys
import numpy as np

# pyqt5
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QHBoxLayout, QPushButton, QMainWindow
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


# matplotlib
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
from mpl_toolkits.mplot3d import Axes3D 

# OS path
from os import listdir
from os.path import isfile, join



# class for images
class ImageDataClass(object):
    def __init__(self):
        super(ImageDataClass, self).__init__()
        self.image = None
       
    # load  image to array
    def loadFromFile (self, fdir):
        self.image = mpimg.imread(fdir)
        
    # get image 
    def getImage(self):
        return self.image
    
   
        

# matplotlib widgets
class matPlotwidget(QWidget):
    def __init__(self):
        super(matPlotwidget, self).__init__()
        
        self.ImageData = None
        self.inx = 0        

     
        # a figure instance to plot on
        self.figure = Figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
        # Just some button connected to `plot` method
        self.button = QtWidgets.QPushButton('Plot')
        self.button.clicked.connect(self.plot)
        # add slider
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setMinimum(0.0)
        self.slider.setMaximum(10.0)
        self.slider.setValue(0.0)
        self.slider.valueChanged.connect(self.sliderValueChange)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.slider)
        layout.addWidget(self.button)
        self.setLayout(layout)
        
    def plot(self):

        # create an axis
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        # plot image3D
        if self.ImageData  is not None:
            self.ax.clear()
            # self.im = self.ax.imshow(self.ImageData[self.inx,:,:], cmap=plt.cm.gray)
            self.im = self.ax.imshow(self.ImageData, cmap=plt.cm.gray)


        # refresh canvas
        self.canvas.draw()
        
    def setImage(self, data):
        self.ImageData  = data
        sizes = self.ImageData.shape
        self.slider.setMaximum(sizes[0]-1)
        
        
    def sliderValueChange(self):
        self.inx = int(self.slider.value())
        print ("slider value changes (matplotlib)", self.inx)
 

        
    
# slider panel
class controlWidget(QWidget):
    def __init__(self):
        super(controlWidget, self).__init__()       
        self.init()
    
    def init(self):
    
        # ComboBox
        self.cb = QtWidgets.QComboBox()       
    
        # slider        
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setMinimum(0.0)
        self.slider.setMaximum(10.0)
        self.slider.setValue(0.0)
        
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.cb)
        vbox.addWidget(self.slider)
        self.setLayout(vbox)
        
    def getSlider(self):
        return self.slider
    
    # get combo box reference    
    def getCB(self):
        return self.cb
    

# main application GUI
class MainWindow(QMainWindow):
    
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads)      
       
        # Image data
        self.ImageDataClass = ImageDataClass()        
        # initialize GUI 
        self.initUIwindow()
    
        
    # GUI function to define all widgets    
    def initUIwindow(self):     
                        
        # add as a CONTROL panel dock widget
        self.controlWid = controlWidget()       
        self.controlPanel = QtWidgets.QDockWidget("Control", self)
        self.controlPanel.setObjectName("Control")
        self.controlPanel.setWidget( self.controlWid )
        self.controlPanel.setFloating(False)        
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.controlPanel) 
        
        
        # add as a MATPLOTLIB panel dock widget
        self.matPlotlWid = matPlotwidget()      
        self.matPlotPanel = QtWidgets.QDockWidget("IMAGE", self)
        self.matPlotPanel.setObjectName("Image")
        self.matPlotPanel.setWidget( self.matPlotlWid )
        self.matPlotPanel.setFloating(False)        
        self.setCentralWidget(self.matPlotPanel)
        # self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.matPlotPanel)  
        
        
        # action: exit
        exitAction = QtWidgets.QAction( QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtWidgets.qApp.quit)        
        # action: open file (Image files)
        openImageAction = QtWidgets.QAction(QtGui.QIcon('dicom.png'), '&open ultrasound images', self)
        openImageAction.setStatusTip('open ultrasound dir')
        openImageAction.triggered.connect(self.LoadImageFileDialog)       

        
        # menu bar
        menubar = self.menuBar()
        fileMemu = menubar.addMenu('&File')
        fileMemu.addAction(exitAction)
        fileMemu.addAction(openImageAction)
        
        # tool bar
        self.toolbar = self.addToolBar('&ToolBar1')     
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(openImageAction)

        
        # status bar
        self.statusBar()        
        self.resize(1200,1000)
        self.center()
        self.setWindowTitle('GUI sample App v1.0')             
        self.show()
        
    # close Event reimplement
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
        
        if reply ==QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
                    
    # set the window to center
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
   
    # load DICOM file directory 
    def LoadImageFileDialog(self):
        # get folder dir
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Select Folder", "/home/kenan/Documents/gitProject/pyMedImage/DICOM_data/")     
        fileName = str(files[0]) 
        print ("open file name: ", fileName)
        self.ImageDataClass.loadFromFile(fileName)    
        
        self.matPlotlWid.setImage(self.ImageDataClass.getImage())
        self.matPlotlWid.plot()
        
    # control panel slider
    def sliderValueChange(self):
        num = self.controlWid.getSlider().value()
        # conver to range (-1, 1)
        num = (num-5.0)/5.0 
        print ("slider value change to : ", num)     



# main function
def main ():    
    app = QApplication(sys.argv)
    window = MainWindow()   
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()













