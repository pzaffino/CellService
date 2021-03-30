#!/usr/bin/env python

import sys
from copy import deepcopy
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QAction, QFileDialog, QMenuBar, QMainWindow, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QImage, qRgb

import CellService_analysis
import CellService_processing
import Analisys_cellService

import numpy as np
import skimage.io

class CellService(QMainWindow):

    def __init__(self):
        super(CellService, self).__init__()

        self.red_image = None
        self.green_image = None
        self.blue_image = None

        self.red_mask = None
        self.green_mask = None
        self.blue_mask = None

        self.initUI()

    def initUI(self):

        # Create widgent and layout
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        grid = QGridLayout()
        self.centralWidget.setLayout(grid)

        # Define title, menu and other init stuff
        self.move(20, 20)
        self.setWindowTitle("CellService")
        self.create_menu()

        init_size = 128

        # RGB
        self.RGB_QLabel = QLabel(self)
        self.RGB_QLabel.setStyleSheet("border: 3px solid black;")
        self.RGB_QLabel.setScaledContents(True)
        grid.addWidget(self.RGB_QLabel, 0,0)
        self.RGB_QLabel.resize(init_size, init_size)

        # RED
        self.Red_QLabel = QLabel(self)
        self.Red_QLabel.setStyleSheet("border: 3px solid red;")
        self.Red_QLabel.setScaledContents(True)
        grid.addWidget(self.Red_QLabel, 0,1)
        self.Red_QLabel.resize(init_size, init_size)

        # GREEN
        self.Green_QLabel = QLabel(self)
        self.Green_QLabel.setStyleSheet("border: 3px solid green;")
        self.Green_QLabel.setScaledContents(True)
        grid.addWidget(self.Green_QLabel, 1,0)
        self.Green_QLabel.resize(init_size, init_size)

        # BLUE
        self.Blue_QLabel = QLabel(self)
        self.Blue_QLabel.setStyleSheet("border: 3px solid blue;")
        self.Blue_QLabel.setScaledContents(True)
        grid.addWidget(self.Blue_QLabel, 1,1)
        self.Blue_QLabel.resize(init_size, init_size)

        # Show the window
        self.maximize_window()
        self.show()

    def maximize_window(self):
        screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(int(screen.height()*1.2), int(screen.height()*0.9))

    def create_menu(self):
        mainMenu = self.menuBar()

        # File menu
        fileMenu = mainMenu.addMenu("File")

        # Open (single) RGB image
        openRGBAction = QAction(QIcon('open.png'), '&Open RGB image', self)
        openRGBAction.setShortcut('Ctrl+O')
        openRGBAction.setStatusTip('Open a new RGB image')
        openRGBAction.triggered.connect(self.openRGBCall)
        fileMenu.addAction(openRGBAction)

        # Open single channels RGB image
        openSingleChannelsAction = QAction(QIcon('open.png'), '&Open single channels image', self)
        openSingleChannelsAction.setStatusTip('Open a new RGB image by selecting different channels')
        openSingleChannelsAction.triggered.connect(self.openSingleChannelsCall)
        fileMenu.addAction(openSingleChannelsAction)

        # Binarization processing
        self.third_title = mainMenu.addMenu("Image Processing")
        # add first choice 
        self.firstChoiceThirdMenu = QAction("Image binarization")
        self.firstChoiceThirdMenu.triggered.connect(self.window2)
        self.third_title.addAction(self.firstChoiceThirdMenu)

        # Analysis menu
        analysisMenu = mainMenu.addMenu("Analysis")
        #self.intensityAnalysis = CellService_analysis.CellServiceIntensityAnalysis(self)

        # Intensity analysis
        intensityAnalysisAction = QAction('&Similarity analysis', self)
        intensityAnalysisAction.setStatusTip("Execute intensity analysis")
        intensityAnalysisAction.triggered.connect(self.analisysWindow)
        analysisMenu.addAction(intensityAnalysisAction)
    
    def window2(self):
        self.intensityAnalysis = CellService_processing.CellServiceBinaryProcessing(self)
        self.intensityAnalysis.show()
        
    def analisysWindow(self):
        self.analysis = Analisys_cellService.Ui_Analisys_cellService(self)
        self.analysis.show()
        
    def set_image(self, np_array, qt_label, channel, mask=False):

        # If the image is not set (None) do nothing
        if np_array is None:
           return

        if channel == "rgb":
            image = np_array
        elif channel == "red":
            image = np.zeros((np_array.shape[0], np_array.shape[1], 3), dtype=np.uint8)
            image[:,:,0] = np_array
        elif channel == "green":
            image = np.zeros((np_array.shape[0], np_array.shape[1], 3), dtype=np.uint8)
            image[:,:,1] = np_array
        elif channel == "blue":
            image = np.zeros((np_array.shape[0], np_array.shape[1], 3), dtype=np.uint8)
            image[:,:,2] = np_array

        # if it is a binary mask, scale it to 0-255
        if mask:
            image = image*255

        self.qt_image = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888)
        qt_pixmap = QPixmap.fromImage(self.qt_image)
        qt_label.setPixmap(qt_pixmap)
        self.maximize_window()

    def set_all_images(self):
        self.set_image(self.rgb_image, self.RGB_QLabel, "rgb", mask=False)
        self.set_image(self.red_image, self.Red_QLabel, "red", mask=False)
        self.set_image(self.green_image, self.Green_QLabel, "green", mask=False)
        self.set_image(self.blue_image, self.Blue_QLabel, "blue", mask=False)

    def openRGBCall(self):
        # see https://gist.github.com/smex/5287589
        file_name = QFileDialog.getOpenFileName(self, 'Open RGB Image')
        if file_name:
            self.rgb_image = skimage.io.imread(file_name[0]).astype(np.uint8)
            self.red_image = deepcopy(self.rgb_image[:,:,0])
            self.green_image = deepcopy(self.rgb_image[:,:,1])
            self.blue_image = deepcopy(self.rgb_image[:,:,2])

            self.set_all_images()

    def openSingleChannelsCall(self):
        # RED
        red_channel_file_name = QFileDialog.getOpenFileName(self, 'Open red channel')
        if red_channel_file_name[0]:
            self.red_image = skimage.io.imread(red_channel_file_name[0])[:,:,0].astype(np.uint8)

        # GREEN
        green_channel_file_name = QFileDialog.getOpenFileName(self, 'Open green channel')
        if green_channel_file_name[0]:
            self.green_image = skimage.io.imread(green_channel_file_name[0])[:,:,1].astype(np.uint8)

        # BLUE
        blue_channel_file_name = QFileDialog.getOpenFileName(self, 'Open blue channel')
        if blue_channel_file_name[0]:
            self.blue_image = skimage.io.imread(blue_channel_file_name[0])[:,:,2].astype(np.uint8)

        # Manage if the user do not open three channels
        # Figure out image shape (even if a single image has been open)
        if self.red_image is not None:
            matrix_shape = self.red_image.shape
        elif self.green_image is not None:
            matrix_shape = self.green_image.shape
        elif self.blue_image is not None:
            matrix_shape = self.blue_image.shape
        else:
            self.error_message("Any image opened!")
            return

        # if a channel was not open create zeros matrix
        if self.red_image is None:
            self.red_image = np.zeros(matrix_shape, dtype=np.uint8)
        if self.green_image is None:
            self.green_image = np.zeros(matrix_shape, dtype=np.uint8)
        if self.blue_image is None:
            self.blue_image = np.zeros(matrix_shape, dtype=np.uint8)

        # Check image shape (must be equal)
        if self.red_image.shape != self.green_image.shape or self.red_image.shape != self.blue_image.shape or self.green_image.shape != self.blue_image.shape:
            self.error_message("The images have not the same shape!")
            self.red_image = None
            self.green_image = None
            self.blue_image = None
            return

        # RGB
        self.rgb_image = np.dstack((self.red_image, self.green_image, self.blue_image)).astype(np.uint8)

        # Set images
        self.set_all_images()

    def error_message(self, text_error):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(text_error)
        msg.setWindowTitle("Error")
        msg.exec_()

if __name__ == '__main__':
     app = QApplication(sys.argv)
     ex = CellService()
     sys.exit(app.exec_())

