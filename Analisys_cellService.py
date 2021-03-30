import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QColor
import numpy as np
import skimage
import skimage.io
from skimage import exposure
import skimage.morphology
from skimage import filters
from scipy import ndimage

class Ui_Analisys_cellService(QMainWindow):
    
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        
        self.setupUi()
        
        self.set_numberWidget()       
        
        self.set_biologicalWidget()
        
        self.set_similarityWidget()
        
        self.set_menuBar()
    
    def setupUi(self):
        # set the window's style
        self.setObjectName("Analisys_cellService")
        self.resize(946, 754)
        self.setWindowTitle("Analisys")
        
        # set principa widget's style
        self.principal_widget = QtWidgets.QWidget()
        self.principal_widget.setStyleSheet("background-color: rgb(244, 244, 244);\n""")
        self.principal_widget.setObjectName("principal_widget")
        
        # set grid widget
        self.gridLayoutWidget = QtWidgets.QWidget(self.principal_widget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(230, 10, 681, 681))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        
        # set grid layout
        self.principal_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.principal_layout.setContentsMargins(0, 0, 0, 0)
        self.principal_layout.setObjectName("principal_layout")
        
        # set RED Label and add the label to grid layout
        self.RED_Label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.RED_Label.setTabletTracking(True)
        self.RED_Label.setStyleSheet("border: 2px solid red")
        self.RED_Label.setFrameShape(QtWidgets.QFrame.Panel)
        self.RED_Label.setLineWidth(2)
        self.RED_Label.setText("")
        self.RED_Label.setScaledContents(True)
        self.RED_Label.setObjectName("RED_Label")
        self.principal_layout.addWidget(self.RED_Label, 0, 0, 1, 1)
        
        # set BLUE Label and add the label to grid layout
        self.RGB_Label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.RGB_Label.setStyleSheet("border: 2px solid black")
        self.RGB_Label.setText("")
        self.RGB_Label.setScaledContents(True)
        self.RGB_Label.setObjectName("RGB_Label")
        self.principal_layout.addWidget(self.RGB_Label, 1, 1, 1, 1)
        
        # set GREEN Label and add the label to grid layout
        self.BLUE_Label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.BLUE_Label.setStyleSheet("border: 2px solid blue")
        self.BLUE_Label.setText("")
        self.BLUE_Label.setScaledContents(True)
        self.BLUE_Label.setObjectName("BLUE_Label")
        self.principal_layout.addWidget(self.BLUE_Label, 1, 0, 1, 1)
        
        # set RED Label and add the label to grid layout
        self.GREEN_Label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.GREEN_Label.setStyleSheet("border: 2px solid green")
        self.GREEN_Label.setText("")
        self.GREEN_Label.setScaledContents(True)
        self.GREEN_Label.setObjectName("GREEN_Label")
        self.principal_layout.addWidget(self.GREEN_Label, 0, 1, 1, 1)
        
    def set_biologicalWidget(self):
        self.biological_widget = QtWidgets.QWidget(self.principal_widget)
        self.biological_widget.setGeometry(QtCore.QRect(20, 310, 171, 211))
        self.biological_widget.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 30px;")
        self.biological_widget.setObjectName("biological_widget")
        self.biological_widget.setGraphicsEffect(self.applyShadow())
        self.red_buttonBC = QtWidgets.QPushButton(self.biological_widget)
        self.red_buttonBC.setGeometry(QtCore.QRect(10, 40, 41, 41))
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
        self.red_buttonBC.setGraphicsEffect(self.applyShadow())
        self.red_buttonBC.setText("")
        self.red_buttonBC.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">RED image biological contents</span></p></body></html>")
        self.red_buttonBC.setStatusTip("RED image biological contents")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon bio.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.red_buttonBC.setIcon(icon)
        self.red_buttonBC.setIconSize(QtCore.QSize(60, 35))
        self.red_buttonBC.setObjectName("red_buttonBC")
        self.red_buttonBC.clicked.connect(self.set_biologicalRED)
        self.green_buttonBC = QtWidgets.QPushButton(self.biological_widget)
        self.green_buttonBC.setGeometry(QtCore.QRect(10, 100, 41, 41))
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
        self.green_buttonBC.setGraphicsEffect(self.applyShadow())
        self.green_buttonBC.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon bio 3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.green_buttonBC.setIcon(icon1)
        self.green_buttonBC.setIconSize(QtCore.QSize(60, 35))
        self.green_buttonBC.setObjectName("green_buttonBC")
        self.green_buttonBC.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">GREEN image biological contents</span></p></body></html>")
        self.green_buttonBC.setStatusTip("GREEN image biological contents")
        self.green_buttonBC.clicked.connect(self.set_biologicalGREEN)
        self.blue_buttonBC = QtWidgets.QPushButton(self.biological_widget)
        self.blue_buttonBC.setGeometry(QtCore.QRect(10, 160, 41, 41))
        self.blue_buttonBC.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.blue_buttonBC.setStyleSheet("QPushButton {\n"
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
        self.blue_buttonBC.setGraphicsEffect(self.applyShadow())
        self.blue_buttonBC.setText("")
        self.blue_buttonBC.clicked.connect(self.set_biologicalBLUE)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon bio 2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.blue_buttonBC.setIcon(icon2)
        self.blue_buttonBC.setIconSize(QtCore.QSize(60, 35))
        self.blue_buttonBC.setObjectName("blue_buttonBC")
        self.blue_buttonBC.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">BLUE image biological contents</span></p></body></html>")
        self.blue_buttonBC.setStatusTip("BLUE image biological contents")

        self.Red_PercentBC_edit = QtWidgets.QLineEdit(self.biological_widget)
        self.Red_PercentBC_edit.setGeometry(QtCore.QRect(70, 50, 71, 31))
        self.Red_PercentBC_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 10px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 10pt \"Varela\";\n"
