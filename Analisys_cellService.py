import os
import sys
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QColor, QImage, QPixmap, QKeySequence
import numpy as np
import skimage
import skimage.io
from skimage import exposure
import skimage.morphology
from skimage import filters
from scipy import ndimage
from scipy.ndimage import label, generate_binary_structure

class Ui_Analisys_cellService(QMainWindow):
        
    def __init__(self, parent):
        super().__init__()
        
        self.parameter = None
        
        self.parent = parent
        
        self.setupUi()
        
        self.set_biologicalWidget()
        
        self.set_overlapWidget()
        
        self.set_numberIslands()
        
        self.set_intensityWidget()
        
        self.statusBar()
        
        self.set_all_images()
        
        self.image_None()
        
        if self.parent.red_mask is not None:
            self.image_size(self.parent.red_mask)
        elif self.parent.green_mask is not None:
            self.image_size(self.parent.green_mask)
        elif self.parent.blue_mask is not None:
            self.image_size(self.parent.blue_mask)
            
        self.setWindowIcon(QtGui.QIcon(self.parent.resource_path('Icon/CellService_icon.ico')))
    
    def setupUi(self):
        # set the window's style
        self.setObjectName("Analisys_cellService")
        self.setFixedSize(1129, 690)
        self.setWindowTitle("Analisys")
        
        # set principa widget's style
        self.principal_widget = QtWidgets.QWidget()
        self.principal_widget.setStyleSheet("background-color: rgb(244, 244, 244)")
        self.principal_widget.setObjectName("principal_widget")
        
        # set grid layout
        self.gridLayoutWidget = QtWidgets.QWidget(self.principal_widget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(240, 20, 651, 651))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        
        # set principal layout
        self.principal_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.principal_layout.setContentsMargins(0, 0, 0, 0)
        self.principal_layout.setObjectName("principal_layout")
        
        # set RGB Label and add the label to grid layout
        self.RGB_Label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.RGB_Label.setTabletTracking(True)
        self.RGB_Label.setStyleSheet("border: 2px solid black")
        self.RGB_Label.setFrameShape(QtWidgets.QFrame.Panel)
        self.RGB_Label.setLineWidth(2)
        self.RGB_Label.setFixedSize(315,315)
        self.RGB_Label.setText("")
        self.RGB_Label.setScaledContents(True)
        self.RGB_Label.setObjectName("RGB_Label")
        self.principal_layout.addWidget(self.RGB_Label, 1, 1, 1, 1)
        
        # set BLUE Label and add the label to grid layout
        self.BLUE_Label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.BLUE_Label.setStyleSheet("border: 2px solid blue")
        self.BLUE_Label.setText("")
        self.BLUE_Label.setFixedSize(315,315)
        self.BLUE_Label.setScaledContents(True)
        self.BLUE_Label.setObjectName("BLUE_Label")
        self.principal_layout.addWidget(self.BLUE_Label, 1, 0, 1, 1)
        
        # set GREEN Label and add the label to grid layout
        self.GREEN_Label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.GREEN_Label.setStyleSheet("border: 2px solid green")
        self.GREEN_Label.setText("")
        self.GREEN_Label.setFixedSize(315,315)
        self.GREEN_Label.setScaledContents(True)
        self.GREEN_Label.setObjectName("GREEN_Label")
        self.principal_layout.addWidget(self.GREEN_Label, 0, 1, 1, 1)
        
        # set RED Label and add the label to grid layout
        self.RED_Label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.RED_Label.setStyleSheet("border: 2px solid red")
        self.RED_Label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.RED_Label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.RED_Label.setFixedSize(315,315)
        self.RED_Label.setLineWidth(2)
        self.RED_Label.setText("")
        self.RED_Label.setScaledContents(True)
        self.RED_Label.setObjectName("RED_Label")
        self.principal_layout.addWidget(self.RED_Label, 0, 0, 1, 1)
        
        self.canc_image_button = QtWidgets.QPushButton(self.principal_widget)
        self.canc_image_button.setGeometry(QtCore.QRect(920, 20, 41, 41))
        self.canc_image_button.setMouseTracking(True)
        self.canc_image_button.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canc_image_button.setToolTipDuration(-1)
        self.canc_image_button.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 10px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}" "\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}\n"
            "")
        self.canc_image_button.setText("")
        icon14 = QtGui.QIcon(self.parent.resource_path("Icon/canc icon.png"))
        #icon14.addPixmap(QtGui.QPixmap("canc icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.canc_image_button.setIcon(icon14)
        self.canc_image_button.setIconSize(QtCore.QSize(35, 40))
        self.canc_image_button.setObjectName("canc_image_button")
        self.canc_image_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Clear all (Ctrl+Del)</span></p></body></html>")
        self.canc_image_button.setStatusTip("Clear all (Ctrl+Del)")
        self.canc_image_button.clicked.connect(self.save_message)
        self.canc_image_button.setGraphicsEffect(self.applyShadow())
        self.ctrl_canc = QtWidgets.QShortcut(QKeySequence('Ctrl+Delete'), self)
        self.ctrl_canc.activated.connect(self.save_message)
        
        self.help_button = QtWidgets.QPushButton(self.principal_widget)
        self.help_button.setGeometry(QtCore.QRect(990, 20, 41, 41))
        self.help_button.setMouseTracking(True)
        self.help_button.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.help_button.setToolTipDuration(-1)
        self.help_button.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 10px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}" "\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}\n"
            "")
        self.help_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Help </span></p></body></html>")
        self.help_button.setStatusTip("Help")
        self.help_button.setText("")
        icon15 = QtGui.QIcon(self.parent.resource_path("Icon/help.png"))
        #icon15.addPixmap(QtGui.QPixmap("help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.help_button.setIcon(icon15)
        self.help_button.setIconSize(QtCore.QSize(35, 35))
        self.help_button.setObjectName("help_button")
        self.help_button.setGraphicsEffect(self.applyShadow())
        self.help_button.clicked.connect(self.help_message)
        #self.ctrl_help = QtWidgets.QShortcut(QKeySequence('Ctrl+Delete'), self)
        #self.ctrl_help.activated.connect(self.clearAll)
        
        self.label = QtWidgets.QLabel(self.principal_widget)
        self.label.setGeometry(QtCore.QRect(10, 20, 191, 16))
        self.label.setObjectName("label")
        self.label.setText("Image size: ")
        self.maximize_window()
        
    def set_biologicalWidget(self):
        self.biological_widget = QtWidgets.QWidget(self.principal_widget)
        self.biological_widget.setGeometry(QtCore.QRect(20, 400, 200, 261))
        self.biological_widget.setStyleSheet("background-color: rgb(255, 255, 255);\n" "border-radius: 35px;")
        self.biological_widget.setObjectName("biological_widget")
        self.biological_widget.setGraphicsEffect(self.applyShadow())
        self.red_buttonBC = QtWidgets.QPushButton(self.biological_widget)
        self.red_buttonBC.setGeometry(QtCore.QRect(10, 60, 41, 41))
        self.red_buttonBC.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.red_buttonBC.setStyleSheet("QPushButton {\n"
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
        self.red_buttonBC.clicked.connect(self.set_biologicalRED)
        self.red_buttonBC.setGraphicsEffect(self.applyShadow())
        self.red_buttonBC.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">RED image density</span></p></body></html>")
        self.red_buttonBC.setStatusTip("RED image density")
        self.red_buttonBC.setText("")
        icon = QtGui.QIcon(self.parent.resource_path("Icon/icon bio.png"))
        #icon.addPixmap(QtGui.QPixmap("icon bio.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.red_buttonBC.setIcon(icon)
        self.red_buttonBC.setIconSize(QtCore.QSize(60, 45))
        self.red_buttonBC.setObjectName("red_buttonBC")
        self.green_buttonBC = QtWidgets.QPushButton(self.biological_widget)
        self.green_buttonBC.setGeometry(QtCore.QRect(10, 130, 41, 41))
        self.green_buttonBC.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.green_buttonBC.setStyleSheet("QPushButton {\n"
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
        self.green_buttonBC.clicked.connect(self.set_biologicalGREEN)
        self.green_buttonBC.setGraphicsEffect(self.applyShadow())
        self.green_buttonBC.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">GREEN image density</span></p></body></html>")
        self.green_buttonBC.setStatusTip("GREEN image density")
        self.green_buttonBC.setText("")
        icon1 = QtGui.QIcon(self.parent.resource_path("Icon/icon bio 3.png"))
        #icon1.addPixmap(QtGui.QPixmap("icon bio 3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.green_buttonBC.setIcon(icon1)
        self.green_buttonBC.setIconSize(QtCore.QSize(60, 45))
        self.green_buttonBC.setObjectName("green_buttonBC")
        self.blue_buttonBC = QtWidgets.QPushButton(self.biological_widget)
        self.blue_buttonBC.setGeometry(QtCore.QRect(10, 200, 41, 41))
        self.blue_buttonBC.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.blue_buttonBC.setStyleSheet("QPushButton {\n"
            "    background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.blue_buttonBC.clicked.connect(self.set_biologicalBLUE)
        self.blue_buttonBC.setGraphicsEffect(self.applyShadow())
        self.blue_buttonBC.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">BLUE image density</span></p></body></html>")
        self.blue_buttonBC.setStatusTip("BLUE image biological density")
        self.blue_buttonBC.setText("")
        icon2 = QtGui.QIcon(self.parent.resource_path("Icon/icon bio 2.png"))
        #icon2.addPixmap(QtGui.QPixmap("icon bio 2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.blue_buttonBC.setIcon(icon2)
        self.blue_buttonBC.setIconSize(QtCore.QSize(60, 45))
        self.blue_buttonBC.setObjectName("blue_buttonBC")
        self.Red_PercentBC_edit = QtWidgets.QLineEdit(self.biological_widget)
        self.Red_PercentBC_edit.setGeometry(QtCore.QRect(55, 70, 130, 31))
        self.Red_PercentBC_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 9pt \"Arial\";\n"
            "color: rgb(255, 255, 255);")
        self.Red_PercentBC_edit.setAlignment(QtCore.Qt.AlignCenter) 
        self.Red_PercentBC_edit.setReadOnly(True)
        self.Red_PercentBC_edit.setObjectName("Red_PercentBC_edit")
        self.Blue_PercentBC_edit = QtWidgets.QLineEdit(self.biological_widget)
        self.Blue_PercentBC_edit.setGeometry(QtCore.QRect(55, 210, 130, 31))
        self.Blue_PercentBC_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 9pt \"Arial\";\n"
            "color: rgb(255, 255, 255);")
        self.Blue_PercentBC_edit.setReadOnly(True)
        self.Blue_PercentBC_edit.setAlignment(QtCore.Qt.AlignCenter) 
        self.Blue_PercentBC_edit.setObjectName("Blue_PercentBC_edit")
        self.compensate_edit2 = QtWidgets.QLineEdit(self.biological_widget)
        self.compensate_edit2.setGeometry(QtCore.QRect(0, 20, 200, 16))
        self.compensate_edit2.setStyleSheet("background-color: rgb(19, 82, 255);\n"
            "\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 14pt \"Arial\" bold;\n"
            "color: rgb(255, 255, 255);")
        self.compensate_edit2.setText("")
        self.compensate_edit2.setReadOnly(True)
        self.compensate_edit2.setObjectName("compensate_edit2")
        self.red_biological_title = QtWidgets.QLineEdit(self.biological_widget)
        self.red_biological_title.setGeometry(QtCore.QRect(55, 50, 135, 20))
        self.red_biological_title.setStyleSheet("font: 9pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.red_biological_title.setReadOnly(True)
        self.red_biological_title.setObjectName("red_biological_title")
        self.red_biological_title.setText("Red biological density")
        self.blue_biological_title = QtWidgets.QLineEdit(self.biological_widget)
        self.blue_biological_title.setGeometry(QtCore.QRect(55, 190, 135, 20))
        self.blue_biological_title.setStyleSheet("font: 9pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.blue_biological_title.setReadOnly(True)
        self.blue_biological_title.setObjectName("blue_biological_title")
        self.blue_biological_title.setText("Blue biological density")
        self.Green_PercentBC_edit = QtWidgets.QLineEdit(self.biological_widget)
        self.Green_PercentBC_edit.setGeometry(QtCore.QRect(55, 140, 130, 31))
        self.Green_PercentBC_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 9pt \"Arial\";\n"
            "color: rgb(255, 255, 255);")
        self.Green_PercentBC_edit.setText("")
        self.Green_PercentBC_edit.setAlignment(QtCore.Qt.AlignCenter) 
        self.Green_PercentBC_edit.setReadOnly(True)
        self.Green_PercentBC_edit.setObjectName("Green_PercentBC_edit")
        self.green_biological_title = QtWidgets.QLineEdit(self.biological_widget)
        self.green_biological_title.setGeometry(QtCore.QRect(55, 120, 142, 20))
        self.green_biological_title.setStyleSheet("font: 9pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.green_biological_title.setReadOnly(True)
        self.green_biological_title.setObjectName("green_biological_title")
        self.green_biological_title.setText("Green biological density")
        self.biological_edit = QtWidgets.QLineEdit(self.biological_widget)
        self.biological_edit.setGeometry(QtCore.QRect(0, 0, 200, 31))
        self.biological_edit.setStyleSheet("background-color: rgb(19, 82, 255);\n"
            "border-radius:15px;\n"
            "    font: bold 10px;\n"
            "    padding: 6px;\n"
            "font: 14pt \"Arial\";\n"
            "color: rgb(255, 255, 255);")
        self.biological_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.biological_edit.setReadOnly(True)
        self.biological_edit.setObjectName("biological_edit")
        self.biological_edit.setText("Density")
        self.maximize_biologicalWidget()
    
    def set_overlapWidget(self):
        self.similarity_widget = QtWidgets.QWidget(self.principal_widget)
        
        self.similarity_widget.setStyleSheet("background-color: rgb(255, 255, 255);\n" "border-radius: 35px;")
        self.similarity_widget.setGraphicsEffect(self.applyShadow())
        self.similarity_widget.setObjectName("similarity_widget")
        self.red_blue_buttonS = QtWidgets.QPushButton(self.similarity_widget)
        self.red_blue_buttonS.setMouseTracking(True)
        self.red_blue_buttonS.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.red_blue_buttonS.setToolTipDuration(-1)
        self.red_blue_buttonS.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}\n"
            "")
        self.red_blue_buttonS.clicked.connect(self.similarity_buttonRB)
        self.red_blue_buttonS.setGraphicsEffect(self.applyShadow())
        self.red_blue_buttonS.setText("")
        icon3 = QtGui.QIcon(self.parent.resource_path("Icon/icon 1.png"))
        #icon3.addPixmap(QtGui.QPixmap("icon 1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.red_blue_buttonS.setIcon(icon3)
        self.red_blue_buttonS.setObjectName("red_blue_buttonS")
        self.red_blue_buttonS.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">RED and BLUE intersect</span></p></body></html>")
        self.red_blue_buttonS.setStatusTip("RED and BLUE intersect")
        self.red_green_buttonS = QtWidgets.QPushButton(self.similarity_widget)
        self.red_green_buttonS.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.red_green_buttonS.setToolTipDuration(-1)
        self.red_green_buttonS.setStyleSheet("QPushButton {\n"
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
        self.red_green_buttonS.clicked.connect(self.similarity_buttonRG)
        self.red_green_buttonS.setGraphicsEffect(self.applyShadow())
        self.red_green_buttonS.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">RED and GREEN intersect</span></p></body></html>")
        self.red_green_buttonS.setStatusTip("RED and GREEN intersect")
        self.red_green_buttonS.setText("")
        icon4 = QtGui.QIcon(self.parent.resource_path("Icon/icon 2.png"))
        #icon4.addPixmap(QtGui.QPixmap("icon 2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.red_green_buttonS.setIcon(icon4)
        self.red_green_buttonS.setObjectName("red_green_buttonS")
        self.blue_green_buttonS = QtWidgets.QPushButton(self.similarity_widget)
        
        self.red_blue_buttonS.setIconSize(QtCore.QSize(60, 35))
        self.red_green_buttonS.setIconSize(QtCore.QSize(60, 35))
    
        self.blue_green_buttonS.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.blue_green_buttonS.setStyleSheet("QPushButton {\n"
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
            "    border-style: inset;\n"
            "}")
        self.blue_green_buttonS.clicked.connect(self.similarity_buttonGB)
        self.blue_green_buttonS.setGraphicsEffect(self.applyShadow())
        self.blue_green_buttonS.setText("")
        icon5 = QtGui.QIcon(self.parent.resource_path("Icon/icon 3.png"))
        #icon5.addPixmap(QtGui.QPixmap("icon 3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.blue_green_buttonS.setIcon(icon5)
        self.blue_green_buttonS.setIconSize(QtCore.QSize(60, 35))
        self.blue_green_buttonS.setObjectName("blue_green_buttonS")
        self.blue_green_buttonS.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">GREEN and BLUE intersect</span></p></body></html>")
        self.blue_green_buttonS.setStatusTip("GREEN and BLUE intersect")
        self.total_buttonS = QtWidgets.QPushButton(self.similarity_widget)
        self.total_buttonS.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.total_buttonS.setStyleSheet("QPushButton {\n"
            "    background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton::hover {\n"
            "    background-color: rgb(204, 204, 204);\n"
            "}"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.total_buttonS.clicked.connect(self.similarity_buttonRGB)
        self.total_buttonS.setGraphicsEffect(self.applyShadow())
        self.total_buttonS.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">RED, GREEN and BLUE intersect</span></p></body></html>")
        self.total_buttonS.setStatusTip("RED, GREEN and BLUE intersect")
        self.total_buttonS.setText("")
        icon6 = QtGui.QIcon(self.parent.resource_path("Icon/icon 4 grey.png"))
        #icon6.addPixmap(QtGui.QPixmap("icon 4 grey.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.total_buttonS.setIcon(icon6)
        self.total_buttonS.setIconSize(QtCore.QSize(60, 35))
        self.total_buttonS.setObjectName("total_buttonS")
        self.RB_PercentS_edit = QtWidgets.QLineEdit(self.similarity_widget)
        self.RB_PercentS_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 9pt \"Arial\";\n"
            "color: rgb(255, 255, 255);")
        self.RB_PercentS_edit.setText("")
        self.RB_PercentS_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.RB_PercentS_edit.setReadOnly(True)
        self.RB_PercentS_edit.setObjectName("RB_PercentS_edit")
        self.RG_PercentS_edit = QtWidgets.QLineEdit(self.similarity_widget)
        self.RG_PercentS_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 9pt \"Arial\";\n"
            "color: rgb(255, 255, 255);")
        self.RG_PercentS_edit.setReadOnly(True)
        self.RG_PercentS_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.RG_PercentS_edit.setObjectName("RG_PercentS_edit")
        self.BG_PercentS_edit = QtWidgets.QLineEdit(self.similarity_widget)
        self.BG_PercentS_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 9pt \"Arial\";\n"
            "color: rgb(255, 255, 255);")
        self.BG_PercentS_edit.setReadOnly(True)
        self.BG_PercentS_edit.setObjectName("BG_PercentS_edit")
        self.BG_PercentS_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.RGB_PercentS_edit = QtWidgets.QLineEdit(self.similarity_widget)
        self.RGB_PercentS_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 9pt \"Arial\";\n"
            "color: rgb(255, 255, 255);")
        self.RGB_PercentS_edit.setReadOnly(True)
        self.RGB_PercentS_edit.setObjectName("RGB_PercentS_edit")
        self.RGB_PercentS_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.compensate_edit = QtWidgets.QLineEdit(self.similarity_widget)
        self.compensate_edit.setStyleSheet("background-color: rgb(19, 82, 255);\n"
            "\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 14pt \"Varela\" bold;\n"
            "color: rgb(255, 255, 255);")
        self.compensate_edit.setText("")
        self.compensate_edit.setReadOnly(True)
        self.compensate_edit.setObjectName("compensate_edit")
        self.similarity_edit = QtWidgets.QLineEdit(self.similarity_widget)
        self.similarity_edit.setStyleSheet("background-color: rgb(19, 82, 255);\n"
            "border-radius:15px;\n"
            "    padding: 6px;\n"
            "font: 14pt \"Arial\";\n"
            "color: rgb(255, 255, 255);")
        self.similarity_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.similarity_edit.setReadOnly(True)
        self.similarity_edit.setObjectName("similarity_edit")
        self.similarity_edit.setText("Intersect")
        self.redBlue_overlap_title = QtWidgets.QLineEdit(self.similarity_widget)
        self.redBlue_overlap_title.setStyleSheet("font: 9pt \"Arial\";\n"
"color: rgb(19, 82, 255);")
        self.redBlue_overlap_title.setReadOnly(True)
        self.redBlue_overlap_title.setObjectName("redBlue_overlap_title")
        self.redBlue_overlap_title.setText("Blue-red intersect")
        self.redGreen_overlap_title = QtWidgets.QLineEdit(self.similarity_widget)
        self.redGreen_overlap_title.setStyleSheet("font: 9pt \"Arial\";\n"
"color: rgb(19, 82, 255);")
        self.redGreen_overlap_title.setReadOnly(True)
        self.redGreen_overlap_title.setObjectName("redGreen_overlap_title")
        self.redGreen_overlap_title.setText("Red-green intersect")
        self.blueGreen_overlap_title = QtWidgets.QLineEdit(self.similarity_widget)
        self.blueGreen_overlap_title.setStyleSheet("font: 9pt \"Arial\";\n"
"color: rgb(19, 82, 255);")
        self.blueGreen_overlap_title.setReadOnly(True)
        self.blueGreen_overlap_title.setObjectName("blueGreen_overlap_title")
        self.blueGreen_overlap_title.setText("Green-blue intersect")
        self.all_overlap_title = QtWidgets.QLineEdit(self.similarity_widget)
        self.all_overlap_title.setStyleSheet("font: 9pt \"Arial\";\n"
"color: rgb(19, 82, 255);")
        self.all_overlap_title.setReadOnly(True)
        self.all_overlap_title.setObjectName("all_overlap_title")
        self.all_overlap_title.setText("All images intersect")
        
        self.red_green_buttonS.setGeometry(QtCore.QRect(10, 130, 41, 41))
        self.similarity_widget.setGeometry(QtCore.QRect(20, 50, 200, 331))
        self.red_blue_buttonS.setGeometry(QtCore.QRect(10, 60, 41, 41))
        self.blue_green_buttonS.setGeometry(QtCore.QRect(10, 200, 41, 41))
        self.total_buttonS.setGeometry(QtCore.QRect(10, 270, 41, 41))
        self.RB_PercentS_edit.setGeometry(QtCore.QRect(55, 70, 130, 31))
        self.RG_PercentS_edit.setGeometry(QtCore.QRect(55, 140, 130, 31))
        self.BG_PercentS_edit.setGeometry(QtCore.QRect(55, 210, 130, 31))
        self.RGB_PercentS_edit.setGeometry(QtCore.QRect(55, 280, 130, 31))
        self.compensate_edit.setGeometry(QtCore.QRect(0, 20, 200, 16))
        self.similarity_edit.setGeometry(QtCore.QRect(0, 0, 200, 31))
        self.redBlue_overlap_title.setGeometry(QtCore.QRect(55, 50, 100, 20))
        self.redGreen_overlap_title.setGeometry(QtCore.QRect(55, 120, 120, 20))
        self.blueGreen_overlap_title.setGeometry(QtCore.QRect(55, 190, 120, 20))
        self.all_overlap_title.setGeometry(QtCore.QRect(55, 260, 120, 20))
        self.maximize_overlapWidget()
        
    def set_numberIslands(self):
        self.number_widget = QtWidgets.QWidget(self.principal_widget)
        self.number_widget.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 35px;")
        self.number_widget.setGraphicsEffect(self.applyShadow())
        self.number_widget.setObjectName("number_widget")
        self.number_button_red = QtWidgets.QPushButton(self.number_widget)
        self.number_button_red.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.number_button_red.setStyleSheet("QPushButton {\n"
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
        self.number_button_red.clicked.connect(self.set_number_RED)
        self.number_button_red.setGraphicsEffect(self.applyShadow())
        self.number_button_red.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Calculate the number of islands in the red image</span></p></body></html>")
        self.number_button_red.setStatusTip("Calculate the number of islands in the red image")
        self.number_button_red.setText("")
        icon7 = QtGui.QIcon(self.parent.resource_path("Icon/icon n 2.png"))
        #icon7.addPixmap(QtGui.QPixmap("icon n 2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.number_button_red.setIcon(icon7)
        self.number_button_red.setIconSize(QtCore.QSize(60, 45))
        self.number_button_red.setObjectName("number_button_red")
        self.number_button_green = QtWidgets.QPushButton(self.number_widget)
        self.number_button_green.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.number_button_green.setStyleSheet("QPushButton {\n"
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
        self.number_button_green.clicked.connect(self.set_number_GREEN)
        self.number_button_green.setGraphicsEffect(self.applyShadow())
        self.number_button_green.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Calculate the number of islands in the green image</span></p></body></html>")
        self.number_button_green.setStatusTip("Calculate the number of islands in the green image")
        self.number_button_green.setText("")
        icon8 = QtGui.QIcon(self.parent.resource_path("Icon/icon n 4.png"))
        #icon8.addPixmap(QtGui.QPixmap("icon n 4.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.number_button_green.setIcon(icon8)
        self.number_button_green.setIconSize(QtCore.QSize(60, 45))
        self.number_button_green.setObjectName("number_button_green")
        self.number_button_blue = QtWidgets.QPushButton(self.number_widget)
        self.number_button_blue.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.number_button_blue.setStyleSheet("QPushButton {\n"
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
            "    border-style: inset;\n"
            "}")
        self.number_button_blue.clicked.connect(self.set_number_BLUE)
        self.number_button_blue.setGraphicsEffect(self.applyShadow())
        self.number_button_blue.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Calculate the number of islands in the blue image</span></p></body></html>")
        self.number_button_blue.setStatusTip("Calculate the number of islands in the blue image")
        self.number_button_blue.setText("")
        icon9 = QtGui.QIcon(self.parent.resource_path("Icon/icon n 3.png"))
        #icon9.addPixmap(QtGui.QPixmap("icon n 3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.number_button_blue.setIcon(icon9)
        self.number_button_blue.setIconSize(QtCore.QSize(60, 45))
        self.number_button_blue.setObjectName("number_button_blue")
        self.Red_number_edit = QtWidgets.QLineEdit(self.number_widget)
        self.Red_number_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 15px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 9pt \"Arial\";\n"
"color: rgb(255, 255, 255);")
        self.Red_number_edit.setReadOnly(True)
        self.Red_number_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.Red_number_edit.setObjectName("Red_number_edit")
        self.Blue_number_edit = QtWidgets.QLineEdit(self.number_widget)
        self.Blue_number_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 15px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 9pt \"Arial\";\n"
"color: rgb(255, 255, 255);")
        self.Blue_number_edit.setReadOnly(True)
        self.Blue_number_edit.setObjectName("Blue_number_edit")
        self.Blue_number_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.compensate_edit2_2 = QtWidgets.QLineEdit(self.number_widget)
        self.compensate_edit2_2.setStyleSheet("background-color: rgb(19, 82, 255);\n"
"\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 14pt \"Varela\" bold;\n"
"color: rgb(255, 255, 255);")
        self.compensate_edit2_2.setText("")
        self.compensate_edit2_2.setReadOnly(True)
        self.compensate_edit2_2.setObjectName("compensate_edit2_2")
        self.number_edit = QtWidgets.QLineEdit(self.number_widget)
        self.number_edit.setStyleSheet("background-color: rgb(19, 82, 255);\n"
"border-radius:15px;\n"
"    padding: 6px;\n"
"font: 13pt \"Arial\";\n"
"color: rgb(255, 255, 255);")
        self.number_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.number_edit.setReadOnly(True)
        self.number_edit.setObjectName("number_edit")
        self.number_edit.setText("Number of islands")
        self.red_number_title = QtWidgets.QLineEdit(self.number_widget)
        
        self.red_number_title.setStyleSheet("font: 9pt \"Arial\";\n"
"color: rgb(19, 82, 255);")
        self.red_number_title.setReadOnly(True)
        self.red_number_title.setObjectName("red_number_title")
        self.red_number_title.setText("Red numbers of islands")
        self.blue_number_title = QtWidgets.QLineEdit(self.number_widget)
        self.blue_number_title.setStyleSheet("font: 9pt \"Arial\";\n"
"color: rgb(19, 82, 255);")
        self.blue_number_title.setReadOnly(True)
        self.blue_number_title.setObjectName("blue_number_title")
        self.blue_number_title.setText("Blue number of islands")
        self.Green_number_edit = QtWidgets.QLineEdit(self.number_widget)
        
        self.Green_number_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 15px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 9pt \"Arial\";\n"
