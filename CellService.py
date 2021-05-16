import sys
from copy import deepcopy
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QKeySequence
from PyQt5 import QtWidgets
import CellService_processing
import Analisys_cellService
from PyQt5 import QtCore, QtGui
import numpy as np
import skimage.io

class CellService(QMainWindow):

    def __init__(self):
        super(CellService, self).__init__()
        
        self.setupUi()
        
        self.red_image = None
        self.green_image = None
        self.blue_image = None
        self.rgb_image = None

        self.red_mask = None
        self.green_mask = None
        self.blue_mask = None
        
        self.maximize_window()
    
    def setupUi(self):
        self.setWindowTitle("CellService")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setStyleSheet("background-color: rgb(244, 244, 244);")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(257, 30, 951, 851))
        self.principal_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.principal_layout.setContentsMargins(0, 0, 0, 0)
        
        self.GREEN_QLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.GREEN_QLabel.setStyleSheet("border: 2px solid green")
        self.GREEN_QLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.GREEN_QLabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.GREEN_QLabel.setLineWidth(2)
        self.GREEN_QLabel.setScaledContents(True)
        self.principal_layout.addWidget(self.GREEN_QLabel, 1, 0, 1, 1)
        
        self.RGB_QLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.RGB_QLabel.setStyleSheet("border: 2px solid black")
        self.RGB_QLabel.setFixedSize(465,415)
        self.RGB_QLabel.setScaledContents(True)
        self.principal_layout.addWidget(self.RGB_QLabel, 0, 0, 1, 1)
        
        self.BLUE_QLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.BLUE_QLabel.setStyleSheet("border: 2px solid blue")
        self.BLUE_QLabel.setFixedSize(465,415)
        self.BLUE_QLabel.setScaledContents(True)
        self.principal_layout.addWidget(self.BLUE_QLabel, 1, 1, 1, 1)
        
        self.RED_QLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.RED_QLabel.setTabletTracking(True)
        self.RED_QLabel.setStyleSheet("border: 2px solid red")
        self.RED_QLabel.setFrameShape(QtWidgets.QFrame.Panel)
        self.RED_QLabel.setFixedSize(465,415)
        self.RED_QLabel.setLineWidth(2)
        self.RED_QLabel.setScaledContents(True)
        self.principal_layout.addWidget(self.RED_QLabel, 0, 1, 1, 1)
        
        self.option_widget = QtWidgets.QWidget(self.centralwidget)
        self.option_widget.setGeometry(QtCore.QRect(28, 30, 180, 551))
        self.option_widget.setStyleSheet("background-color: rgb(255, 255, 255);\n" "border-radius: 40px;")
        self.option_widget.setGraphicsEffect(self.applyShadow())
        
        self.open_file_button = QtWidgets.QPushButton(self.option_widget)
        self.open_file_button.setGeometry(QtCore.QRect(60, 20, 51, 51))
        self.open_file_button.setMouseTracking(True)
        self.open_file_button.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.open_file_button.setToolTipDuration(-1)
        self.open_file_button.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 15px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}\n"
            "")
        self.open_file_button.setGraphicsEffect(self.applyShadow())
        icon = QtGui.QIcon("Icon/file_icon.png")
        self.open_file_button.setIcon(icon)
        self.open_file_button.setIconSize(QtCore.QSize(60, 55))
        self.open_file_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Open RGB Image (Ctrl+O)</span></p></body></html>")
        self.open_file_button.setStatusTip("Open RGB Image (Ctrl+O)")
        self.open_file_button.clicked.connect(self.openRGBCall)
        self.ctrl_open = QtWidgets.QShortcut(QKeySequence('Ctrl+O'), self)
        self.ctrl_open.activated.connect(self.openRGBCall)
        
        self.openSingle_button = QtWidgets.QPushButton(self.option_widget)
        self.openSingle_button.setGeometry(QtCore.QRect(60, 130, 51, 51))
        self.openSingle_button.setMouseTracking(True)
        self.openSingle_button.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.openSingle_button.setToolTipDuration(-1)
        self.openSingle_button.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 15px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}\n"
            "")
        self.openSingle_button.setGraphicsEffect(self.applyShadow())
        icon1 = QtGui.QIcon("Icon/file icon rgb.png")
        self.openSingle_button.setIcon(icon1)
        self.openSingle_button.setIconSize(QtCore.QSize(60, 55))
        self.openSingle_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Open singles channels (Ctrl+Shift+O)</span></p></body></html>")
        self.openSingle_button.setStatusTip("Open singles channels (Ctrl+Shift+O)")
        self.openSingle_button.clicked.connect(self.openSingleChannelsCall)
        self.ctrl_openSingle = QtWidgets.QShortcut(QKeySequence('Ctrl+Shift+O'), self)
        self.ctrl_openSingle.activated.connect(self.openSingleChannelsCall)
        
        self.processing_button = QtWidgets.QPushButton(self.option_widget)
        self.processing_button.setGeometry(QtCore.QRect(60, 240, 51, 51))
        self.processing_button.setMouseTracking(True)
        self.processing_button.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.processing_button.setToolTipDuration(-1)
        self.processing_button.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 15px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}\n"
            "")
        self.processing_button.setGraphicsEffect(self.applyShadow())
        icon3 = QtGui.QIcon("Icon/processing.png")
        self.processing_button.setIcon(icon3)
        self.processing_button.setIconSize(QtCore.QSize(60, 50))
        self.processing_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Open processing window</span></p></body></html>")
        self.processing_button.setStatusTip("Open processing window")
        self.processing_button.clicked.connect(self.processingWindow)
        
        self.analisys_button = QtWidgets.QPushButton(self.option_widget)
        self.analisys_button.setGeometry(QtCore.QRect(60, 350, 51, 51))
        self.analisys_button.setMouseTracking(True)
        self.analisys_button.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.analisys_button.setToolTipDuration(-1)
        self.analisys_button.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 15px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}\n"
            "")
        self.analisys_button.setGraphicsEffect(self.applyShadow())
        icon2 = QtGui.QIcon("Icon/analizer.png")
        self.analisys_button.setIcon(icon2)
        self.analisys_button.setIconSize(QtCore.QSize(60, 55))
        self.analisys_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Open analisys window</span></p></body></html>")
        self.analisys_button.setStatusTip("Open analisys window")
        self.analisys_button.clicked.connect(self.analisysWindow)
        
        self.help_button = QtWidgets.QPushButton(self.option_widget)
        self.help_button.setGeometry(QtCore.QRect(60, 450, 51, 51))
        self.help_button.setMouseTracking(True)
        self.help_button.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.help_button.setToolTipDuration(-1)
        self.help_button.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 15px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}\n"
            "")
        self.help_button.setGraphicsEffect(self.applyShadow())
        icon4 = QtGui.QIcon("Icon/help.png")
        self.help_button.setIcon(icon4)
        self.help_button.setIconSize(QtCore.QSize(60, 55))
        self.help_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Help page</span></p></body></html>")
        self.help_button.setStatusTip("Help page")
        self.help_button.clicked.connect(self.help_message)
        
        self.open_title = QtWidgets.QLineEdit(self.option_widget)
        self.open_title.setGeometry(QtCore.QRect(10, 80, 141, 20))
        self.open_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(23, 23, 23);")
        self.open_title.setAlignment(QtCore.Qt.AlignCenter)
        self.open_title.setReadOnly(True)
        self.open_title.setText("Open RGB image")
        
        self.openSingle_title = QtWidgets.QLineEdit(self.option_widget)
        self.openSingle_title.setGeometry(QtCore.QRect(10, 190, 161, 16))
        self.openSingle_title.setStyleSheet("font: 7pt \"Arial\";\n" "color: rgb(0, 0, 0);")
        self.openSingle_title.setAlignment(QtCore.Qt.AlignCenter)
        self.openSingle_title.setReadOnly(True)
        self.openSingle_title.setText("Open single channels image")
        
        self.analisys_title = QtWidgets.QLineEdit(self.option_widget)
        self.analisys_title.setGeometry(QtCore.QRect(20, 410, 131, 16))
        self.analisys_title.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.analisys_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(0, 0, 0);")
        self.analisys_title.setAlignment(QtCore.Qt.AlignCenter)
        self.analisys_title.setReadOnly(True)
        self.analisys_title.setText("Analisys")
         
        self.processing_title = QtWidgets.QLineEdit(self.option_widget)
        self.processing_title.setGeometry(QtCore.QRect(20, 300, 131, 20))
        self.processing_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(0, 0, 0);")
        self.processing_title.setAlignment(QtCore.Qt.AlignCenter)
        self.processing_title.setReadOnly(True)
        self.processing_title.setText("Processing")
        
        self.help_title = QtWidgets.QLineEdit(self.option_widget)
        self.help_title.setGeometry(QtCore.QRect(30, 510, 111, 16))
        self.help_title.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.help_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(0, 0, 0);")
        self.help_title.setAlignment(QtCore.Qt.AlignCenter)
        self.help_title.setReadOnly(True)
        self.help_title.setText("Help")
        
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)
        
    def applyShadow(self):
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QtGui.QColor(209, 209, 209))
        return shadow
    
    def maximize_window(self):
        screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(int(screen.height()*1.3), int(screen.height()*0.8))
        self.gridLayoutWidget.setGeometry(QtCore.QRect(257, 30, int(screen.height()*0.93), int(screen.height()*0.73)))
        self.RED_QLabel.setFixedSize(int(screen.height()*0.45),int(screen.height()*0.35))
        self.GREEN_QLabel.setFixedSize(int(screen.height()*0.45),int(screen.height()*0.35))
        self.BLUE_QLabel.setFixedSize(int(screen.height()*0.45),int(screen.height()*0.35))
        self.RGB_QLabel.setFixedSize(int(screen.height()*0.45),int(screen.height()*0.35))
    
    def processingWindow(self):
        if (self.red_image is None and self.green_image is None and self.blue_image is None):
            self.error_message("Missing image! Insert an image")
        else:
            self.processing = CellService_processing.Processing_cellService(self)
            self.processing.show()
        
    def analisysWindow(self):
        if (self.red_image is None and self.green_image is None and self.blue_image is None):
            self.error_message("Missing image! Insert an image")
        else:
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

    def set_all_images(self):
        self.set_image(self.rgb_image, self.RGB_QLabel, "rgb", mask=False)
        self.set_image(self.red_image, self.RED_QLabel, "red", mask=False)
        self.set_image(self.green_image, self.GREEN_QLabel, "green", mask=False)
        self.set_image(self.blue_image, self.BLUE_QLabel, "blue", mask=False)

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
        '''if self.red_image is None:
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
            return'''

        # RGB
        if (self.red_image is not None and self.green_image is not None and self.blue_image is not None):
            self.rgb_image = np.dstack((self.red_image, self.green_image, self.blue_image)).astype(np.uint8)
        if (self.red_image is not None and self.green_image is not None and self.blue_image is None):
            self.rgb_image = np.dstack((self.red_image, self.green_image, np.zeros(matrix_shape, dtype=np.uint8))).astype(np.uint8)
        if (self.red_image is None and self.green_image is not None and self.blue_image is not None):
            self.rgb_image = np.dstack((np.zeros(matrix_shape, dtype=np.uint8), self.green_image, self.blue_image)).astype(np.uint8)
        if (self.red_image is not None and self.green_image is None and self.blue_image is not None):
            self.rgb_image = np.dstack((self.red_image, np.zeros(matrix_shape, dtype=np.uint8), self.blue_image)).astype(np.uint8)
        if (self.red_image is not None and self.green_image is None and self.blue_image is None):
            self.rgb_image = np.dstack((self.red_image, np.zeros(matrix_shape, dtype=np.uint8), np.zeros(matrix_shape, dtype=np.uint8))).astype(np.uint8)
        if (self.red_image is None and self.green_image is not None and self.blue_image is None):
            self.rgb_image = np.dstack((np.zeros(matrix_shape, dtype=np.uint8), self.green_image, np.zeros(matrix_shape, dtype=np.uint8))).astype(np.uint8)
        if (self.red_image is None and self.green_image is None and self.blue_image is not None):
            self.rgb_image = np.dstack((np.zeros(matrix_shape, dtype=np.uint8), np.zeros(matrix_shape, dtype=np.uint8), self.blue_image)).astype(np.uint8)
          
        
        # Set images
        self.set_all_images()

    def error_message(self, text_error):
        msg = QMessageBox(self)
        msg.setFixedSize(200, 200)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(text_error)
        msg.setWindowTitle("Error")
        msg.exec_()
    
    def help_message(self):
        mbox = QMessageBox(self)
        mbox.setIcon(QMessageBox.Information)
        mbox.setWindowTitle("Help")
        mbox.setText("Cell Service")
        mbox.setInformativeText ("Application for image analysis. Insert the image in RGB format or the individual channels (red, green and blue) to continue. Alternatively, you can also open a single channel but you can only take advantage of the intensity, percentage of biological content and count functions. Remember that before the analysis you have to do the processing operation.")
        mbox.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = CellService()
    MainWindow.show()
    sys.exit(app.exec_())
    