"color: rgb(255, 255, 255);")
        self.Red_PercentBC_edit.setReadOnly(True)
        self.Red_PercentBC_edit.setObjectName("Red_PercentBC_edit")
        self.Green_PercentBC_edit = QtWidgets.QLineEdit(self.biological_widget)
        self.Green_PercentBC_edit.setGeometry(QtCore.QRect(70, 110, 71, 31))
        self.Green_PercentBC_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 10px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 10pt \"Varela\";\n"
"color: rgb(255, 255, 255);")
        self.Green_PercentBC_edit.setReadOnly(True)
        self.Green_PercentBC_edit.setObjectName("Green_PercentBC_edit")
        self.Blue_PercentBC_edit = QtWidgets.QLineEdit(self.biological_widget)
        self.Blue_PercentBC_edit.setGeometry(QtCore.QRect(70, 170, 71, 31))
        self.Blue_PercentBC_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 10px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 10pt \"Varela\";\n"
"color: rgb(255, 255, 255);")
        self.Blue_PercentBC_edit.setReadOnly(True)
        self.Blue_PercentBC_edit.setObjectName("Blue_PercentBC_edit")

        self.compensate_edit2 = QtWidgets.QLineEdit(self.biological_widget)
        self.compensate_edit2.setGeometry(QtCore.QRect(0, 20, 171, 16))
        self.compensate_edit2.setStyleSheet("background-color: rgb(19, 82, 255);\n"
"\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 14pt \"Varela\" bold;\n"
"color: rgb(255, 255, 255);")
        self.compensate_edit2.setText("")
        self.compensate_edit2.setReadOnly(True)
        self.compensate_edit2.setObjectName("compensate_edit2")
        self.biological_edit = QtWidgets.QLineEdit(self.biological_widget)
        self.biological_edit.setGeometry(QtCore.QRect(0, 0, 171, 31))
        self.biological_edit.setStyleSheet("background-color: rgb(19, 82, 255);\n"
"border-radius:15px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 13pt \"Varela\" bold;\n"
"color: rgb(255, 255, 255);")
        self.biological_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.biological_edit.setReadOnly(True)
        self.biological_edit.setObjectName("biological_edit")
        self.biological_edit.setText("Biological contents")
        
    def set_numberWidget(self):
        self.number_widget = QtWidgets.QWidget(self.principal_widget)
        self.number_widget.setGeometry(QtCore.QRect(20, 530, 171, 171))
        self.number_widget.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 30px;")
        self.number_widget.setObjectName("number_widget")
        #self.number_widget.setGraphicsEffect(self.applyShadow())
        self.number_cells_edit = QtWidgets.QLineEdit(self.number_widget)
        self.number_cells_edit.setGeometry(QtCore.QRect(70, 40, 71, 31))
        self.number_cells_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 10px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 10pt \"Varela\";\n"