"color: rgb(255, 255, 255);")
        self.Green_number_edit.setText("")
        self.Green_number_edit.setReadOnly(True)
        self.Green_number_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.Green_number_edit.setObjectName("Green_number_edit")
        self.green_number_title = QtWidgets.QLineEdit(self.number_widget)
        
        self.green_number_title.setStyleSheet("font: 9pt \"Arial\";\n"
"color: rgb(19, 82, 255);")
        self.green_number_title.setReadOnly(True)
        self.green_number_title.setObjectName("green_number_title")
        self.green_number_title.setText("Green numbers of islands")
        self.intensity_widget = QtWidgets.QWidget(self.principal_widget)
        
        if (self.parent.red_mask is not None):
            self.parent.red_mask=self.parent.red_mask.astype(np.uint8)
        if (self.parent.green_mask is not None):
            self.parent.green_mask=self.parent.green_mask.astype(np.uint8)
        if (self.parent.blue_mask is not None):
            self.parent.blue_mask=self.parent.blue_mask.astype(np.uint8)
        
        
        self.number_widget.setGeometry(QtCore.QRect(920, 90, 191, 261))
        self.number_button_red.setGeometry(QtCore.QRect(10, 60, 41, 41))
        self.number_button_green.setGeometry(QtCore.QRect(10, 130, 41, 41))
        self.number_button_blue.setGeometry(QtCore.QRect(10, 200, 41, 41))
        self.Red_number_edit.setGeometry(QtCore.QRect(60, 70, 100, 31))
        self.Blue_number_edit.setGeometry(QtCore.QRect(60, 210, 100, 31))
        self.compensate_edit2_2.setGeometry(QtCore.QRect(0, 20, 191, 16))
        self.number_edit.setGeometry(QtCore.QRect(0, 0, 191, 31))
        self.red_number_title.setGeometry(QtCore.QRect(50, 50, 140, 20))
        self.blue_number_title.setGeometry(QtCore.QRect(50, 190, 140, 20))
        self.Green_number_edit.setGeometry(QtCore.QRect(60, 140, 100, 31))
        self.green_number_title.setGeometry(QtCore.QRect(48, 120, 147, 20))
        self.maximize_numberIslands()
    
    def set_intensityWidget(self):
        self.intensity_widget.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 35px;")
        self.intensity_widget.setGraphicsEffect(self.applyShadow())
        self.intensity_widget.setObjectName("intensity_widget_2")
        self.intensity_button_red = QtWidgets.QPushButton(self.intensity_widget)
        self.intensity_button_red.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.intensity_button_red.setStyleSheet("QPushButton {\n"
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
        self.intensity_button_red.clicked.connect(self.set_min_max_intensityRED)
        self.intensity_button_red.setGraphicsEffect(self.applyShadow())
        self.intensity_button_red.setText("")
        icon10 = QtGui.QIcon(self.parent.resource_path("Icon/icon int 1.png"))
        #icon10.addPixmap(QtGui.QPixmap("icon int 1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.intensity_button_red.setIcon(icon10)
        self.intensity_button_red.setIconSize(QtCore.QSize(60, 45))
        self.intensity_button_red.setObjectName("intensity_button_red")
        self.intensity_button_red.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">RED image min and max intensity</span></p></body></html>")
        self.intensity_button_red.setStatusTip("RED image min and max intensity")
        self.intensity_button_green = QtWidgets.QPushButton(self.intensity_widget)
        self.intensity_button_green.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.intensity_button_green.setStyleSheet("QPushButton {\n"
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
        self.intensity_button_green.clicked.connect(self.set_min_max_intensityGREEN)
        self.intensity_button_green.setGraphicsEffect(self.applyShadow())
        self.intensity_button_green.setText("")
        icon11 = QtGui.QIcon(self.parent.resource_path("Icon/icon int 3.png"))
        #icon11.addPixmap(QtGui.QPixmap("icon int 3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.intensity_button_green.setIcon(icon11)
        self.intensity_button_green.setIconSize(QtCore.QSize(60, 45))
        self.intensity_button_green.setObjectName("intensity_button_green")
        self.intensity_button_green.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">GREEN image min and max intensity</span></p></body></html>")
        self.intensity_button_green.setStatusTip("GREEN image min and max intensity")
        self.intensity_button_blue = QtWidgets.QPushButton(self.intensity_widget)
        self.intensity_button_blue.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.intensity_button_blue.setStyleSheet("QPushButton {\n"
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
        self.intensity_button_blue.clicked.connect(self.set_min_max_intensityBLUE)
        self.intensity_button_blue.setGraphicsEffect(self.applyShadow())
        self.intensity_button_blue.setText("")
        icon12 = QtGui.QIcon(self.parent.resource_path("Icon/icon int 2.png"))
        #icon12.addPixmap(QtGui.QPixmap("icon int 2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.intensity_button_blue.setIcon(icon12)
        self.intensity_button_blue.setIconSize(QtCore.QSize(60, 45))
        self.intensity_button_blue.setObjectName("intensity_button_blue")
        self.intensity_button_blue.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">BLUE image min and max intensity</span></p></body></html>")
        self.intensity_button_blue.setStatusTip("BLUE image min and max intensity")
        
        self.Red_intensity_edit_min = QtWidgets.QLineEdit(self.intensity_widget)
        self.Red_intensity_edit_min.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 15px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 8.5pt \"Arial\";\n"
