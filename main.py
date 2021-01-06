# This Python file uses the following encoding: utf-8
import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog
from PyQt5.QtCore import QFile
from PyQt5.QtGui import QIcon, QImage, QPixmap, qRgb
import PyQt5.uic

import numpy as np
import skimage.io

class CellService(QMainWindow):
    def __init__(self):
        super(CellService, self).__init__()
        self.load_ui()
        self.create_menu()

    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader = PyQt5.uic.loadUi(ui_file, self)
        ui_file.close()

    def create_menu(self):
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

        if file_name:
            print(file_name[0])
            self.RGB_image = skimage.io.imread(file_name[0]).astype(np.uint8)

            RGB_QImage = QImage(self.RGB_image.data, self.RGB_image.shape[1], self.RGB_image.shape[0], self.RGB_image.strides[0], QImage.Format_RGB888)
            self.RGB_QLabel.setPixmap(QPixmap.fromImage(RGB_QImage))

if __name__ == "__main__":
    app = QApplication([])
    widget = CellService()
    widget.show()
    sys.exit(app.exec_())