"color: rgb(255, 255, 255);")
        self.number_cells_edit.setReadOnly(True)
        self.number_cells_edit.setObjectName("number_cells_edit")
        self.compensate_edit3 = QtWidgets.QLineEdit(self.number_widget)
        self.compensate_edit3.setGeometry(QtCore.QRect(0, 20, 171, 16))
        self.compensate_edit3.setStyleSheet("background-color: rgb(19, 82, 255);\n"
"\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 14pt \"Varela\" bold;\n"
"color: rgb(255, 255, 255);")
        self.compensate_edit3.setText("")
        self.compensate_edit3.setReadOnly(True)
        self.compensate_edit3.setObjectName("compensate_edit3")
        self.numbers_edit = QtWidgets.QLineEdit(self.number_widget)
        self.numbers_edit.setGeometry(QtCore.QRect(0, 0, 171, 31))
        self.numbers_edit.setStyleSheet("background-color: rgb(19, 82, 255);\n"
"border-radius:15px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 14pt \"Varela\" bold;\n"
"color: rgb(255, 255, 255);")
        self.numbers_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.numbers_edit.setReadOnly(True)
        self.numbers_edit.setObjectName("numbers_edit")
        self.numbers_edit.setText('Numbers of cells')
        self.number_button = QtWidgets.QPushButton(self.number_widget)
        self.number_button.setGeometry(QtCore.QRect(20, 40, 31, 31))
        self.number_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.number_button.setStyleSheet("QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-style: outset;\n"
"    border: 2px;\n"
"    border-width: 1px;\n"
"    border-radius: 15px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton::hover {\n"
"    background-color: rgb(204, 204, 204);\n"
"}"
"QPushButton:pressed {\n"
"    background-color: rgb(180, 180, 180);\n"
"}")
        self.number_button.clicked.connect(self.set_number_RED)
        self.number_button.setGraphicsEffect(self.applyShadow())
        self.number_button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icon n.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.number_button.setIcon(icon3)
        self.number_button.setIconSize(QtCore.QSize(40, 30))
        self.number_button.setObjectName("number_button")
        self.number_cells_edit_2 = QtWidgets.QLineEdit(self.number_widget)
        self.number_cells_edit_2.setGeometry(QtCore.QRect(70, 80, 71, 31))
        self.number_cells_edit_2.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 10px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 10pt \"Varela\";\n"
"color: rgb(255, 255, 255);")
        self.number_cells_edit_2.setReadOnly(True)
        self.number_cells_edit_2.setObjectName("number_cells_edit_2")
        self.number_cells_edit_3 = QtWidgets.QLineEdit(self.number_widget)
        self.number_cells_edit_3.setGeometry(QtCore.QRect(70, 120, 71, 31))
        self.number_cells_edit_3.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 10px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 10pt \"Varela\";\n"