"color: rgb(255, 255, 255);")
        self.Red_intensity_edit_min.setReadOnly(True)
        self.Red_intensity_edit_min.setObjectName("Red_intensity_edit_min")
        self.Red_intensity_edit_min.setAlignment(QtCore.Qt.AlignCenter)
        
        self.Blue_intensity_edit_min = QtWidgets.QLineEdit(self.intensity_widget)
        self.Blue_intensity_edit_min.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 15px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 8.5pt \"Arial\";\n"
"color: rgb(255, 255, 255);")
        self.Blue_intensity_edit_min.setReadOnly(True)
        self.Blue_intensity_edit_min.setObjectName("Blue_intensity_edit_min")
        self.Blue_intensity_edit_min.setAlignment(QtCore.Qt.AlignCenter)
        
        self.compensate_edit2_3 = QtWidgets.QLineEdit(self.intensity_widget)
        self.compensate_edit2_3.setStyleSheet("background-color: rgb(19, 82, 255);\n"
"\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 14pt \"Varela\" bold;\n"
"color: rgb(255, 255, 255);")
        self.compensate_edit2_3.setText("")
        self.compensate_edit2_3.setReadOnly(True)
        self.compensate_edit2_3.setObjectName("compensate_edit2_3")
        self.intensity_edit = QtWidgets.QLineEdit(self.intensity_widget)
        self.intensity_edit.setStyleSheet("background-color: rgb(19, 82, 255);\n"
"border-radius:15px;\n"
"    padding: 6px;\n"
"font: 14pt \"Arial\";\n"
"color: rgb(255, 255, 255);")
        self.intensity_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.intensity_edit.setReadOnly(True)
        self.intensity_edit.setObjectName("intensity_edit")
        self.intensity_edit.setText("Intensity (no mask)")
        self.intensity_red_title = QtWidgets.QLineEdit(self.intensity_widget)
        
        self.intensity_red_title.setText("Red intensity")
        self.intensity_red_title.setStyleSheet("font: 9pt \"Arial\";\n"
"color: rgb(19, 82, 255);")
        self.intensity_red_title.setReadOnly(True)
        self.intensity_red_title.setObjectName("intensity_red_title")
        self.intensity_blue_title = QtWidgets.QLineEdit(self.intensity_widget)
        self.intensity_blue_title.setStyleSheet("font: 9pt \"Arial\";\n"
"color: rgb(19, 82, 255);")
        self.intensity_blue_title.setReadOnly(True)
        self.intensity_blue_title.setObjectName("intensity_blue_title")
        self.intensity_blue_title.setText("Blue intensity")
        self.Green_intensity_edit_min = QtWidgets.QLineEdit(self.intensity_widget)
        self.Green_intensity_edit_min.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 15px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 8.5pt \"Arial\";\n"
