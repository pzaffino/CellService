import sys
from PyQt5.QtWidgets import (QSlider, QDockWidget, QApplication, QWidget, QRadioButton, QPushButton, QToolTip, QLabel, QVBoxLayout, QDesktopWidget, QStyleFactory)
from PyQt5.QtWidgets import (QCheckBox, QBoxLayout,QFileDialog, QWidget, QMainWindow, QGroupBox, QAction, QMenu, QSystemTrayIcon, QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QImage
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot
import skimage.io
import skimage.morphology
import numpy as np
from skimage import filters,morphology

class CellServiceBinaryProcessing(QMainWindow):
    
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        self.setWindowTitle("Processing")
        self.setupUi()
        
        self.binary_processing()       
        
        self.segmentation_processing()
        
        self.menuBar()
    
    # 771,541
    def setupUi(self):
        self.resize(1128, 820)
        self.principal_widget = QtWidgets.QWidget()
        self.principal_widget.setStyleSheet("background-color: rgb(244, 244, 244);\n" "")
        self.gridLayoutWidget = QtWidgets.QWidget(self.principal_widget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(340, 120,1000, 700))
        self.principal_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.principal_layout.setContentsMargins(0, 0, 0, 0)
        self.Filtred_Label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Filtred_Label.setTabletTracking(True)
        self.Filtred_Label.setStyleSheet("border: 2px solid red")
        self.Filtred_Label.setFrameShape(QtWidgets.QFrame.Panel)
        self.Filtred_Label.setLineWidth(2)
        self.Filtred_Label.setScaledContents(True)
        self.principal_layout.addWidget(self.Filtred_Label, 1, 0, 1, 1)
        self.Original_Label2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Original_Label2.setStyleSheet("border: 2px solid blue")
        self.Original_Label2.setScaledContents(True)
        self.principal_layout.addWidget(self.Original_Label2, 0, 3, 1, 1)
        self.Original_Label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Original_Label.setTabletTracking(True)
        self.Original_Label.setStyleSheet("border: 2px solid red")
        self.Original_Label.setFrameShape(QtWidgets.QFrame.Panel)
        self.Original_Label.setLineWidth(2)
        self.Original_Label.setScaledContents(True)
        self.principal_layout.addWidget(self.Original_Label, 0, 0, 1, 1)
        self.Filtred_Label2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Filtred_Label2.setStyleSheet("border: 2px solid blue")
        self.Filtred_Label2.setScaledContents(True)
        self.principal_layout.addWidget(self.Filtred_Label2, 1, 3, 1, 1)
        self.Filtred_Label1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Filtred_Label1.setStyleSheet("border: 2px solid green")
        self.Filtred_Label1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Filtred_Label1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Filtred_Label1.setLineWidth(2)
        self.Filtred_Label1.setScaledContents(True)
        self.principal_layout.addWidget(self.Filtred_Label1, 1, 1, 1, 1)
        self.Original_Label1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Original_Label1.setStyleSheet("border: 2px solid green")
        self.Original_Label1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Original_Label1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Original_Label1.setLineWidth(2)
        self.Original_Label1.setScaledContents(True)
        self.principal_layout.addWidget(self.Original_Label1, 0, 1, 1, 1)
        
        self.radioRed = QtWidgets.QRadioButton(self.principal_widget)
        self.radioRed.setStyleSheet("font: 10pt \"Varela\";\n" "color: red;")
        self.radioRed.setChecked(True)
        self.radioRed.setText("Red Image")
        self.radioRed.setGeometry(QtCore.QRect(430, 60, 121, 31))
        self.radioGreen = QtWidgets.QRadioButton(self.principal_widget)
        self.radioGreen.setText("Green Image")
        self.radioGreen.setGeometry(QtCore.QRect(750, 60, 131, 31))
        self.radioGreen.setStyleSheet("font: 10pt \"Varela\";\n" "color: green;")
        self.radioBlue = QtWidgets.QRadioButton(self.principal_widget)
        self.radioBlue.setGeometry(QtCore.QRect(1100, 60, 121, 31))
        self.radioBlue.setStyleSheet("font: 10pt \"Varela\";\n" "color: blue;")
        self.radioBlue.setText("Blue Image")
        
        self.setCentralWidget(self.principal_widget)
        self.set_all_images()
        self.maximize_window()
    
    def binary_processing(self):
        self.binary_widget = QtWidgets.QWidget(self.principal_widget)
        self.binary_widget.setGeometry(QtCore.QRect(20, 20, 291, 301))
        self.binary_widget.setStyleSheet("background-color: rgb(255, 255, 255);\n" "border-radius: 30px;")
        self.binary_edit = QtWidgets.QLineEdit(self.binary_widget)
        self.binary_edit.setGeometry(QtCore.QRect(0, 0, 291, 41))
        self.binary_edit.setStyleSheet("background-color: rgb(19, 82, 255);\n"
            "border-radius:15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 14pt \"Varela\" bold;\n"
            "color: rgb(255, 255, 255);")
        self.binary_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.binary_edit.setReadOnly(True)
        self.binary_edit.setText("Binarize")
        self.fontSizeSpinBox = QtWidgets.QDoubleSpinBox(self.binary_widget)
        self.fontSizeSpinBox.setGeometry(QtCore.QRect(20, 70, 91, 31))
        self.fontSizeSpinBox.setTabletTracking(True)
        self.fontSizeSpinBox.setAutoFillBackground(False)
        self.fontSizeSpinBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(19, 82, 255);")
        self.fontSizeSpinBox.setDecimals(3)
        self.fontSizeSpinBox.setMaximum(255.0)
        self.fontSizeSpinBox2 = QtWidgets.QDoubleSpinBox(self.binary_widget)
        self.fontSizeSpinBox2.setGeometry(QtCore.QRect(20, 130, 91, 31))
        self.fontSizeSpinBox2.setTabletTracking(True)
        self.fontSizeSpinBox2.setAutoFillBackground(False)
        self.fontSizeSpinBox2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(19, 82, 255);")
        self.fontSizeSpinBox2.setDecimals(3)
        self.fontSizeSpinBox2.setMaximum(255.0)
        self.label = QtWidgets.QLabel(self.binary_widget)
        self.label.setGeometry(QtCore.QRect(140, 70, 131, 31))
        self.label.setText("Min Threashold")
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(19, 82, 255);")
        self.label_2 = QtWidgets.QLabel(self.binary_widget)
        self.label_2.setGeometry(QtCore.QRect(140, 130, 131, 31))
        self.label_2.setText("Max Threashold")
        self.label_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(19, 82, 255);")
        self.AutomaticButton = QtWidgets.QPushButton(self.binary_widget)
        self.AutomaticButton.setGeometry(QtCore.QRect(60, 180, 171, 41))
        self.AutomaticButton.clicked.connect(self.Automatic_threshold)
        self.AutomaticButton.setText("Automatic Threashold")
        self.AutomaticButton.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.Apply = QtWidgets.QPushButton(self.binary_widget)
        self.Apply.clicked.connect(self.runIntensityBinarization)
        self.Apply.setGeometry(QtCore.QRect(90, 230, 101, 41))
        self.Apply.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.Apply.setText("Apply")
        
    def segmentation_processing(self):
        self.segmentation_widget_2 = QtWidgets.QWidget(self.principal_widget)
        self.segmentation_widget_2.setGeometry(QtCore.QRect(20, 350, 291, 541))
        self.segmentation_widget_2.setStyleSheet("background-color: rgb(255, 255, 255);\n" "border-radius: 30px;")
        self.segmentation_edit_2 = QtWidgets.QLineEdit(self.segmentation_widget_2)
        self.segmentation_edit_2.setText("Segmentation")
        self.segmentation_edit_2.setGeometry(QtCore.QRect(0, 0, 291, 41))
        self.segmentation_edit_2.setStyleSheet("background-color: rgb(19, 82, 255);\n"
            "border-radius:15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 14pt \"Varela\" bold;\n"
            "color: rgb(255, 255, 255);")
        self.segmentation_edit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.segmentation_edit_2.setReadOnly(True)
        self.removeCheck = QtWidgets.QCheckBox(self.segmentation_widget_2)
        self.removeCheck.setText("Remove Small Object")
        self.removeCheck.setGeometry(QtCore.QRect(40, 120, 201, 31))
        self.removeCheck.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(19, 82, 255);")
        self.erosionCheck = QtWidgets.QCheckBox(self.segmentation_widget_2)
        self.erosionCheck.setText("Erosion")
        
        self.erosionCheck.setGeometry(QtCore.QRect(40, 150, 101, 31))
        self.erosionCheck.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(19, 82, 255);")
        self.dilationCheck = QtWidgets.QCheckBox(self.segmentation_widget_2)
        self.dilationCheck.setText("Dilation")
        self.dilationCheck.setGeometry(QtCore.QRect(150, 150, 101, 31))
        self.dilationCheck.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(19, 82, 255);")
        self.openCheck = QtWidgets.QCheckBox(self.segmentation_widget_2)
        self.openCheck.setText("Opening")
        self.openCheck.setGeometry(QtCore.QRect(40, 180, 101, 31))
        self.openCheck.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(19, 82, 255);")
        self.noiseCheck = QtWidgets.QCheckBox(self.segmentation_widget_2)
        self.noiseCheck.setText("Closing")
        self.noiseCheck.setGeometry(QtCore.QRect(150, 180, 101, 31))
        self.noiseCheck.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(19, 82, 255);")
        self.label_3 = QtWidgets.QLabel(self.segmentation_widget_2)
        self.label_3.setText("Radius")
        self.label_3.setGeometry(QtCore.QRect(150, 60, 71, 31))
        self.label_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(19, 82, 255);")
        self.Raggio = QtWidgets.QDoubleSpinBox(self.segmentation_widget_2)
        self.Raggio.setGeometry(QtCore.QRect(30, 60, 91, 31))
        self.Raggio.setTabletTracking(True)
        self.Raggio.setAutoFillBackground(False)
        self.Raggio.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(19, 82, 255);")
        self.Raggio.setDecimals(3)
        self.Raggio.setMaximum(255.0)
        self.Label_Save = QtWidgets.QLabel(self.segmentation_widget_2)
        self.Label_Save.setText("Don't forget to save image!")
        self.Label_Save.setWordWrap(True)
        self.Label_Save.setGeometry(QtCore.QRect(40, 280, 211, 151))
        self.Label_Save.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(19, 82, 255);")
        self.pushButton = QtWidgets.QPushButton(self.segmentation_widget_2)
        self.pushButton.clicked.connect(self.apply_segmentation)
        self.pushButton.setText("Apply")
        self.pushButton.setGeometry(QtCore.QRect(50, 230, 91, 41))
        self.pushButton.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.pushButton_2 = QtWidgets.QPushButton(self.segmentation_widget_2)
        self.pushButton_2.setText("Save")
        self.pushButton_2.clicked.connect(self.save)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 230, 101, 41))
        self.pushButton_2.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.mask_red=None
        self.mask_green=None
        self.mask_blue=None
        
    def menuBar(self):
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1128, 26))
        self.menubar.setTabletTracking(False)
        self.menubar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.menubar.setStyleSheet("background-color: rgb(255, 253, 253);\n"
            "selection-color: rgb(128, 183, 255);\n"
            "color: rgb(71, 71, 71);")
        self.help_menu = QtWidgets.QMenu(self.menubar)
        self.help_menu.setTitle( "Help")
        self.setMenuBar(self.menubar)
        self.menubar.addAction(self.help_menu.menuAction())
    
    def maximize_window(self):
        screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(int(screen.height()*1.3), int(screen.height()*0.9))
    
    def set_all_images(self):
        self.parent.set_image(self.parent.red_image, self.Original_Label, "red", mask=False)
        self.parent.set_image(self.parent.green_image, self.Original_Label1, "green", mask=False)
        self.parent.set_image(self.parent.blue_image, self.Original_Label2, "blue", mask=False)
    
    def runIntensityBinarization(self):
        if self.radioRed.isChecked():
            self.parent.red_mask = self.binarizeImage(self.parent.red_image)
            self.parent.set_image(self.parent.red_mask, self.Filtred_Label, "red", mask=True)
        elif self.radioGreen.isChecked():
            self.parent.green_mask = self.binarizeImage(self.parent.green_image)
            self.parent.set_image(self.parent.green_mask, self.Filtred_Label1, "green", mask=True)
        elif self.radioBlue.isChecked():
            self.parent.blue_mask = self.binarizeImage(self.parent.blue_image)
            self.parent.set_image(self.parent.blue_mask, self.Filtred_Label2, "blue", mask=True)
        else:
            pass
    
    def Automatic_threshold(self):
        self.soglia1=0
        if self.radioRed.isChecked():
            self.soglia1 = filters.threshold_otsu(self.parent.red_image)
        elif self.radioGreen.isChecked():
            self.soglia1 = filters.threshold_otsu(self.parent.green_image)
        elif self.radioBlue.isChecked():
            self.soglia1 = filters.threshold_otsu(self.parent.blue_image)
        else:
            pass
        self.fontSizeSpinBox.setValue(self.soglia1)
    
    def binarizeImage(self,img):
        valore1 = self.fontSizeSpinBox.value()
        valore2 =self.fontSizeSpinBox2.value()
        binarymat = np.zeros_like(img, dtype=np.uint8)
        if (valore1==0):
            valore1=filters.threshold_otsu(img)
        if (valore2!=0):
            mask=np.logical_and(img > valore1, img < valore2)
            binarymat[mask]=1
        if (valore2==0):
            mask=img>valore1
            binarymat[mask]=1
        return binarymat
    
    def apply_segmentation(self):
        notRed=True
        notGreen=True
        notBlue=True
        if self.radioRed.isChecked():
            if self.erosionCheck.isChecked():
                self.mask_red=morphology.erosion(self.parent.red_mask)
                notRed=False
            if self.dilationCheck.isChecked():
                if(self.mask_red is not None):
                    self.mask_red=morphology.dilation(self.mask_red)
                else:
                    self.mask_red=morphology.dilation(self.parent.red_mask)
                notRed=False
            if self.noiseCheck.isChecked():
                if(self.mask_red is not None):
                    self.mask_red=morphology.binary_closing(self.mask_red)
                else:
                    self.mask_red=morphology.binary_closing(self.parent.red_mask)
                notRed=False
            if self.openCheck.isChecked():
                if(self.mask_red is not None):
                    self.mask_red=morphology.binary_opening(self.mask_red)
                else:
                    self.mask_red=morphology.binary_opening(self.parent.red_mask)
                notRed=False
            if self.removeCheck.isChecked():
                raggio=self.Raggio.value()
                if(self.mask_red is not None):
                    self.mask_red= morphology.remove_small_objects(self.mask_red.astype(np.bool), raggio)
                else:
                    self.mask_red= morphology.remove_small_objects(self.parent.red_mask.astype(np.bool), raggio)
                notRed=False
            if notRed:
                self.mask_red=None
                self.parent.set_image(self.parent.red_mask, self.Filtred_Label, "red", mask=True)
            self.parent.set_image(self.mask_red, self.Filtred_Label, "red", mask=True)
            self.Label_Save.setText("Don't forget to save image!")
        if self.radioGreen.isChecked():
            if self.erosionCheck.isChecked():
                self.mask_green=morphology.erosion(self.parent.green_mask)
                notGreen=False
            if self.dilationCheck.isChecked():
                if(self.mask_green is not None):
                    self.mask_green=morphology.dilation(self.mask_green)
                else:
                    self.mask_green=morphology.dilation(self.parent.green_mask)
                notGreen=False
            if self.noiseCheck.isChecked():
                if(self.mask_green is not None):
                    self.mask_green=morphology.binary_closing(self.mask_green)
                else:
                    self.mask_green=morphology.binary_closing(self.parent.green_mask)
                notGreen=False
            if self.openCheck.isChecked():
                if(self.mask_green is not None):
                    self.mask_green=morphology.binary_opening(self.mask_green)
                else:
                    self.mask_green=morphology.binary_opening(self.parent.green_mask)
                notGreen=False
            if self.removeCheck.isChecked():
                raggio=self.Raggio.value()
                if(self.mask_green is not None):
                    self.mask_green= morphology.remove_small_objects(self.mask_green.astype(np.bool), raggio)
                else:
                    self.mask_green= morphology.remove_small_objects(self.parent.green_mask.astype(np.bool), raggio)
                notGreen=False
            if notGreen:
                self.mask_green=None
                self.parent.set_image(self.parent.green_mask, self.Filtred_Label1, "green", mask=True)
            self.parent.set_image(self.mask_green, self.Filtred_Label1, "green", mask=True)
            self.Label_Save.setText("Don't forget to save image!")
        if self.radioBlue.isChecked():
            if self.noiseCheck.isChecked():
                self.mask_blue=morphology.binary_closing(self.parent.blue_mask)
                notBlue=False
            if self.dilationCheck.isChecked():
                if(self.mask_blue is not None):
                    self.mask_blue=morphology.dilation(self.mask_blue)
                else:
                    self.mask_blue=morphology.dilation(self.parent.blue_mask)
                notBlue=False
            if self.openCheck.isChecked():
                if(self.mask_blue is not None):
                    self.mask_blue=morphology.binary_opening(self.mask_blue)
                else:
                    self.mask_blue=morphology.binary_opening(self.parent.blue_mask)
                notBlue=False
            if self.erosionCheck.isChecked():
                if(self.mask_blue is not None):
                    self.mask_blue=morphology.erosion(self.mask_blue)
                else:
                    self.mask_blue=morphology.erosion(self.parent.blue_mask)
                notBlue=False
            if self.removeCheck.isChecked():
                raggio=self.Raggio.value()
                if(self.mask_blue is not None):
                    self.mask_blue= morphology.remove_small_objects(self.mask_blue.astype(np.bool), raggio)
                else:
                    self.mask_blue= morphology.remove_small_objects(self.parent.blue_mask.astype(np.bool), raggio)
                notBlue=False
            if notBlue:
                self.mask_blue=None
                self.parent.set_image(self.parent.blue_mask, self.Filtred_Label2, "blue", mask=True)
            self.parent.set_image(self.mask_blue, self.Filtred_Label2, "blue", mask=True)
            self.Label_Save.setText("Don't forget to save image!")
    
    def save(self):
        if(self.mask_red is not None):
            self.parent.red_mask = self.mask_red
        if(self.mask_green is not None):
            self.parent.green_mask = self.mask_green
        if(self.mask_blue is not None):
            self.parent.blue_mask = self.mask_blue
        self.Label_Save.setText("SAVED IMAGES! IF YOU WANT TO CHANGE THE IMAGES, REMEMBER TO REPEAT THE BINARIZATION")