"color: rgb(255, 255, 255);")
        self.number_cells_edit_3.setReadOnly(True)
        self.number_cells_edit_3.setObjectName("number_cells_edit_3")
        self.number_button_2 = QtWidgets.QPushButton(self.number_widget)
        self.number_button_2.setGeometry(QtCore.QRect(20, 80, 31, 31))
        self.number_button_2.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.number_button_2.setStyleSheet("QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-style: outset;\n"
"    border: 2px;\n"
"    border-width: 1px;\n"
"    border-radius: 15px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton::hover {\n"
"    background-color: rgb(204, 204, 204);\n"
"}"
"QPushButton:pressed {\n"
"    background-color: rgb(180, 180, 180);\n"
"}")
        self.number_button_2.clicked.connect(self.set_number_GREEN)
        self.number_button_2.setGraphicsEffect(self.applyShadow())
        self.number_button_2.setText("")
        self.number_button_2.setIcon(icon3)
        self.number_button_2.setIconSize(QtCore.QSize(40, 30))
        self.number_button_2.setObjectName("number_button_2")
        self.number_button_3 = QtWidgets.QPushButton(self.number_widget)
        self.number_button_3.setGeometry(QtCore.QRect(20, 120, 31, 31))
        self.number_button_3.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.number_button_3.setStyleSheet("QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-style: outset;\n"
"    border: 2px;\n"
"    border-width: 1px;\n"
"    border-radius: 15px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton::hover {\n"
"    background-color: rgb(204, 204, 204);\n"
"}"
"QPushButton:pressed {\n"
"    background-color: rgb(180, 180, 180);\n"
"}")
        self.number_button_3.clicked.connect(self.set_number_BLUE)
        self.number_button_3.setGraphicsEffect(self.applyShadow())
        self.number_button_3.setText("")
        self.number_button_3.setIcon(icon3)
        self.number_button_3.setIconSize(QtCore.QSize(40, 30))
        self.number_button_3.setObjectName("number_button_3")
        self.similarity_widget = QtWidgets.QWidget(self.principal_widget)
        self.similarity_widget.setGeometry(QtCore.QRect(20, 10, 171, 281))
        self.similarity_widget.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 30px;")
        self.similarity_widget.setObjectName("similarity_widget")
    
    def set_similarityWidget(self):
        self.similarity_widget = QtWidgets.QWidget(self.principal_widget)
        self.similarity_widget.setGeometry(QtCore.QRect(20, 10, 171, 281))
        self.similarity_widget.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 30px;")
        self.similarity_widget.setObjectName("similarity_widget")
        self.similarity_widget.setGraphicsEffect(self.applyShadow())
        self.red_blue_buttonS = QtWidgets.QPushButton(self.similarity_widget)
        self.red_blue_buttonS.setGeometry(QtCore.QRect(10, 40, 41, 41))
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
        self.red_blue_buttonS.setGraphicsEffect(self.applyShadow())
        self.red_blue_buttonS.setText("")
        self.red_blue_buttonS.clicked.connect(self.similarity_buttonRB)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icon 1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.red_blue_buttonS.setIcon(icon5)
        self.red_blue_buttonS.setIconSize(QtCore.QSize(60, 35))
        self.red_blue_buttonS.setObjectName("red_blue_buttonS")
        self.red_blue_buttonS.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">RED and BLUE similarity</span></p></body></html>")
        self.red_blue_buttonS.setStatusTip("RED and BLUE similarity")
        self.red_green_buttonS = QtWidgets.QPushButton(self.similarity_widget)
        self.red_green_buttonS.setGeometry(QtCore.QRect(10, 100, 41, 41))
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
        self.red_green_buttonS.setGraphicsEffect(self.applyShadow())
        self.red_green_buttonS.setText("")
        self.red_green_buttonS.clicked.connect(self.similarity_buttonRG)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icon 2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.red_green_buttonS.setIcon(icon6)
        self.red_green_buttonS.setIconSize(QtCore.QSize(60, 35))
        self.red_green_buttonS.setObjectName("red_green_buttonS")
        self.red_green_buttonS.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">RED and GREEN similarity</span></p></body></html>")
        self.red_green_buttonS.setStatusTip("RED and GREEN similarity")
        self.blue_green_buttonS = QtWidgets.QPushButton(self.similarity_widget)
        self.blue_green_buttonS.setGeometry(QtCore.QRect(10, 160, 41, 41))
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
"}")
        self.blue_green_buttonS.setGraphicsEffect(self.applyShadow())
        self.blue_green_buttonS.setText("")
        self.blue_green_buttonS.clicked.connect(self.similarity_buttonGB)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icon 3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.blue_green_buttonS.setIcon(icon7)
        self.blue_green_buttonS.setIconSize(QtCore.QSize(60, 35))
        self.blue_green_buttonS.setObjectName("blue_green_buttonS")
        self.blue_green_buttonS.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">GREEN and BLUE similarity</span></p></body></html>")
        self.blue_green_buttonS.setStatusTip("GREEN and BLUE similarity")
        self.total_buttonS = QtWidgets.QPushButton(self.similarity_widget)
        self.total_buttonS.setGeometry(QtCore.QRect(10, 220, 41, 41))
        self.total_buttonS.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.total_buttonS.setStyleSheet("QPushButton {\n"
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
        self.total_buttonS.setGraphicsEffect(self.applyShadow())
        self.total_buttonS.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icon 4.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.total_buttonS.setIcon(icon8)
        self.total_buttonS.setIconSize(QtCore.QSize(60, 35))
        self.total_buttonS.setObjectName("total_buttonS")
        self.total_buttonS.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">RED, GREEN and BLUE similarity</span></p></body></html>")
        self.total_buttonS.setStatusTip("RED, GREEN and BLUE similarity")
        self.total_buttonS.clicked.connect(self.similarity_buttonRGB)
        self.RB_PercentS_edit = QtWidgets.QLineEdit(self.similarity_widget)
        self.RB_PercentS_edit.setGeometry(QtCore.QRect(70, 50, 71, 31))
        self.RB_PercentS_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 10px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 10pt \"Varela\";\n"
