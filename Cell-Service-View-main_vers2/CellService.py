import sys
from copy import deepcopy
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QAction, QFileDialog, QMenuBar, QMainWindow, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QImage, QFont

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
        self.setWindowTitle("CellService")
        self.centralwidget = QWidget()
        self.centralwidget.setStyleSheet("background-color: qradialgradient(spread:reflect, cx:0.5, cy:0.494318, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(135, 200, 255, 255), stop:1 rgba(255, 255, 255, 255));\n")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.principal_layout = QGridLayout(self.gridLayoutWidget)
        self.principal_layout.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutWidget.setStyleSheet("background-color: white;\n" "border-radius: 10px;\n")
        self.setCentralWidget(self.centralwidget)
        
        self.RGB_QLabel = QLabel(self.gridLayoutWidget)
        self.RGB_QLabel.setTabletTracking(True)
        self.RGB_QLabel.setStyleSheet("background-color: rgb(255, 255, 255);\n" "    border-radius: 10px;\n" "border: 3px solid black")
        self.RGB_QLabel.setScaledContents(True)
        self.principal_layout.addWidget(self.RGB_QLabel, 0, 0, 1, 1)
        
        self.Red_QLabel = QLabel(self.gridLayoutWidget)
        self.Red_QLabel.setTabletTracking(True)
        self.Red_QLabel.setStyleSheet("background-color: rgb(255, 255, 255);\n" "border-radius: 10px;\n" "border: 3px solid red")
        self.Red_QLabel.setScaledContents(True)
        self.principal_layout.addWidget(self.Red_QLabel, 0, 1, 1, 1)
        
        self.Green_QLabel = QLabel(self.gridLayoutWidget)
        self.Green_QLabel.setStyleSheet("background-color: rgb(255, 255, 255);\n" "border-radius: 10px;\n" "border: 3px solid green")
        self.Green_QLabel.setScaledContents(True)
        self.principal_layout.addWidget(self.Green_QLabel, 1, 0, 1, 1)
        
        self.Blue_QLabel = QLabel(self.gridLayoutWidget)
        self.Blue_QLabel.setStyleSheet("background-color: rgb(255, 255, 255);\n" "border-radius: 10px;\n" "border: 3px solid blue")
        self.Blue_QLabel.setScaledContents(True)
        self.principal_layout.addWidget(self.Blue_QLabel, 1, 1, 1, 1)
        
        self.Analysis = QPushButton(self.centralwidget)
        self.Analysis.setText("Analysis")
        self.Analysis.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "border-radius: 10px;\n"
            "font: bold 14px;\n"
            "padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.Analysis.clicked.connect(self.analysis)
        
        self.Processing = QPushButton(self.centralwidget)
        self.Processing.setText("Processing")
        self.Processing.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.Processing.clicked.connect(self.processing)
        
        self.menuBar()
        self.maximize_window()
        self.show()
    
    def menuBar(self):
        self.menubar = QMenuBar()
        self.menubar.setGeometry(QRect(0, 0, 900, 37))
        self.menubar.setStyleSheet("background-color: qradialgradient(spread:reflect, cx:0, cy:0.494318, radius:1.5, fx:0.5, fy:0.5, stop:0 rgba(135, 200, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "selection-color: rgb(128, 183, 255);\n"
            "color: white;")
        self.menubar.setObjectName("menubar")
        self.menuFile = self.menubar.addMenu("File")
        font = QFont()
        font.setFamily("Varela")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.menuFile.setFont(font)
        self.menuFile.setAutoFillBackground(False)
        self.menuFile.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: blue;")
        self.menuFile.setToolTipsVisible(False)
        self.menuFile.setTitle("Add Image")
        self.setMenuBar(self.menubar)
        
        openRGBAction = QAction(QIcon('open.png'), '&Open RGB image', self)
        openRGBAction.setShortcut('Ctrl+O')
        openRGBAction.setStatusTip('Open a new RGB image')
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        openRGBAction.setFont(font)
        openRGBAction.triggered.connect(self.openRGBCall)
        self.menuFile.addAction(openRGBAction)
        
        openSingleChannelsAction = QAction(QIcon('open.png'), '&Open single channels image', self)
        openSingleChannelsAction.setStatusTip('Open a new RGB image by selecting different channels')
        openSingleChannelsAction.setFont(font)
        openSingleChannelsAction.triggered.connect(self.openSingleChannelsCall)
        self.menuFile.addAction(openSingleChannelsAction)
        
    
    def processing(self):
        self.intensityAnalysis = CellService_processing.CellServiceBinaryProcessing(self)
        self.intensityAnalysis.show()
        
    def analysis(self):
        self.analysis = Analisys_cellService.Ui_Analisys_cellService(self)
        self.analysis.show()
    
    def maximize_window(self):
        screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(int(screen.height()*1.2), int(screen.height()*0.9))
        y=int(screen.height()*0.75)
        x=int(screen.height()*1)
        position=int(screen.height()*0.08)
        self.gridLayoutWidget.setGeometry(QRect(position, position, x, y))
        self.gridLayoutWidget.setFixedSize(x,y)
        self.Analysis.setGeometry(QRect(int(screen.height()*0.65), 20, 271, 41))
        self.Processing.setGeometry(QRect(int(screen.height()*0.20), 20, 231, 41))
        
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

