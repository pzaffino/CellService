#!/usr/bin/env python

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QAction, QFileDialog, QMenuBar, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap, QImage, qRgb

import numpy as np
import skimage.io


class CellService(QMainWindow):

    def __init__(self):
        super(CellService, self).__init__()
        self.initUI()

    def initUI(self):

        # Create widgent and layout
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        grid = QGridLayout()
        self.centralWidget.setLayout(grid)

        # Define title, menu and other init stuff
        self.move(300, 150)
        self.setWindowTitle("CellService")
        self.create_menu()

        init_size = 512

        # RGB
        self.RGB_QLabel = QLabel(self)
        self.RGB_QLabel.setStyleSheet("border: 2px solid black;")
        self.RGB_QLabel.setScaledContents(True)
        grid.addWidget(self.RGB_QLabel, 0,0)
        self.RGB_QLabel.resize(init_size, init_size)

        # RED
        self.Red_QLabel = QLabel(self)
        self.Red_QLabel.setStyleSheet("border: 2px solid red;")
        self.Red_QLabel.setScaledContents(True)
        grid.addWidget(self.Red_QLabel, 0,1)
        self.Red_QLabel.resize(init_size, init_size)

        # GREEN
        self.Green_QLabel = QLabel(self)
        self.Green_QLabel.setStyleSheet("border: 2px solid green;")
        self.Green_QLabel.setScaledContents(True)
        grid.addWidget(self.Green_QLabel, 1,0)
        self.Green_QLabel.resize(init_size, init_size)

        # BLUE
        self.Blue_QLabel = QLabel(self)
        self.Blue_QLabel.setStyleSheet("border: 2px solid blue;")
        self.Blue_QLabel.setScaledContents(True)
        grid.addWidget(self.Blue_QLabel, 1,1)
        self.Blue_QLabel.resize(init_size, init_size)

        # Show the window
        self.resize(1024,1024)
        self.show()

    def create_menu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")

        openAction = QAction(QIcon('open.png'), '&Open RGB', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a new RGB image')
        openAction.triggered.connect(self.openCall)
        fileMenu.addAction(openAction)

    def set_image(self, np_array, qt_label, channel):

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

        qt_image = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888)
        qt_label.setPixmap(QPixmap.fromImage(qt_image))

    def openCall(self):
        # see https://gist.github.com/smex/5287589
        print('Open RGB Image')
        file_name = QFileDialog.getOpenFileName(self, 'Open RGB Image')


        if file_name:
            self.RGB_image = skimage.io.imread(file_name[0]).astype(np.uint8)
            self.set_image(self.RGB_image, self.RGB_QLabel, "rgb")
            self.set_image(self.RGB_image[:,:,0], self.Red_QLabel, "red")
            self.set_image(self.RGB_image[:,:,1], self.Green_QLabel, "green")
            self.set_image(self.RGB_image[:,:,2], self.Blue_QLabel, "blue")


if __name__ == '__main__':
     app = QApplication(sys.argv)
     ex = CellService()
     sys.exit(app.exec_())