"color: rgb(255, 255, 255);")
        self.Green_intensity_edit_min.setText("")
        self.Green_intensity_edit_min.setReadOnly(True)
        self.Green_intensity_edit_min.setObjectName("Green_intensity_edit_min")
        self.Green_intensity_edit_min.setAlignment(QtCore.Qt.AlignCenter)
        
        self.intensity_green_title = QtWidgets.QLineEdit(self.intensity_widget)
        self.intensity_green_title.setStyleSheet("font: 9pt \"Arial\";\n"
"color: rgb(19, 82, 255);")
        self.intensity_green_title.setReadOnly(True)
        self.intensity_green_title.setObjectName("intensity_green_title")
        self.intensity_green_title.setText("Green intensity")
        self.Red_intensity_edit_max = QtWidgets.QLineEdit(self.intensity_widget)
        self.Red_intensity_edit_max.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 15px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 8.5pt \"Arial\";\n"
"color: rgb(255, 255, 255);")
        self.Red_intensity_edit_max.setReadOnly(True)
        self.Red_intensity_edit_max.setObjectName("Red_intensity_edit_max")
        self.Red_intensity_edit_max.setAlignment(QtCore.Qt.AlignCenter)
        
        self.Green_intensity_edit_max = QtWidgets.QLineEdit(self.intensity_widget)
        self.Green_intensity_edit_max.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 15px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 8.5pt \"Arial\";\n"