"color: rgb(255, 255, 255);")
        self.RB_PercentS_edit.setText("")
        self.RB_PercentS_edit.setReadOnly(True)
        self.RB_PercentS_edit.setObjectName("RB_PercentS_edit")
        self.RG_PercentS_edit = QtWidgets.QLineEdit(self.similarity_widget)
        self.RG_PercentS_edit.setGeometry(QtCore.QRect(70, 110, 71, 31))
        self.RG_PercentS_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 10px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 10pt \"Varela\";\n"
"color: rgb(255, 255, 255);")
        self.RG_PercentS_edit.setReadOnly(True)
        self.RG_PercentS_edit.setObjectName("RG_PercentS_edit")
        self.BG_PercentS_edit = QtWidgets.QLineEdit(self.similarity_widget)
        self.BG_PercentS_edit.setGeometry(QtCore.QRect(70, 170, 71, 31))
        self.BG_PercentS_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 10px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 10pt \"Varela\";\n"
"color: rgb(255, 255, 255);")
        self.BG_PercentS_edit.setReadOnly(True)
        self.BG_PercentS_edit.setObjectName("BG_PercentS_edit")
        self.RGB_PercentS_edit = QtWidgets.QLineEdit(self.similarity_widget)
        self.RGB_PercentS_edit.setGeometry(QtCore.QRect(70, 230, 71, 31))
        self.RGB_PercentS_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
