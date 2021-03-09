#!/usr/bin/env python

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QAction, QFileDialog, QMenuBar, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap

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

        pixmap = QPixmap('/home/p4ol0/Pictures/logo_vv.png')

        # RGB
        self.QLabelRGB = QLabel(self)
        self.QLabelRGB.setStyleSheet("border: 2px solid black;")
        self.QLabelRGB.setScaledContents(True)
        grid.addWidget(self.QLabelRGB, 0,0)
        self.QLabelRGB.setPixmap(pixmap)

        # RED
        self.QLabelR = QLabel(self)
        self.QLabelR.setStyleSheet("border: 2px solid red;")
        self.QLabelR.setScaledContents(True)
        grid.addWidget(self.QLabelR, 0,1)
        self.QLabelR.setPixmap(pixmap)

        # GREEN
        self.QLabelG = QLabel(self)
        self.QLabelG.setStyleSheet("border: 2px solid green;")
        self.QLabelG.setScaledContents(True)
        grid.addWidget(self.QLabelG, 1,0)
        self.QLabelG.setPixmap(pixmap)

        # BLUE
        self.QLabelB = QLabel(self)
        self.QLabelB.setStyleSheet("border: 2px solid blue;")
        self.QLabelB.setScaledContents(True)
        grid.addWidget(self.QLabelB, 1,1)
        self.QLabelB.setPixmap(pixmap)

        # Show the window
        self.show()

    def create_menu(self):
        #mainMenu = QMenuBar(self)
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")

        openAction = QAction(QIcon('open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a new image')
        openAction.triggered.connect(self.openCall)
        fileMenu.addAction(openAction)

    def openCall(self):
        # see https://gist.github.com/smex/5287589
        print('Open RGB Image')
        file_name = QFileDialog.getOpenFileName(self, 'Open RGB Image')

        """
        if file_name:
            self.RGB_image = skimage.io.imread(file_name[0]).astype(np.uint8)
            self.set_image(self.RGB_image, self.RGB_QLabel, "rgb")
            self.set_image(self.RGB_image[:,:,0], self.Red_QLabel, "red")
            self.set_image(self.RGB_image[:,:,1], self.Green_QLabel, "green")
            self.set_image(self.RGB_image[:,:,2], self.Blue_QLabel, "blue")
        """

if __name__ == '__main__':
     app = QApplication(sys.argv)
     ex = CellService()
     sys.exit(app.exec_())

