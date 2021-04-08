import sys
from PyQt5.QtWidgets import (QSlider, QDockWidget, QApplication, QWidget, QRadioButton, QPushButton, QToolTip, QLabel, QVBoxLayout, QDesktopWidget, QStyleFactory)
from PyQt5.QtWidgets import (QMessageBox, QCheckBox, QBoxLayout,QFileDialog, QWidget, QMainWindow, QGroupBox, QAction, QMenu, QSystemTrayIcon, QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QImage
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot, QRect
import skimage.io
import skimage.morphology
import numpy as np
from skimage import filters,morphology

class CellServiceBinaryProcessing(QMainWindow):
    
    def __init__(self, parent):
        super().__init__()
        
        self.local_red_mask=None
        self.local_green_mask=None
        self.local_blue_mask=None
        self.mask_red=None
        self.mask_green=None
        self.mask_blue=None
        
        self.parent = parent
        self.setWindowTitle("Processing")
        self.setupUi()
        
        self.binary_processing()       
        
        self.segmentation_processing()
        self.set_intensityWidget()
    
    # 771,541
    def setupUi(self):
        self.principal_widget = QtWidgets.QWidget()
        self.setFixedSize(1500, 820)
        self.principal_widget.setStyleSheet("background-color:qradialgradient(spread:reflect, cx:0.5, cy:0.494318, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(135, 200, 255, 255), stop:1 rgba(255, 255, 255, 255)) ;\n")
        self.gridLayoutWidget = QtWidgets.QWidget(self.principal_widget)
        self.gridLayoutWidget.setStyleSheet("background-color: white;\n" "border-radius: 10px;\n")
        self.gridLayoutWidget.setGeometry(QtCore.QRect(340, 120, 771, 541))
        self.principal_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.principal_layout.setContentsMargins(0, 0, 0, 0)
        
        self.Original_Label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Original_Label.setStyleSheet("border-radius: 10px;\n" "border: 3px solid red")
        self.Original_Label.setScaledContents(True)
        self.principal_layout.addWidget(self.Original_Label, 0, 0, 1, 1)
        self.Filtred_Label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Filtred_Label.setStyleSheet("border-radius: 10px;\n" "border: 3px solid red")
        self.Filtred_Label.setScaledContents(True)
        self.principal_layout.addWidget(self.Filtred_Label, 1, 0, 1, 1)
        
        self.Original_Label1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Original_Label1.setStyleSheet("border-radius: 10px;\n" "border: 3px solid green")
        self.Original_Label1.setScaledContents(True)
        self.principal_layout.addWidget(self.Original_Label1, 0, 1, 1, 1)
        self.Filtred_Label1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Filtred_Label1.setStyleSheet("border-radius: 10px;\n" "border: 3px solid green")
        self.Filtred_Label1.setScaledContents(True)
        self.principal_layout.addWidget(self.Filtred_Label1, 1, 1, 1, 1)
        
        self.Original_Label2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Original_Label2.setStyleSheet("border-radius: 10px;\n" "border: 3px solid blue")
        self.Original_Label2.setScaledContents(True)
        self.principal_layout.addWidget(self.Original_Label2, 0, 3, 1, 1)
        self.Filtred_Label2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Filtred_Label2.setStyleSheet("border-radius: 10px;\n" "border: 3px solid blue")
        self.Filtred_Label2.setScaledContents(True)
        self.principal_layout.addWidget(self.Filtred_Label2, 1, 3, 1, 1)
        
        
        self.radioRed = QtWidgets.QRadioButton(self.principal_widget)
        self.radioRed.setStyleSheet("background-color: white;" "border-radius: 10px;\n" "font: 10pt \"Varela\";\n" "color: red;")
        self.radioRed.setChecked(True)
        self.radioRed.setGeometry(QtCore.QRect(400, 60, 121, 31))
        self.radioRed.setText("Red Image")
        self.radioGreen = QtWidgets.QRadioButton(self.principal_widget)
        self.radioGreen.setText("Green Image")
        self.radioGreen.setGeometry(QtCore.QRect(650, 60, 131, 31))
        self.radioGreen.setStyleSheet("background-color: white;" "border-radius: 10px;\n" "font: 10pt \"Varela\";\n" "color: green;")
        self.radioBlue = QtWidgets.QRadioButton(self.principal_widget)
        self.radioBlue.setStyleSheet("background-color: white;" "border-radius: 10px;\n" "font: 10pt \"Varela\";\n" "color: blue;")
        self.radioBlue.setText("Blue Image")
        self.radioBlue.setGeometry(QtCore.QRect(930, 60, 121, 31))
        self.selezioni=np.array([0,0,0,0,0])
        self.valore=0
        self.setCentralWidget(self.principal_widget)
        self.set_all_images()

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
        self.fontSizeSpinBox.setGeometry(QtCore.QRect(10, 70, 95, 31))
        self.fontSizeSpinBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(19, 82, 255);")
        self.fontSizeSpinBox.setDecimals(3)
        self.fontSizeSpinBox.setMaximum(255.0)
        self.fontSizeSpinBox2 = QtWidgets.QDoubleSpinBox(self.binary_widget)
        self.fontSizeSpinBox2.setGeometry(QtCore.QRect(10, 130, 95, 31))
        self.fontSizeSpinBox2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(19, 82, 255);")
        self.fontSizeSpinBox2.setDecimals(3)
        self.fontSizeSpinBox2.setMaximum(255.0)
        self.label = QtWidgets.QLabel(self.binary_widget)
        self.label.setGeometry(QtCore.QRect(110, 70, 131, 31))
        self.label.setText("Min Threashold")
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(19, 82, 255);")
        self.label_2 = QtWidgets.QLabel(self.binary_widget)
        self.label_2.setGeometry(QtCore.QRect(110, 130, 131, 31))
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
        self.Label_Save.setGeometry(QtCore.QRect(40, 330, 211, 151))
        self.Label_Save.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "    border-radius: 10px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(19, 82, 255);")
        
        
    def set_intensityWidget(self):
        self.intensity_widget = QtWidgets.QWidget(self.principal_widget)
        self.intensity_widget.setGeometry(QtCore.QRect(1150, 50, 300, 600))
        self.intensity_widget.setStyleSheet("background-color: rgb(255, 255, 255);\n" "border-radius: 35px;")
        self.intensity_widget.setGraphicsEffect(self.applyShadow())

        self.Remove_button= QtWidgets.QPushButton(self.intensity_widget)
        
        self.Remove_button.setGeometry(QtCore.QRect(10, 60, 41, 41))
        self.Remove_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Remove_button.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Remove_button.setGraphicsEffect(self.applyShadow())
        icon10 = QtGui.QIcon("Icon/icon int 1.png")
        self.Remove_button.setIcon(icon10)
        self.Remove_button.setIconSize(QtCore.QSize(60, 35))
        icon_help = QtGui.QIcon("Icon/help.png")
        self.Remove_edit_help = QtWidgets.QPushButton(self.intensity_widget)
        self.Remove_edit_help.setIcon(icon_help)
        self.Remove_edit_help.clicked.connect(self.remove_message)
        self.Remove_edit_help.setGeometry(QtCore.QRect(60, 70, 61, 31))
        self.Remove_edit_help.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(28, 83, 255);\n"
            "border-radius: 15px;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Remove_edit_help.setGraphicsEffect(self.applyShadow())
        
        self.Erosion_button = QtWidgets.QPushButton(self.intensity_widget)
        self.Erosion_button.setGeometry(QtCore.QRect(10, 130, 41, 41))
        self.Erosion_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Erosion_button.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Erosion_button.setGraphicsEffect(self.applyShadow())
        icon11 = QtGui.QIcon("Icon/icon int 3.png")
        self.Erosion_button.setIcon(icon11)
        self.Erosion_button.setIconSize(QtCore.QSize(60, 35))
        self.Erosion_edit_help = QtWidgets.QPushButton(self.intensity_widget)
        self.Erosion_edit_help.setIcon(icon_help)
        self.Erosion_edit_help.clicked.connect(self.erosion_message)
        self.Erosion_edit_help.setGeometry(QtCore.QRect(60, 140, 61, 31))
        self.Erosion_edit_help.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(28, 83, 255);\n"
            "border-radius: 15px;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Erosion_edit_help.setGraphicsEffect(self.applyShadow())
        
        self.Dilation_button = QtWidgets.QPushButton(self.intensity_widget)
        self.Dilation_button.setGeometry(QtCore.QRect(10, 200, 41, 41))
        self.Dilation_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Dilation_button.setStyleSheet("QPushButton {\n"
            "    background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Dilation_button.setGraphicsEffect(self.applyShadow())
        icon12 = QtGui.QIcon("Icon/icon int 2.png")
        self.Dilation_button.setIcon(icon12)
        self.Dilation_button.setIconSize(QtCore.QSize(60, 35))
        self.Dilation_edit_help = QtWidgets.QPushButton(self.intensity_widget)
        self.Dilation_edit_help.setIcon(icon_help)
        self.Dilation_edit_help.clicked.connect(self.dilation_message)
        self.Dilation_edit_help.setGeometry(QtCore.QRect(60, 210, 61, 31))
        self.Dilation_edit_help.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(28, 83, 255);\n"
            "border-radius: 15px;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Dilation_edit_help.setGraphicsEffect(self.applyShadow())
        
        self.Open_button= QtWidgets.QPushButton(self.intensity_widget)
        self.Open_button.setGeometry(QtCore.QRect(10, 270, 41, 41))
        self.Open_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Open_button.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Open_button.setGraphicsEffect(self.applyShadow())
        icon10 = QtGui.QIcon("Icon/icon int 1.png")
        self.Open_button.setIcon(icon10)
        self.Open_button.setIconSize(QtCore.QSize(60, 35))
        self.Open_edit_help = QtWidgets.QPushButton(self.intensity_widget)
        self.Open_edit_help.setIcon(icon_help)
        self.Open_edit_help.clicked.connect(self.open_message)
        self.Open_edit_help.setGeometry(QtCore.QRect(60, 280, 61, 31))
        self.Open_edit_help.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(28, 83, 255);\n"
            "border-radius: 15px;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Open_edit_help.setGraphicsEffect(self.applyShadow())
        
        self.Close_button= QtWidgets.QPushButton(self.intensity_widget)
        self.Close_button.setGeometry(QtCore.QRect(10, 340, 41, 41))
        self.Close_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Close_button.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Close_button.setGraphicsEffect(self.applyShadow())
        icon10 = QtGui.QIcon("Icon/icon int 1.png")
        self.Close_button.setIcon(icon10)
        self.Close_button.setIconSize(QtCore.QSize(60, 35))
        self.Close_edit_help = QtWidgets.QPushButton(self.intensity_widget)
        self.Close_edit_help.setIcon(icon_help)
        self.Close_edit_help.clicked.connect(self.close_message)
        self.Close_edit_help.setGeometry(QtCore.QRect(60, 350, 61, 31))
        self.Close_edit_help.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(28, 83, 255);\n"
            "border-radius: 15px;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Close_edit_help.setGraphicsEffect(self.applyShadow())
        
        self.intensity_edit = QtWidgets.QLineEdit(self.intensity_widget)
        self.intensity_edit.setGeometry(QtCore.QRect(0, 0, 300, 41))
        self.intensity_edit.setStyleSheet("background-color: rgb(19, 82, 255);\n"
            "border-radius:15px;\n"
            "    padding: 6px;\n"
            "font: 14pt \"Arial\";\n"
            "color: rgb(255, 255, 255);")
        self.intensity_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.intensity_edit.setReadOnly(True)
        self.intensity_edit.setText("Segmentation")
        
        self.remove_title = QtWidgets.QLineEdit(self.intensity_widget)
        self.remove_title.setGeometry(QtCore.QRect(60, 50, 200, 20))
        self.remove_title.setText("Remove small object")
        self.remove_title.setStyleSheet("font: 7.5pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.remove_title.setReadOnly(True)
        self.Remove_edit= QtWidgets.QLineEdit(self.intensity_widget)
        self.Remove_edit.setGeometry(QtCore.QRect(125, 70, 61, 31))
        self.Remove_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.Remove_edit.setReadOnly(True)
        self.Remove_button.clicked.connect(self.set_edit_remove)
        self.Remove_canc = QtWidgets.QPushButton(self.intensity_widget)
        self.Remove_canc.setText("Del")
        self.Remove_canc.clicked.connect(self.delete_edit_remove)
        self.Remove_canc.setGeometry(QtCore.QRect(190, 70, 61, 31))
        self.Remove_canc.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(28, 83, 255);\n"
            "border-radius: 15px;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        
        self.dilation_title = QtWidgets.QLineEdit(self.intensity_widget)
        self.dilation_title.setGeometry(QtCore.QRect(85, 190, 85, 20))
        self.dilation_title.setStyleSheet("font: 7.5pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.dilation_title.setReadOnly(True)
        self.dilation_title.setText("Dilation")
        self.Dilation_edit = QtWidgets.QLineEdit(self.intensity_widget)
        self.Dilation_edit.setGeometry(QtCore.QRect(125, 210, 61, 31))
        self.Dilation_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.Dilation_edit.setReadOnly(True)
        self.Dilation_button.clicked.connect(self.set_edit_dilation)
        self.Dilation_canc = QtWidgets.QPushButton(self.intensity_widget)
        self.Dilation_canc.clicked.connect(self.delete_edit_dilation)
        self.Dilation_canc.setText("Del")
        self.Dilation_canc.setGeometry(QtCore.QRect(190, 210, 61, 31))
        self.Dilation_canc.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(28, 83, 255);\n"
            "border-radius: 15px;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        
        self.erosion_title = QtWidgets.QLineEdit(self.intensity_widget)
        self.erosion_title.setGeometry(QtCore.QRect(85, 120, 90, 20))
        self.erosion_title.setStyleSheet("font: 7.5pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.erosion_title.setReadOnly(True)
        self.erosion_title.setText("Erosion")
        self.Erosion_edit = QtWidgets.QLineEdit(self.intensity_widget)
        self.Erosion_edit.setGeometry(QtCore.QRect(125, 140, 61, 31))
        self.Erosion_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.Erosion_edit.setReadOnly(True)
        self.Erosion_button.clicked.connect(self.set_edit_erosion)
        self.Erosion_canc = QtWidgets.QPushButton(self.intensity_widget)
        self.Erosion_canc.setText("Del")
        self.Erosion_canc.clicked.connect(self.delete_edit_erosion)
        self.Erosion_canc.setGeometry(QtCore.QRect(190, 140, 61, 31))
        self.Erosion_canc.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(28, 83, 255);\n"
            "border-radius: 15px;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        
        self.open_title = QtWidgets.QLineEdit(self.intensity_widget)
        self.open_title.setGeometry(QtCore.QRect(85, 260, 90, 20))
        self.open_title.setText("Opening")
        self.open_title.setStyleSheet("font: 7.5pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.open_title.setReadOnly(True)
        self.Open_edit= QtWidgets.QLineEdit(self.intensity_widget)
        self.Open_edit.setGeometry(QtCore.QRect(125, 280, 61, 31))
        self.Open_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.Open_edit.setReadOnly(True)
        self.Open_button.clicked.connect(self.set_edit_open)
        self.Open_canc = QtWidgets.QPushButton(self.intensity_widget)
        self.Open_canc.setText("Del")
        self.Open_canc.setGeometry(QtCore.QRect(190, 280, 61, 31))
        self.Open_canc.clicked.connect(self.delete_edit_open)
        self.Open_canc.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(28, 83, 255);\n"
            "border-radius: 15px;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        
        self.close_title = QtWidgets.QLineEdit(self.intensity_widget)
        self.close_title.setGeometry(QtCore.QRect(85, 330, 90, 20))
        self.close_title.setText("Closing")
        self.close_title.setStyleSheet("font: 7.5pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.close_title.setReadOnly(True)
        self.Close_edit= QtWidgets.QLineEdit(self.intensity_widget)
        self.Close_edit.setGeometry(QtCore.QRect(125, 350, 61, 31))
        self.Close_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.Close_edit.setReadOnly(True)
        self.Close_button.clicked.connect(self.set_edit_close)
        self.Close_canc = QtWidgets.QPushButton(self.intensity_widget)
        self.Close_canc.setText("Del")
        self.Close_canc.setGeometry(QtCore.QRect(190, 350, 61, 31))
        self.Close_canc.clicked.connect(self.delete_edit_close)
        self.Close_canc.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(28, 83, 255);\n"
            "border-radius: 15px;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        
        self.setCentralWidget(self.principal_widget)
        
        self.Apply_Segmentation = QtWidgets.QPushButton(self.intensity_widget)
        self.Apply_Segmentation.clicked.connect(self.apply_segmentation)
        self.Apply_Segmentation.setText("New Segmentation")
        self.Apply_Segmentation.setGeometry(QtCore.QRect(10, 420, 150, 41))
        self.Apply_Segmentation.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.Add = QtWidgets.QPushButton(self.intensity_widget)
        self.Add.setText("Add Change")
        self.Add.setGeometry(QtCore.QRect(170, 420, 100, 41))
        self.Add.clicked.connect(self.add_change)
        self.Add.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.Save = QtWidgets.QPushButton(self.intensity_widget)
        self.Save.setText("Save")
        self.Save.clicked.connect(self.save)
        self.Save.setGeometry(QtCore.QRect(110, 470, 101, 41))
        self.Save.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.clear_filtred_label = QtWidgets.QPushButton(self.intensity_widget)
        self.clear_filtred_label.setGeometry(QtCore.QRect(80, 520, 150, 41))
        self.clear_filtred_label.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.clear_filtred_label.setText("Clear Filtred Label")
        self.clear_filtred_label.clicked.connect(self.Clear_filtred_label)
        
    
    def set_all_images(self):
        self.parent.set_image(self.parent.red_image, self.Original_Label, "red", mask=False)
        self.parent.set_image(self.parent.green_image, self.Original_Label1, "green", mask=False)
        self.parent.set_image(self.parent.blue_image, self.Original_Label2, "blue", mask=False)
        self.Repeat_Red=False
        self.Repeat_Green=False
        self.Repeat_Blue=False
    
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
        if(self.parent.red_image is None):
            self.error_message("Missing images! Upload images to continue.")
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
    
    def control(self):
        if (self.valore==0):
            self.setEnabled_True_Button()
    
    def set_edit_remove(self):
        self.control()
        self.valore=self.valore+1
        self.selezioni[(self.valore-1)]=1
        self.Remove_edit.setText(str(self.valore))
    
    def set_edit_erosion(self):
        self.control()
        self.valore=self.valore+1
        self.selezioni[(self.valore-1)]=2
        self.Erosion_edit.setText(str(self.valore))
    
    def set_edit_dilation(self):
        self.control()
        self.valore=self.valore+1
        self.selezioni[(self.valore-1)]=3
        self.Dilation_edit.setText(str(self.valore))
    
    def set_edit_open(self):
        self.control()
        self.valore=self.valore+1
        self.selezioni[(self.valore-1)]=4
        self.Open_edit.setText(str(self.valore))
    
    def set_edit_close(self):
        self.valore=self.valore+1
        self.selezioni[(self.valore-1)]=5
        self.Close_edit.setText(str(self.valore))
        
    def apply_segmentation(self):
        self.notRed=True
        self.notGreen=True
        self.notBlue=True
        if self.radioRed.isChecked():
            if(self.parent.red_mask is None):
                self.error_message("Binarize red image")
            if(self.Repeat_Red):
                self.mask_red=None
        if self.radioGreen.isChecked():
            if(self.parent.green_mask is None):
                self.error_message("Binarize green image")
            if(self.Repeat_Green):
                self.mask_green=None
        if self.radioBlue.isChecked():
            if(self.parent.blue_mask is None):
                self.error_message("Binarize blue image")
            if(self.Repeat_Blue):
                self.mask_green=None
        for i in range (0,5):
            if (self.selezioni[i]==1):
                raggio=self.Raggio.value()
                if raggio==0:
                    self.error_message("Insert a radius!")
                    pass
                elif self.radioRed.isChecked():
                    if(self.mask_red is not None):
                        self.mask_red= morphology.remove_small_objects(self.mask_red.astype(np.bool), raggio)
                    else:
                        self.mask_red= morphology.remove_small_objects(self.parent.red_mask.astype(np.bool), raggio)
                    self.notRed=False
                    self.parent.set_image(self.mask_red, self.Filtred_Label, "red", mask=True)
                    print("arrivato in set red")
                elif self.radioGreen.isChecked():
                    if(self.mask_green is not None):
                        self.mask_green= morphology.remove_small_objects(self.mask_green.astype(np.bool), raggio)
                    else:
                        self.mask_green= morphology.remove_small_objects(self.parent.green_mask.astype(np.bool), raggio)
                    self.notGreen=False
                    self.parent.set_image(self.mask_green, self.Filtred_Label1, "green", mask=True)
                elif self.radioBlue.isChecked():
                    raggio=self.Raggio.value()
                    if (self.mask_blue is not None):
                        self.mask_blue= morphology.remove_small_objects(self.mask_blue.astype(np.bool), raggio)
                    else:
                        self.mask_blue= morphology.remove_small_objects(self.parent.blue_mask.astype(np.bool), raggio)
                    self.notBlue=False
                    self.parent.set_image(self.mask_blue, self.Filtred_Label2, "blue", mask=True) 
            elif (self.selezioni[i]==2):
                if self.radioRed.isChecked():
                    if(self.mask_blue is not None):
                        self.mask_red=morphology.binary_erosion(self.mask_red)
                    else:
                        self.mask_red=morphology.binary_erosion(self.parent.red_mask)
                    self.notRed=False
                    self.parent.set_image(self.mask_red, self.Filtred_Label, "red", mask=True)
                    print("arrivato in set red 2")
                if self.radioGreen.isChecked():
                    if(self.mask_green is not None):
                        self.mask_green=morphology.binary_erosion(self.mask_green)
                    else:
                        self.mask_green=morphology.binary_erosion(self.parent.green_mask)
                    self.notGreen=False
                    self.parent.set_image(self.mask_green, self.Filtred_Label1, "green", mask=True)
                if self.radioBlue.isChecked():
                    if(self.mask_blue is not None):
                        self.mask_blue=morphology.binary_erosion(self.mask_blue)
                    else:
                        self.mask_blue=morphology.binary_erosion(self.parent.blue_mask)
                    self.notBlue=False
                    self.parent.set_image(self.mask_blue, self.Filtred_Label2, "blue", mask=True) 
            elif (self.selezioni[i]==3):
                if self.radioRed.isChecked():
                    if(self.mask_blue is not None):
                        self.mask_red=morphology.binary_dilation(self.mask_red)
                    else:
                        self.mask_red=morphology.binary_dilation(self.parent.red_mask)
                    self.notRed=False
                    self.parent.set_image(self.mask_red, self.Filtred_Label, "red", mask=True)
                    print("arrivato in set red 3")
                if self.radioGreen.isChecked():
                    if(self.mask_green is not None):
                        self.mask_green=morphology.binary_dilation(self.mask_green)
                    else:
                        self.mask_green=morphology.binary_dilation(self.parent.green_mask)
                    self.notGreen=False
                    self.parent.set_image(self.mask_green, self.Filtred_Label1, "green", mask=True)
                if self.radioBlue.isChecked():
                    if(self.mask_blue is not None):
                        self.mask_blue=morphology.binary_dilation(self.mask_blue)
                    else:
                        self.mask_blue=morphology.binary_dilation(self.parent.blue_mask)
                    self.notBlue=False
                    self.parent.set_image(self.mask_blue, self.Filtred_Label2, "blue", mask=True) 
            elif (self.selezioni[i]==4):
                if self.radioRed.isChecked():
                    if(self.mask_blue is not None):
                        self.mask_red=morphology.binary_opening(self.mask_red)
                    else:
                        self.mask_red=morphology.binary_opening(self.parent.red_mask)
                    self.notRed=False
                    self.parent.set_image(self.mask_red, self.Filtred_Label, "red", mask=True)
                    print("arrivato in set red 4")
                if self.radioGreen.isChecked():
                    if(self.mask_green is not None):
                        self.mask_green=morphology.binary_opening(self.mask_green)
                    else:
                        self.mask_green=morphology.binary_opening(self.parent.green_mask)
                    self.notGreen=False
                    self.parent.set_image(self.mask_green, self.Filtred_Label1, "green", mask=True)
                if self.radioBlue.isChecked():
                    if(self.mask_blue is not None):
                        self.mask_blue=morphology.binary_opening(self.mask_blue)
                    else:
                        self.mask_blue=morphology.binary_opening(self.parent.blue_mask)
                    self.notBlue=False
                    self.parent.set_image(self.mask_blue, self.Filtred_Label2, "blue", mask=True) 
            elif (self.selezioni[i]==5):
                if self.radioRed.isChecked():
                    if(self.mask_blue is not None):
                        self.mask_red=morphology.binary_closing(self.mask_red)
                    else:
                        self.mask_red=morphology.binary_closing(self.parent.red_mask)
                    self.notRed=False
                    self.parent.set_image(self.mask_red, self.Filtred_Label, "red", mask=True)
                    print("arrivato in set red 5")
                if self.radioGreen.isChecked():
                    if(self.mask_green is not None):
                        self.mask_green=morphology.binary_closing(self.mask_green)
                    else:
                        self.mask_green=morphology.binary_closing(self.parent.green_mask)
                    self.notGreen=False
                    self.parent.set_image(self.mask_green, self.Filtred_Label1, "green", mask=True)
                if self.radioBlue.isChecked():
                    if(self.mask_blue is not None):
                        self.mask_blue=morphology.binary_closing(self.mask_blue)
                    else:
                        self.mask_blue=morphology.binary_closing(self.parent.blue_mask)
                    self.notBlue=False
                    self.parent.set_image(self.mask_blue, self.Filtred_Label2, "blue", mask=True) 
        if self.radioRed.isChecked() and self.notRed:
            self.parent.set_image(self.parent.red_mask, self.Filtred_Label, "red", mask=True)
        if self.radioGreen.isChecked() and self.notGreen:
            self.parent.set_image(self.parent.green_mask, self.Filtred_Label1, "green", mask=True)
        if self.radioBlue.isChecked() and self.notBlue:
            self.parent.set_image(self.parent.blue_mask, self.Filtred_Label2, "blue", mask=True) 
        self.Label_Save.setText("Don't forget to save image!")
        self.Repeat_Red=True
        self.Repeat_Green=True
        self.Repeat_Blue=True
        self.notRed=True
        self.notGreen=True
        self.notBlue=True
        self.clear_edit_label()
        self.setEnabled_False_Button()
    
    def setEnabled_False_Button(self):
        self.Remove_canc.setEnabled(False)
        self.Dilation_canc.setEnabled(False)
        self.Erosion_canc.setEnabled(False)
        self.Open_canc.setEnabled(False)
        self.Close_canc.setEnabled(False)
    
    def setEnabled_True_Button(self):
        self.Remove_canc.setEnabled(True)
        self.Dilation_canc.setEnabled(True)
        self.Erosion_canc.setEnabled(True)
        self.Open_canc.setEnabled(True)
        self.Close_canc.setEnabled(True)
    
    def delete(self, label):
        current_number=int(label.text())-1
        print(current_number)
        for i in range (current_number, (len(self.selezioni))):
            if(i==(len(self.selezioni)-1)):
                self.selezioni[i]=0
            else:
                self.selezioni[i]=self.selezioni[i+1]
                print(str(i))
            if(self.selezioni[i]==1):
                stringa=str(i+1)
                self.Remove_edit.setText(stringa)
            if(self.selezioni[i]==2):
                stringa=str(i+1)
                self.Erosion_edit.setText(stringa)
            if(self.selezioni[i]==3):
                stringa=str(i+1)
                self.Dilation_edit.setText(stringa)
            if(self.selezioni[i]==4):
                stringa=str(i+1)
                self.Open_edit.setText(stringa)
            if(self.selezioni[i]==5):
                stringa=str(i+1)
                self.Close_edit.setText(stringa)
                print(i)
        self.valore=self.valore-1
    
    def delete_edit_remove(self):
        self.delete(self.Remove_edit)
        self.Remove_edit.clear()
        
    def delete_edit_erosion(self):
        self.delete(self.Erosion_edit)
        self.Erosion_edit.clear()
    
    def delete_edit_dilation(self):
        self.delete(self.Dilation_edit)
        self.Dilation_edit.clear()
    
    def delete_edit_open(self):
        self.delete(self.Open_edit)
        self.Open_edit.clear()
    
    def delete_edit_close(self):
        self.delete(self.Close_edit)
        self.Close_edit.clear()
    
    def add_change(self):
        self.Repeat_Red=False
        self.Repeat_Green=False
        self.Repeat_Blue=False
        self.apply_segmentation()        
    
    def clear_edit_label(self):
        self.valore=0
        self.selezioni=np.array([0,0,0,0,0])
        self.Remove_edit.clear()
        self.Erosion_edit.clear()
        self.Dilation_edit.clear()
        self.Open_edit.clear()
        self.Close_edit.clear()
        
    def set_all_mask(self):
        self.parent.set_image(self.parent.red_mask, self.parent.Red_QLabel, "red", mask=True)
        self.parent.set_image(self.parent.green_mask, self.parent.Green_QLabel, "green", mask=True)
        self.parent.set_image(self.parent.blue_mask, self.parent.Blue_QLabel, "blue", mask=True)
    
    def save(self):
        if((self.parent.red_mask is not None) and (self.parent.green_mask is not None) and (self.parent.blue_mask is not None)):
            self.Label_Save.setText("SAVED IMAGES! IF YOU WANT TO CHANGE THE IMAGES, REMEMBER TO CLEAR FILTRED LABEL")
            self.save_message()
        else:
            self.error_message("Attention: the images haven't been binarized")
    
    def Clear_filtred_label(self):
        if (self.local_red_mask is not None):
            self.parent.red_mask = self.local_red_mask
        if (self.local_green_mask is not None):
            self.parent.green_mask = self.local_green_mask
        if (self.local_blue_mask is not None):
            self.parent.blue_mask = self.local_blue_mask
        self.Filtred_Label.clear()
        self.Filtred_Label1.clear()
        self.Filtred_Label2.clear()
        self.clear_edit_label()
    
    def error_message(self, text_error):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(text_error)
        msg.setWindowTitle("Error")
        msg.exec_()
    
    def save_message(self):
        mbox = QMessageBox(self)
        mbox.setIcon(QMessageBox.Question)
        mbox.setWindowTitle("Save Dialog")
        mbox.setText("Document has been modified!")
        mbox.setInformativeText("Do you want to save your changes?")
        mbox.setDetailedText("Click on Save button to save changes.")
        mbox.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        returnValue = mbox.exec()
        if returnValue == QMessageBox.Save:
            if(self.mask_red is not None):
                self.local_red_mask= self.parent.red_mask
                self.parent.red_mask = self.mask_red
            if(self.mask_green is not None):
                self.local_green_mask= self.parent.green_mask
                self.parent.green_mask = self.mask_green
            if(self.mask_blue is not None):
                self.local_blue_mask= self.parent.blue_mask
                self.parent.blue_mask = self.mask_blue
            self.set_all_mask()
        else:
            pass
    
    def remove_message(self):
        mbox = QMessageBox(self)
        mbox.setIcon(QMessageBox.Question)
        mbox.setWindowTitle("Remove Help")
        mbox.setText("What does it?")
        mbox.setInformativeText("Remove objects smaller than the specified size.")
        mbox.exec_()
    
    def dilation_message(self):
        mbox = QMessageBox(self)
        mbox.setIcon(QMessageBox.Question)
        mbox.setWindowTitle("Dilation Help")
        mbox.setText("What does it?")
        mbox.setInformativeText("Dilation enlarges bright regions and shrinks dark regions.")
        mbox.exec_()
    
    def erosion_message(self):
        mbox = QMessageBox(self)
        mbox.setIcon(QMessageBox.Question)
        mbox.setWindowTitle("Erosion Help")
        mbox.setText("What does it?")
        mbox.setInformativeText("Erosion shrinks bright regions and enlarges dark regions.")
        mbox.exec_()
    
    def open_message(self):
        mbox = QMessageBox(self)
        mbox.setIcon(QMessageBox.Question)
        mbox.setWindowTitle("Opening Help")
        mbox.setText("What does it?")
        mbox.setInformativeText("The morphological opening on an image is defined as an erosion followed by a dilation. Opening can remove small bright spots (i.e. “salt”) and connect small dark cracks. This tends to “open” up (dark) gaps between (bright) features")
        mbox.exec_()
    
    def close_message(self):
        mbox = QMessageBox(self)
        mbox.setIcon(QMessageBox.Question)
        mbox.setWindowTitle("Closing Help")
        mbox.setText("What does it?")
        mbox.setInformativeText("The morphological closing on an image is defined as a dilation followed by an erosion. Closing can remove small dark spots (i.e. “pepper”) and connect small bright cracks. This tends to “close” up (dark) gaps between (bright) features.")
        mbox.exec_()
    
        
    def applyShadow(self):
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QtGui.QColor(209, 209, 209))
        return shadow