"color: rgb(255, 255, 255);")
        self.Green_intensity_edit_max.setReadOnly(True)
        self.Green_intensity_edit_max.setObjectName("Green_intensity_edit_max")
        self.Green_intensity_edit_max.setAlignment(QtCore.Qt.AlignCenter)
        
        self.Blue_intensity_edit_max = QtWidgets.QLineEdit(self.intensity_widget)
        self.Blue_intensity_edit_max.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 15px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 8.5pt \"Arial\";\n"
"color: rgb(255, 255, 255);")
        self.Blue_intensity_edit_max.setReadOnly(True)
        self.Blue_intensity_edit_max.setObjectName("Blue_intensity_edit_max")
        self.Blue_intensity_edit_max.setAlignment(QtCore.Qt.AlignCenter)
        
        self.setCentralWidget(self.principal_widget)
        
        self.intensity_widget.setGeometry(QtCore.QRect(920, 400, 191, 261))
        self.intensity_button_red.setGeometry(QtCore.QRect(10, 60, 41, 41))
        self.intensity_button_green.setGeometry(QtCore.QRect(10, 130, 41, 41))
        self.intensity_button_blue.setGeometry(QtCore.QRect(10, 200, 41, 41))
        self.Red_intensity_edit_min.setGeometry(QtCore.QRect(60, 70, 61, 31))
        self.Blue_intensity_edit_min.setGeometry(QtCore.QRect(60, 210, 61, 31))
        self.compensate_edit2_3.setGeometry(QtCore.QRect(0, 20, 191, 16))
        self.intensity_edit.setGeometry(QtCore.QRect(0, 0, 191, 31))
        self.intensity_red_title.setGeometry(QtCore.QRect(75, 50, 80, 20))
        self.intensity_blue_title.setGeometry(QtCore.QRect(85, 190, 85, 20))
        self.Green_intensity_edit_min.setGeometry(QtCore.QRect(60, 140, 61, 31))
        self.intensity_green_title.setGeometry(QtCore.QRect(85, 120, 90, 20))
        self.Red_intensity_edit_max.setGeometry(QtCore.QRect(125, 70, 61, 31))
        self.Green_intensity_edit_max.setGeometry(QtCore.QRect(125, 140, 61, 31))
        self.Blue_intensity_edit_max.setGeometry(QtCore.QRect(125, 210, 61, 31))
        self.maximize_intensityWidget()
    
    def maximize_window(self):
        self.screen = QDesktopWidget().screenGeometry()
        if ((self.screen.height()*1.3)<=1920):
            screen_height=1076
        else:
            screen_height=1129/1.3
        self.setFixedSize(int(screen_height*1.3), int(screen_height*0.79))
        self.gridLayoutWidget.setGeometry(QtCore.QRect(screen_height*1.3*0.213, 20, screen_height*1.3*0.577, screen_height*1.3*0.577))
        self.RGB_Label.setFixedSize((screen_height*1.3*0.577/2)-10, (screen_height*1.3*0.577/2)-10)
        self.BLUE_Label.setFixedSize((screen_height*1.3*0.577/2)-10, (screen_height*1.3*0.577/2)-10)
        self.GREEN_Label.setFixedSize((screen_height*1.3*0.577/2)-10, (screen_height*1.3*0.577/2)-10)
        self.RED_Label.setFixedSize((screen_height*1.3*0.577/2)-10, (screen_height*1.3*0.577/2)-10)
        self.canc_image_button.setGeometry(QtCore.QRect(screen_height*1.3*0.815, screen_height*1.3*0.0177, screen_height*1.3*0.0363, screen_height*1.3*0.0363))
        self.help_button.setGeometry(QtCore.QRect(screen_height*1.3*0.8769, screen_height*1.3*0.0177, screen_height*1.3*0.0363, screen_height*1.3*0.0363))
        
    def maximize_biologicalWidget(self):
        if ((self.screen.height()*1.3)<=1920):
            screen_height=1076
        else:
            screen_height=1129/1.3
        self.biological_widget.setGeometry(QtCore.QRect(20, screen_height*1.3*0.35, screen_height*1.3*0.177, screen_height*1.3*0.23))
        self.compensate_edit2.setGeometry(QtCore.QRect(0, screen_height*1.3*0.0177, screen_height*1.3*0.177, screen_height*1.3*0.0142))
        self.biological_edit.setGeometry(QtCore.QRect(0, 0, screen_height*1.3*0.177, screen_height*1.3*0.02745))
        self.red_buttonBC.setGeometry(QtCore.QRect(10, screen_height*1.3*0.053, screen_height*1.3*0.0363, screen_height*1.3*0.0363))
        self.green_buttonBC.setGeometry(QtCore.QRect(10, screen_height*1.3*0.1151, screen_height*1.3*0.0363, screen_height*1.3*0.0363))
        self.blue_buttonBC.setGeometry(QtCore.QRect(10, screen_height*1.3*0.177, screen_height*1.3*0.0363, screen_height*1.3*0.0363))
        self.Red_PercentBC_edit.setGeometry(QtCore.QRect(screen_height*1.3*0.0487, screen_height*1.3*0.062, screen_height*1.3*0.115, screen_height*1.3*0.02745))
        self.Blue_PercentBC_edit.setGeometry(QtCore.QRect(screen_height*1.3*0.0487, screen_height*1.3*0.186, screen_height*1.3*0.115, screen_height*1.3*0.02745))
        self.red_biological_title.setGeometry(QtCore.QRect(screen_height*1.3*0.0487, screen_height*1.3*0.0443, screen_height*1.3*0.1196, screen_height*1.3*0.0177))
        self.blue_biological_title.setGeometry(QtCore.QRect(screen_height*1.3*0.0487, screen_height*1.3*0.1683, screen_height*1.3*0.1196, screen_height*1.3*0.0177))
        self.Green_PercentBC_edit.setGeometry(QtCore.QRect(screen_height*1.3*0.0487, screen_height*1.3*0.124, screen_height*1.3*0.115, screen_height*1.3*0.02745))
        self.green_biological_title.setGeometry(QtCore.QRect(screen_height*1.3*0.0487, screen_height*1.3*0.106, screen_height*1.3*0.1258, screen_height*1.3*0.0177))
    
    def maximize_overlapWidget(self):
        if ((self.screen.height()*1.3)<=1920):
            screen_height=1076
        else:
            screen_height=1129/1.3
        self.red_green_buttonS.setGeometry(QtCore.QRect(screen_height*1.3*0.00886, screen_height*1.3*0.115, screen_height*1.3*0.0363, screen_height*1.3*0.0363))
        self.similarity_widget.setGeometry(QtCore.QRect(screen_height*1.3*0.0177, screen_height*1.3*0.044, screen_height*1.3*0.177, screen_height*1.3*0.2932))
        self.red_blue_buttonS.setGeometry(QtCore.QRect(screen_height*1.3*0.00886, screen_height*1.3*0.053, screen_height*1.3*0.0363, screen_height*1.3*0.0363))
        self.blue_green_buttonS.setGeometry(QtCore.QRect(screen_height*1.3*0.00886, screen_height*1.3*0.177, screen_height*1.3*0.0363, screen_height*1.3*0.0363))
        self.total_buttonS.setGeometry(QtCore.QRect(screen_height*1.3*0.00886, screen_height*1.3*0.239, screen_height*1.3*0.0363, screen_height*1.3*0.0363))
        self.RB_PercentS_edit.setGeometry(QtCore.QRect(screen_height*1.3*0.0487, screen_height*1.3*0.062, screen_height*1.3*0.115, screen_height*1.3*0.0275))
        self.RG_PercentS_edit.setGeometry(QtCore.QRect(screen_height*1.3*0.0487, screen_height*1.3*0.124, screen_height*1.3*0.115, screen_height*1.3*0.0275))
        self.BG_PercentS_edit.setGeometry(QtCore.QRect(screen_height*1.3*0.0487, screen_height*1.3*0.186, screen_height*1.3*0.115, screen_height*1.3*0.0275))
        self.RGB_PercentS_edit.setGeometry(QtCore.QRect(screen_height*1.3*0.0487, screen_height*1.3*0.248, screen_height*1.3*0.115, screen_height*1.3*0.0275))
        self.compensate_edit.setGeometry(QtCore.QRect(0, screen_height*1.3*0.0177, screen_height*1.3*0.177, screen_height*1.3*0.0142))
        self.similarity_edit.setGeometry(QtCore.QRect(0, 0, screen_height*1.3*0.177, screen_height*1.3*0.0275))
        self.redBlue_overlap_title.setGeometry(QtCore.QRect(screen_height*1.3*0.0487, screen_height*1.3*0.044, screen_height*1.3*0.0886, screen_height*1.3*0.0177))
        self.redGreen_overlap_title.setGeometry(QtCore.QRect(screen_height*1.3*0.0487, screen_height*1.3*0.1063, screen_height*1.3*0.1063, screen_height*1.3*0.0177))
        self.blueGreen_overlap_title.setGeometry(QtCore.QRect(screen_height*1.3*0.0487, screen_height*1.3*0.1683, screen_height*1.3*0.1063, screen_height*1.3*0.0177))
        self.all_overlap_title.setGeometry(QtCore.QRect(screen_height*1.3*0.0487, screen_height*1.3*0.23, screen_height*1.3*0.1063, screen_height*1.3*0.0177))
    
    def maximize_numberIslands(self):
        if ((self.screen.height()*1.3)<=1920):
            screen_height=1076
        else:
            screen_height=1129/1.3
        self.number_widget.setGeometry(QtCore.QRect(screen_height*1.3*0.8149, screen_height*1.3*0.0797, screen_height*1.3*0.1692, screen_height*1.3*0.2312))
        self.number_button_red.setGeometry(QtCore.QRect(screen_height*1.3*0.0089, screen_height*1.3*0.053, screen_height*1.3*0.036, screen_height*1.3*0.036))
        self.number_button_green.setGeometry(QtCore.QRect(screen_height*1.3*0.0089, screen_height*1.3*0.115, screen_height*1.3*0.036, screen_height*1.3*0.036))
        self.number_button_blue.setGeometry(QtCore.QRect(screen_height*1.3*0.0089, screen_height*1.3*0.177, screen_height*1.3*0.036, screen_height*1.3*0.036))
        self.Red_number_edit.setGeometry(QtCore.QRect(screen_height*1.3*0.053, screen_height*1.3*0.062, screen_height*1.3*0.0886, screen_height*1.3*0.0275))
        self.Blue_number_edit.setGeometry(QtCore.QRect(screen_height*1.3*0.053, screen_height*1.3*0.186, screen_height*1.3*0.0886, screen_height*1.3*0.0275))
        self.compensate_edit2_2.setGeometry(QtCore.QRect(0, screen_height*1.3*0.0177, screen_height*1.3*0.1692, screen_height*1.3*0.0142))
        self.number_edit.setGeometry(QtCore.QRect(0, 0, screen_height*1.3*0.1692, screen_height*1.3*0.0275))
        self.red_number_title.setGeometry(QtCore.QRect(screen_height*1.3*0.0443, screen_height*1.3*0.0443, screen_height*1.3*0.124, screen_height*1.3*0.0177))
        self.blue_number_title.setGeometry(QtCore.QRect(screen_height*1.3*0.0443, screen_height*1.3*0.1683, screen_height*1.3*0.124, screen_height*1.3*0.0177))
        self.Green_number_edit.setGeometry(QtCore.QRect(screen_height*1.3*0.053, screen_height*1.3*0.124, screen_height*1.3*0.0886, screen_height*1.3*0.0275))
        self.green_number_title.setGeometry(QtCore.QRect(screen_height*1.3*0.043, screen_height*1.3*0.1063, screen_height*1.3*0.13, screen_height*1.3*0.0177))
    
    def maximize_intensityWidget(self):
        if ((self.screen.height()*1.3)<=1920):
            screen_height=1076
        else:
            screen_height=1129/1.3
        self.intensity_widget.setGeometry(QtCore.QRect(screen_height*1.3*0.8149, screen_height*1.3*0.3543, screen_height*1.3*0.1692, screen_height*1.3*0.2312))
        self.intensity_button_red.setGeometry(QtCore.QRect(screen_height*1.3*0.0089, screen_height*1.3*0.053, screen_height*1.3*0.0363, screen_height*1.3*0.0363))
        self.intensity_button_green.setGeometry(QtCore.QRect(screen_height*1.3*0.0089, screen_height*1.3*0.115, screen_height*1.3*0.0363, screen_height*1.3*0.0363))
        self.intensity_button_blue.setGeometry(QtCore.QRect(screen_height*1.3*0.0089, screen_height*1.3*0.177, screen_height*1.3*0.0363, screen_height*1.3*0.0363))
        self.Red_intensity_edit_min.setGeometry(QtCore.QRect(screen_height*1.3*0.053, screen_height*1.3*0.062, screen_height*1.3*0.054, screen_height*1.3*0.0275))
        self.Blue_intensity_edit_min.setGeometry(QtCore.QRect(screen_height*1.3*0.053, screen_height*1.3*0.186, screen_height*1.3*0.054, screen_height*1.3*0.0275))
        self.compensate_edit2_3.setGeometry(QtCore.QRect(0, screen_height*1.3*0.0177, screen_height*1.3*0.1692, screen_height*1.3*0.0142))
        self.intensity_edit.setGeometry(QtCore.QRect(0, 0, screen_height*1.3*0.1692, screen_height*1.3*0.0275))
        self.intensity_red_title.setGeometry(QtCore.QRect(screen_height*1.3*0.0664, screen_height*1.3*0.0443, screen_height*1.3*0.071, screen_height*1.3*0.0177))
        self.intensity_blue_title.setGeometry(QtCore.QRect(screen_height*1.3*0.0753, screen_height*1.3*0.1683, screen_height*1.3*0.0753, screen_height*1.3*0.0177))
        self.Green_intensity_edit_min.setGeometry(QtCore.QRect(screen_height*1.3*0.053, screen_height*1.3*0.124, screen_height*1.3*0.054, screen_height*1.3*0.0275))
        self.intensity_green_title.setGeometry(QtCore.QRect(screen_height*1.3*0.0753, screen_height*1.3*0.1063, screen_height*1.3*0.0797, screen_height*1.3*0.0177))
        self.Red_intensity_edit_max.setGeometry(QtCore.QRect(screen_height*1.3*0.1107, screen_height*1.3*0.062, screen_height*1.3*0.054, screen_height*1.3*0.0275))
        self.Green_intensity_edit_max.setGeometry(QtCore.QRect(screen_height*1.3*0.1107, screen_height*1.3*0.124, screen_height*1.3*0.054, screen_height*1.3*0.0275))
        self.Blue_intensity_edit_max.setGeometry(QtCore.QRect(screen_height*1.3*0.1107, screen_height*1.3*0.186, screen_height*1.3*0.054, screen_height*1.3*0.0275))
    
    def applyShadow(self):
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QtGui.QColor(209, 209, 209))
        return shadow
    
    def set_all_images(self):
        self.parent.set_image(self.parent.red_mask, self.RED_Label, "red", mask=True)
        self.parent.set_image(self.parent.green_mask, self.GREEN_Label, "green", mask=True)
        self.parent.set_image(self.parent.blue_mask, self.BLUE_Label, "blue", mask=True)
    
    def two_similarity_overlap(self, image1, image2, edit, overlap_type):
        similarity = 0
        overlapping = np.zeros_like(image1, dtype=np.uint8)
        mask=np.logical_and(image1==1, image2==1)
        overlapping[mask]=1
        if(overlap_type=="RG"):
            overlapping_dstack = np.dstack((image1, image2, np.zeros_like(image1)))
        elif(overlap_type=="RB"):
            overlapping_dstack = np.dstack((image1, np.zeros_like(image1), image2))
        elif(overlap_type=="GB"):
            overlapping_dstack = np.dstack((np.zeros_like(image1), image1, image2))
        similarity=overlapping.sum()
        edit.setText(str(round((similarity*100)/(image1.shape[0] 
                                                 * image1.shape[1]), 2))
                     + "% - " + str(similarity) + " pixels")
        return overlapping_dstack
    
    def similarity_buttonRB(self):
        image = self.two_similarity_overlap(self.parent.red_mask, self.parent.blue_mask, self.RB_PercentS_edit, "RB")
        image_visualize = image*255
        self.convert_npToQimage(image_visualize)
    
    def convert_npToQimage(self, image_visualize):
        qt_image = QImage(image_visualize.data, image_visualize.shape[1], image_visualize.shape[0], image_visualize.strides[0], QImage.Format_RGB888)
        qt_pixmap = QPixmap.fromImage(qt_image)
        self.RGB_Label.setPixmap(qt_pixmap)
    
    def similarity_buttonRG(self):
        image = self.two_similarity_overlap(self.parent.red_mask, self.parent.green_mask, self.RG_PercentS_edit, "RG")
        image_visualize = image*255
        self.convert_npToQimage(image_visualize)
    
    def similarity_buttonGB(self):
        image = self.two_similarity_overlap(self.parent.green_mask, self.parent.blue_mask, self.BG_PercentS_edit, "GB")
        image_visualize = image*255
        self.convert_npToQimage(image_visualize)
    
    def similarity_buttonRGB(self):
        image = self.AllimagesOverlap()
        image_visualize = image*255
        self.convert_npToQimage(image_visualize)
    
    def AllimagesOverlap(self):
        similarity = 0
        #3d_matrix_rgb = np.zeros((2, 3))
        overlapping = np.zeros_like(self.parent.red_image, dtype=np.uint8)
        self.parent.red_mask=self.parent.red_mask.astype(np.uint8)
        mask=np.logical_and(self.parent.red_mask==1, self.parent.green_mask==1, self.parent.blue_mask==1)
        overlapping[mask]=1
        overlapping_stack = np.dstack((self.parent.red_mask, self.parent.green_mask, 
                                       self.parent.blue_mask))
        similarity=overlapping.sum()                          
        self.RGB_Label.setScaledContents(True)
        self.RGB_PercentS_edit.setText(str(round((similarity*100)/(self.parent.red_image.shape[0] * 
                                                                   self.parent.red_image.shape[1]), 2))+ 
                                       "% - " + str(similarity) + " pixels")
        return overlapping_stack
    
    def biologicalContents(self, imageMatrix, edit):
        count = imageMatrix.sum();
        edit.setText(str(round((count*100)/(imageMatrix.shape[0] * 
                                            imageMatrix.shape[1]), 2))
                     + "% - " + str(count) + " pixels")
        
    def set_biologicalRED(self):
        self.biologicalContents(self.parent.red_mask, self.Red_PercentBC_edit)
    
    def set_biologicalGREEN(self):
        self.biologicalContents(self.parent.green_mask, self.Green_PercentBC_edit) 
    
    def set_biologicalBLUE(self):
        self.biologicalContents(self.parent.blue_mask, self.Blue_PercentBC_edit) 
    
    def countCells(self, matrixMask, edit, color_image):
        #imageFiltered = ndimage.gaussian_filter(matrixMask, self.parameter)
        #cells, number_of_cells = ndimage.label(imageFiltered)
        labeled_array, num_features = label(matrixMask)
        edit.setText(str(num_features) + " islands")
        self.parent.set_image(labeled_array, self.RGB_Label, color_image, mask=True)
        
    def confirm_parameter(self):
        self.buttonPressed=True
        try:
            self.parameter = float(self.parameter_edit.text())
            float(self.parameter)
            return
        except ValueError:
            self.error_message("Insert a number!")
    
    def set_number_RED(self):
        self.countCells(self.parent.red_mask, self.Red_number_edit, "red")
    
    def set_number_GREEN(self):
        self.countCells(self.parent.green_mask, self.Green_number_edit, "green")
    
    def set_number_BLUE(self):
        self.countCells(self.parent.blue_mask, self.Blue_number_edit, "blue")
        
    def set_min_max_intensityRED(self):
        self.Red_intensity_edit_min.setText("Min: " + str(np.min(self.parent.red_image)))
        self.Red_intensity_edit_max.setText("Max: " + str(np.max(self.parent.red_image)))
        
    def set_min_max_intensityGREEN(self):
        self.Green_intensity_edit_min.setText("Min: " + str(np.min(self.parent.green_image)))
        self.Green_intensity_edit_max.setText("Max: " + str(np.max(self.parent.green_image)))
        
    def set_min_max_intensityBLUE(self):
        self.Blue_intensity_edit_min.setText("Min: " + str(np.min(self.parent.blue_image)))
        self.Blue_intensity_edit_max.setText("Max: " + str(np.max(self.parent.blue_image)))
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            self.confirm_parameter()
            
    def image_size(self, image):
        self.label.setText("Images size: " + str(image.shape[0]) + "x"
                   + str(image.shape[1]) + "=" + str(image.shape[0]*image.shape[1]) + " pixels")
        
    def clearAll(self):
        # clear labels
        self.RGB_Label.clear()
        
        # clear QLineEdit overlapWidget
        self.RB_PercentS_edit.clear()
        self.RG_PercentS_edit.clear()
        self.BG_PercentS_edit.clear()
        self.RGB_PercentS_edit.clear()
        
        # clear QLineEdit biologicalContents
        self.Red_PercentBC_edit.clear()
        self.Green_PercentBC_edit.clear()
        self.Blue_PercentBC_edit.clear()
        
        # clear QLineEdit numberOfIslands
        self.Red_number_edit.clear()
        self.Green_number_edit.clear()
        self.Blue_number_edit.clear()
        
        # clear QLineEdit intensityWidget
        self.Red_intensity_edit_min.clear()
        self.Red_intensity_edit_max.clear()
        self.Green_intensity_edit_min.clear()
        self.Green_intensity_edit_max.clear()
        self.Blue_intensity_edit_min.clear()
        self.Blue_intensity_edit_max.clear()
        
    def save_message(self):
        mbox = QMessageBox(self)
        mbox.setIcon(QMessageBox.Question)
        mbox.setWindowTitle("Confirm")
        mbox.setText("You are deleting image analysis")
        mbox.setInformativeText("Do you want to delate your analysis?")
        mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        returnValue = mbox.exec()
        if returnValue == QMessageBox.Yes:
            self.clearAll()
        else:
            pass
        
    def error_message(self, text_error):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(text_error)
        msg.setWindowTitle("Error")
        msg.exec_()   
        
    def image_None(self):
        
        if (self.parent.red_mask is None):
            self.red_blue_buttonS.setEnabled(False)
            self.red_green_buttonS.setEnabled(False)
            self.total_buttonS.setEnabled(False)
            self.red_buttonBC.setEnabled(False)
            self.number_button_red.setEnabled(False)
            
        if (self.parent.green_mask is None):
            self.blue_green_buttonS.setEnabled(False)
            self.red_green_buttonS.setEnabled(False)
            self.total_buttonS.setEnabled(False)
            self.green_buttonBC.setEnabled(False)
            self.number_button_green.setEnabled(False)
            
        if (self.parent.blue_mask is None):
            self.blue_green_buttonS.setEnabled(False)
            self.red_blue_buttonS.setEnabled(False)
            self.total_buttonS.setEnabled(False)
            self.blue_buttonBC.setEnabled(False)
            self.number_button_blue.setEnabled(False)
    
    def help_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Function information")
        msg.setWindowTitle("Function information")
        msg.setText("INTERSECT FUNCTION: the intersection function overlaps images and returns an image whose colors represent the parts in common between the images themselves. \
                                                                                                               DENSITY FUNCTION: density is a function that returns the percentage and number of pixels of the biological content in the image \
                                                                                     NUMBER OF ISLANDS FUNCTION: returns an approximate number of cells in the image. It is necessary to perform the image processing operation in the best way, to obtain a more reliable result. \
                                                                                         INTENSITY FUNCTION: returns the maximum and minimum intensity of the unbinarized image")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