"    border-radius: 10px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 10pt \"Varela\";\n"
"color: rgb(255, 255, 255);")
        self.RGB_PercentS_edit.setReadOnly(True)
        self.RGB_PercentS_edit.setObjectName("RGB_PercentS_edit")
        self.compensate_edit = QtWidgets.QLineEdit(self.similarity_widget)
        self.compensate_edit.setGeometry(QtCore.QRect(0, 20, 171, 16))
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
        self.similarity_edit.setGeometry(QtCore.QRect(0, 0, 171, 31))
        self.similarity_edit.setStyleSheet("background-color: rgb(19, 82, 255);\n"
"border-radius:15px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"font: 14pt \"Varela\" bold;\n"
"color: rgb(255, 255, 255);")
        self.similarity_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.similarity_edit.setReadOnly(True)
        self.similarity_edit.setObjectName("similarity_edit")
        self.similarity_edit.setText("Similarity")
        self.setCentralWidget(self.principal_widget)
        
    def set_menuBar(self):
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 946, 21))
        self.menubar.setTabletTracking(False)
        self.menubar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.menubar.setStyleSheet("background-color: rgb(255, 253, 253);\n"
"selection-color: rgb(128, 183, 255);\n"
"color: rgb(71, 71, 71);")
        self.menubar.setObjectName("menubar")
        self.file_menu = QtWidgets.QMenu(self.menubar)
        self.file_menu.setObjectName("file_menu")
        self.file_menu.setTitle("File")
        self.help_menu = QtWidgets.QMenu(self.menubar)
        self.help_menu.setObjectName("help_menu")
        self.help_menu.setTitle("Help")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionPre_processed_image_analisys = QtWidgets.QAction()
        self.actionPre_processed_image_analisys.setObjectName("actionPre_processed_image_analisys")
        self.actionPre_processed_image_analisys.setText("Analysis of pre-processed images")
        self.actionPre_processed_image_analisys.triggered.connect(self.set_all_images)
        self.actionNew_images_analisys = QtWidgets.QAction()
        self.actionNew_images_analisys.setObjectName("actionNew_images_analisys")
        self.actionNew_images_analisys.setText("New images analisys")
        self.actionNew_images_analysis = QtWidgets.QAction()
        self.actionNew_images_analysis.setObjectName("actionNew_images_analysis")
        self.actionNew_images_analysis.setText("New images to analyze")
        self.file_menu.addAction(self.actionPre_processed_image_analisys)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.actionNew_images_analysis)
        self.menubar.addAction(self.file_menu.menuAction())
        self.menubar.addAction(self.help_menu.menuAction())
        
    def applyShadow(self):
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(QtGui.QColor(209, 209, 209))
        return shadow
    
    def set_all_images(self):
        self.parent.set_image(self.parent.red_image, self.RED_Label, "red", mask=False)
        self.parent.set_image(self.parent.green_image, self.GREEN_Label, "green", mask=False)
        self.parent.set_image(self.parent.blue_image, self.BLUE_Label, "blue", mask=False)
    
    def two_similarity_overlap(self, image1, image2, edit):
        similarity = 0
        overlapping = np.zeros_like(image1)
        
        for i in range(image1.shape[0]):
            for j in range(image1.shape[1]):
                if (image1[i][j]==image2[i][j]):
                    similarity += 1
                    overlapping[i][j]=1
        edit.setText(str(round((similarity*100)/(self.parent.red_mask.shape[0]* self.parent.red_mask.shape[1]), 2))+ "%")
        return overlapping
    
    def runSimilarity(self, buttonPressed):
        if self.red_blue_buttonS.isChecked():
            self.parent.set_image(self.two_similarity_overlap(self.parent.red_mask, self.parent.blue_mask), self.RGB_Label, "red", mask=True)
        elif self.red_green_buttonS.isChecked():
            self.parent.set_image(self.two_similarity_overlap(self.parent.red_mask, self.parent.green_mask), self.RGB_Label, "green", mask=True)
        elif self.blue_green_buttonS.isChecked():
            self.parent.set_image(self.two_similarity_overlap(self.parent.blue_mask, self.parent.green_mask), self.RGB_Label, "blue", mask=True)
        elif self.total_buttonS.isChecked():
            self.parent.set_image(self.AllimagesOverlap(), self.RGB_Label, "blue", mask=True)
        else:
            pass
        self.RGB_Label.setScaledContents(True)
    
    def similarity_buttonRB(self):
        self.parent.set_image(self.two_similarity_overlap(self.parent.red_mask, self.parent.blue_mask, self.RB_PercentS_edit), self.RGB_Label, "red", mask=True)
    
    def similarity_buttonRG(self):
        self.parent.set_image(self.two_similarity_overlap(self.parent.red_mask, self.parent.green_mask, self.RG_PercentS_edit), self.RGB_Label, "green", mask=True)
    
    def similarity_buttonGB(self):
        self.parent.set_image(self.two_similarity_overlap(self.parent.green_mask, self.parent.blue_mask, self.BG_PercentS_edit), self.RGB_Label, "blue", mask=True)
    
    def similarity_buttonRGB(self):
        self.parent.set_image(self.AllimagesOverlap(), self.RGB_Label, "green" ,mask=True)
    
    def AllimagesOverlap(self):
        similarity=0
        overlapping = np.zeros_like(self.parent.red_mask)
        for i in range(self.parent.red_mask.shape[0]):
          for j in range(self.parent.red_mask.shape[1]):
              if (self.parent.red_mask[i][j]==1 and self.parent.green_mask[i][j]==1 
                  and self.parent.blue_mask[i][j]==1):
                          overlapping[i][j]=1
                          similarity+=1
                          
        self.RGB_Label.setScaledContents(True)
        self.RGB_PercentS_edit.setText(str(round((similarity*100)/(self.parent.red_mask.shape[0]* self.parent.red_mask.shape[1]), 2))+ "%")
        return overlapping
    
    def biologicalContents(self, imageMatrix, edit):
        count = 0;
        for i in range(imageMatrix.shape[0]):
            for j in range(imageMatrix.shape[1]):
                if imageMatrix[i][j] == 1:
                    count = count+1
        edit.setText(str(round((count*100)/(self.parent.red_mask.shape[0]* self.parent.red_mask.shape[1]), 2))+ "%")
    
    def set_biologicalRED(self):
        self.biologicalContents(self.parent.red_mask, self.Red_PercentBC_edit)
    
    def set_biologicalGREEN(self):
        self.biologicalContents(self.parent.green_mask, self.Green_PercentBC_edit) 
    
    def set_biologicalBLUE(self):
        self.biologicalContents(self.parent.blue_mask, self.Blue_PercentBC_edit) 
    
    def countCells(self, matrixMask, edit):
        imageFiltered = ndimage.gaussian_filter(matrixMask, 0.1)
        cells, number_of_cells = ndimage.label(imageFiltered)
        edit.setText(str(number_of_cells) + " cells")
        self.parent.set_image(cells, self.RGB_Label, "red", mask=True)
    
    def set_number_RED(self):
        self.countCells(self.parent.red_mask, self.number_cells_edit)
    
    def set_number_GREEN(self):
        self.countCells(self.parent.green_mask, self.number_cells_edit_2)
    
    def set_number_BLUE(self):
        self.countCells(self.parent.blue_mask, self.number_cells_edit_3)


