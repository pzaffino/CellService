from PyQt5.QtWidgets import (QMessageBox, QMainWindow)
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
import numpy as np
from skimage import filters,morphology

class Processing_cellService(QMainWindow):
    
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
        
        self.setupUI()
        self.binary_processing()
        self.set_segmentation()
        
    def setupUI(self):
        self.setFixedSize(1120, 826)
        self.principal_widget = QtWidgets.QWidget()
        self.gridLayoutWidget = QtWidgets.QWidget(self.principal_widget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(260, 60, 561, 721))
        self.principal_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.principal_layout.setContentsMargins(0, 0, 0, 0)
        
        self.Original_Label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Original_Label.setTabletTracking(True)
        self.Original_Label.setStyleSheet("border: 2px solid red")
        self.Original_Label.setFixedSize(275,235)
        self.Original_Label.setFrameShape(QtWidgets.QFrame.Panel)
        self.Original_Label.setLineWidth(2)
        self.Original_Label.setScaledContents(True)
        self.principal_layout.addWidget(self.Original_Label, 1, 0, 1, 1)
        self.Filtred_Label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Filtred_Label.setTabletTracking(True)
        self.Filtred_Label.setStyleSheet("border: 2px solid red")
        self.Filtred_Label.setFrameShape(QtWidgets.QFrame.Panel)
        self.Filtred_Label.setLineWidth(2)
        self.Filtred_Label.setFixedSize(275,235)
        self.Filtred_Label.setScaledContents(True)
        self.principal_layout.addWidget(self.Filtred_Label, 1, 1, 1, 1)
        
        self.Original_Label1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Original_Label1.setStyleSheet("border: 2px solid green")
        self.Original_Label1.setFixedSize(275,235)
        self.Original_Label1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Original_Label1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Original_Label1.setLineWidth(2)
        self.Original_Label1.setScaledContents(True)
        self.principal_layout.addWidget(self.Original_Label1, 3, 0, 1, 1)
        self.Filtred_Label1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Filtred_Label1.setStyleSheet("border: 2px solid green")
        self.Filtred_Label1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Filtred_Label1.setFixedSize(275,235)
        self.Filtred_Label1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Filtred_Label1.setLineWidth(2)
        self.Filtred_Label1.setScaledContents(True)
        self.principal_layout.addWidget(self.Filtred_Label1, 3, 1, 1, 1)
        
        self.Original_Label2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Original_Label2.setStyleSheet("border: 2px solid blue")
        self.Original_Label2.setScaledContents(True)
        self.Original_Label2.setFixedSize(275,235)
        self.principal_layout.addWidget(self.Original_Label2, 4, 0, 1, 1)
        self.Filtred_Label2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Filtred_Label2.setStyleSheet("border: 2px solid blue")
        self.Filtred_Label2.setScaledContents(True)
        self.Filtred_Label2.setFixedSize(275,235)
        self.principal_layout.addWidget(self.Filtred_Label2, 4, 1, 1, 1)
        
        self.radioRed = QtWidgets.QRadioButton(self.principal_widget)
        self.radioRed.setText("RadioButton")
        self.radioRed.setChecked(True)
        self.radioRed.setGeometry(QtCore.QRect(320, 20, 101, 20))
        self.radioRed.setStyleSheet("font: 8pt \"Arial\";\n" "color: red;\n")
        self.radioGreen = QtWidgets.QRadioButton(self.principal_widget)
        self.radioGreen.setText("RadioButton")
        self.radioGreen.setGeometry(QtCore.QRect(490, 20, 101, 20))
        self.radioGreen.setStyleSheet("font: 8pt \"Arial\";\n" "color: Green;")
        self.radioBlue = QtWidgets.QRadioButton(self.principal_widget)
        self.radioBlue.setGeometry(QtCore.QRect(670, 20, 101, 20))
        self.radioBlue.setStyleSheet("font: 8pt \"Arial\";\n" "color: Blue;")
        self.radioBlue.setText("RadioButton")
        
        self.help_button = QtWidgets.QPushButton(self.principal_widget)
        self.help_button.setGraphicsEffect(self.applyShadow())
        self.help_button.setGeometry(QtCore.QRect(110, 10, 41, 41))
        self.help_button.setMouseTracking(True)
        self.help_button.setFocusPolicy(QtCore.Qt.StrongFocus)
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
            "\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}\n"
            "")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Icon/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.help_button.setIcon(icon2)
        self.help_button.setIconSize(QtCore.QSize(35, 30))
        self.help_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Help </span></p></body></html>")
        self.help_button.setStatusTip("Help")
       
        self.save_button = QtWidgets.QPushButton(self.principal_widget)
        self.save_button.setGraphicsEffect(self.applyShadow())
        self.save_button.setGeometry(QtCore.QRect(190, 10, 41, 41))
        self.save_button.setMouseTracking(True)
        self.save_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.save_button.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 10px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}\n"
            "")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Icon/save_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_button.setIcon(icon3)
        self.save_button.setIconSize(QtCore.QSize(35, 30))
        self.save_button.clicked.connect(self.save)
        self.save_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Save all changes</span></p></body></html>")
        self.save_button.setStatusTip("Save all changes")
        
        self.Label_Save = QtWidgets.QLabel(self.principal_widget)
        self.Label_Save.setGraphicsEffect(self.applyShadow())
        self.Label_Save.setEnabled(False)
        self.Label_Save.setGeometry(QtCore.QRect(20, 480, 221, 150))
        self.Label_Save.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "border-radius: 30px;\n"
            "font: 9pt \"Arial\";\n"
            "color: rgb(19, 82, 255);")
        self.Label_Save.setScaledContents(True)
        self.Label_Save.setText("Don't forget to save image!")
        
        self.delete_button = QtWidgets.QPushButton(self.principal_widget)
        self.delete_button.setGraphicsEffect(self.applyShadow())
        self.delete_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Delete </span></p></body></html>")
        self.delete_button.setStatusTip("Delete")
        self.delete_button.setGeometry(QtCore.QRect(30, 10, 41, 41))
        self.delete_button.setMouseTracking(True)
        self.delete_button.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.delete_button.setToolTipDuration(-1)
        self.delete_button.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 10px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}\n"
            "")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Icon/canc icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_button.setIcon(icon1)
        self.delete_button.setIconSize(QtCore.QSize(35, 30))
        self.delete_button.clicked.connect(self.Clear_filtred_label)
        self.setCentralWidget(self.principal_widget)
        
        self.selezioni=np.array([0,0,0,0,0])
        self.valore=0
        self.set_all_images()

    def set_segmentation(self):
        self.segmentation_widget = QtWidgets.QWidget(self.principal_widget)
        self.segmentation_widget.setGeometry(QtCore.QRect(840, 50, 261, 631))
        self.segmentation_widget.setGraphicsEffect(self.applyShadow())
        self.segmentation_widget.setStyleSheet("background-color: rgb(255, 255, 255);\n" "border-radius: 35px;")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Icon/confirm.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.Add_button = QtWidgets.QPushButton(self.segmentation_widget)
        self.Add_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Add Changes to the filtred image</span></p></body></html>")
        self.Add_button.setStatusTip("Add Changes to the filtred image")
        self.Add_button.clicked.connect(self.add_change)
        self.Add_button.setGraphicsEffect(self.applyShadow())
        self.Add_button.setGeometry(QtCore.QRect(50, 470, 41, 41))
        self.Add_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Add_button.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Add_button.setIcon(icon3)
        self.Add_button.setIconSize(QtCore.QSize(60, 35))
        self.New_button = QtWidgets.QPushButton(self.segmentation_widget)
        self.New_button.setGraphicsEffect(self.applyShadow())
        self.New_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Filtres a binarized image</span></p></body></html>")
        self.New_button.setStatusTip("Filtres a binarized image")
        self.New_button.clicked.connect(self.apply_segmentation)
        self.New_button.setGeometry(QtCore.QRect(160, 470, 41, 41))
        self.New_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.New_button.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("Icon/images.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.New_button.setIcon(icon4)
        self.Back_button = QtWidgets.QPushButton(self.segmentation_widget)
        self.Back_button.setGraphicsEffect(self.applyShadow())
        self.Back_button.setGeometry(QtCore.QRect(110, 550, 41, 41))
        self.Back_button.setMouseTracking(True)
        self.Back_button.clicked.connect(self.back_binary)
        self.Back_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Back_button.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 10px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}\n"
            "")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("Icon/back_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Back_button.setIcon(icon5)
        self.Back_button.setIconSize(QtCore.QSize(60, 35))
        self.Back_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Back to binarized images </span></p></body></html>")
        self.Back_button.setStatusTip("Back to binarized images")

        self.Remove_button = QtWidgets.QPushButton(self.segmentation_widget)
        self.Remove_button.setGeometry(QtCore.QRect(30, 130, 41, 41))
        self.Remove_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Remove_button.setGraphicsEffect(self.applyShadow())
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
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icon/icon n 3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Remove_button.setIcon(icon)
        self.Remove_button.clicked.connect(self.set_edit_remove)
        self.Remove_button.setGraphicsEffect(self.applyShadow())
        self.Remove_button.setIconSize(QtCore.QSize(60, 35))
        self.Remove_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Remove small object</span></p></body></html>")
        self.Remove_button.setStatusTip("Remove small object")
        self.Erosion_button = QtWidgets.QPushButton(self.segmentation_widget)
        self.Erosion_button.setGeometry(QtCore.QRect(30, 200, 41, 41))
        self.Erosion_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Erosion_button.setStyleSheet("QPushButton {\n"
            "    background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "    border-style: inset;\n"
            "}")
        self.Erosion_button.setGraphicsEffect(self.applyShadow())
        self.Erosion_button.setIcon(icon)
        self.Erosion_button.setIconSize(QtCore.QSize(60, 35))
        self.Erosion_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Erosion</p></body></html>")
        self.Erosion_button.setStatusTip("Erosion")
        self.Erosion_button.clicked.connect(self.set_edit_erosion)
        
        self.Dilation_button = QtWidgets.QPushButton(self.segmentation_widget)
        self.Dilation_button.setGeometry(QtCore.QRect(30, 270, 41, 41))
        self.Dilation_button.setGraphicsEffect(self.applyShadow())
        self.Dilation_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Dilation_button.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Dilation_button.setIcon(icon)
        self.Dilation_button.clicked.connect(self.set_edit_dilation)
        self.Dilation_button.setToolTip( "<html><head/><body><p><span style=\" color:#80b7ff;\">Dilation</p></body></html>")
        self.Dilation_button.setStatusTip("Dilation")
        self.Dilation_button.setIconSize(QtCore.QSize(60, 35))
        self.Open_button = QtWidgets.QPushButton(self.segmentation_widget)
        self.Open_button.setGraphicsEffect(self.applyShadow())
        self.Open_button.setGeometry(QtCore.QRect(30, 340, 41, 41))
        self.Open_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Open_button.clicked.connect(self.set_edit_open)
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
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Open_button.setIcon(icon)
        self.Open_button.setIconSize(QtCore.QSize(60, 35))
        self.Open_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Opening</span></p></body></html>")
        self.Open_button.setStatusTip("Opening")
        self.Close_button = QtWidgets.QPushButton(self.segmentation_widget)
        self.Close_button.clicked.connect(self.set_edit_close)
        self.Close_button.setGraphicsEffect(self.applyShadow())
        self.Close_button.setGeometry(QtCore.QRect(30, 410, 41, 41))
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
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Close_button.setIcon(icon)
        self.Close_button.setIconSize(QtCore.QSize(60, 35))
        self.Close_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Closing</span></p></body></html>")
        self.Close_button.setStatusTip("Closing")
        
        self.Close_help = QtWidgets.QPushButton(self.segmentation_widget)
        self.Close_help.setGraphicsEffect(self.applyShadow())
        self.Close_help.setGeometry(QtCore.QRect(190, 422, 31, 31))
        self.Close_help.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Close_help.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Icon/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Close_help.setIcon(icon2)
        self.Close_help.clicked.connect(self.close_message)
        self.Open_help = QtWidgets.QPushButton(self.segmentation_widget)
        self.Open_help.setGraphicsEffect(self.applyShadow())
        self.Open_help.setGeometry(QtCore.QRect(190, 352, 31, 31))
        self.Open_help.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Open_help.clicked.connect(self.open_message)
        self.Open_help.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Open_help.setIcon(icon2)
        self.Dilation_help = QtWidgets.QPushButton(self.segmentation_widget)
        self.Dilation_help.setGraphicsEffect(self.applyShadow())
        self.Dilation_help.clicked.connect(self.dilation_message)
        self.Dilation_help.setGeometry(QtCore.QRect(190, 282, 31, 31))
        self.Dilation_help.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Dilation_help.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Dilation_help.setIcon(icon2)
        self.Erosion_help = QtWidgets.QPushButton(self.segmentation_widget)
        self.Erosion_help.setGraphicsEffect(self.applyShadow())
        self.Erosion_help.setGeometry(QtCore.QRect(190, 212, 31, 31))
        self.Erosion_help.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Erosion_help.clicked.connect(self.erosion_message)
        self.Erosion_help.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Erosion_help.setIcon(icon2)
        self.Remove_help = QtWidgets.QPushButton(self.segmentation_widget)
        self.Remove_help.setGraphicsEffect(self.applyShadow())
        self.Remove_help.clicked.connect(self.remove_message)
        self.Remove_help.setGeometry(QtCore.QRect(190, 142, 31, 31))
        self.Remove_help.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Remove_help.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Remove_help.setIcon(icon2)
        
        self.Remove_canc = QtWidgets.QPushButton(self.segmentation_widget)
        self.Remove_canc.setGraphicsEffect(self.applyShadow())
        self.Remove_canc.setGeometry(QtCore.QRect(150, 142, 31, 31))
        self.Remove_canc.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Remove_canc.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Icon/canc icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Remove_canc.setIcon(icon1)
        self.Remove_canc.clicked.connect(self.delete_edit_remove)
        self.Erosion_canc = QtWidgets.QPushButton(self.segmentation_widget)
        self.Erosion_canc.setGraphicsEffect(self.applyShadow())
        self.Erosion_canc.clicked.connect(self.delete_edit_erosion)
        self.Erosion_canc.setGeometry(QtCore.QRect(150, 212, 31, 31))
        self.Erosion_canc.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Erosion_canc.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Erosion_canc.setIcon(icon1)
        self.Dilation_canc = QtWidgets.QPushButton(self.segmentation_widget)
        self.Dilation_canc.setGraphicsEffect(self.applyShadow())
        self.Dilation_canc.setGeometry(QtCore.QRect(150, 282, 31, 31))
        self.Dilation_canc.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Dilation_canc.clicked.connect(self.delete_edit_dilation)
        self.Dilation_canc.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Dilation_canc.setIcon(icon1)
        self.Open_canc = QtWidgets.QPushButton(self.segmentation_widget)
        self.Open_canc.setGraphicsEffect(self.applyShadow())
        self.Open_canc.setGeometry(QtCore.QRect(150, 350, 31, 31))
        self.Open_canc.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Open_canc.clicked.connect(self.delete_edit_open)
        self.Open_canc.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Open_canc.setIcon(icon1)
        self.Close_canc = QtWidgets.QPushButton(self.segmentation_widget)
        self.Close_canc.setGraphicsEffect(self.applyShadow())
        self.Close_canc.setGeometry(QtCore.QRect(150, 420, 31, 31))
        self.Close_canc.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Close_canc.clicked.connect(self.delete_edit_close)
        self.Close_canc.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.Close_canc.setIcon(icon1)
        
        self.segmentation_edit = QtWidgets.QLineEdit(self.segmentation_widget)
        self.segmentation_edit.setGeometry(QtCore.QRect(0, 0, 261, 41))
        self.segmentation_edit.setStyleSheet("background-color: rgb(19, 82, 255);\n"
            "border-radius:15px;\n"
            "    padding: 6px;\n"
            "font: 14pt \"Arial\";\n"
            "color: rgb(255, 255, 255);")
        self.segmentation_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.segmentation_edit.setReadOnly(True)
        self.segmentation_edit.setText("Segmentation")
        self.Remove_edit = QtWidgets.QLineEdit(self.segmentation_widget)
        self.Remove_edit.setGeometry(QtCore.QRect(80, 140, 61, 31))
        self.Remove_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.Remove_edit.setReadOnly(True)
        self.Erosion_edit = QtWidgets.QLineEdit(self.segmentation_widget)
        self.Erosion_edit.setGeometry(QtCore.QRect(80, 210, 61, 31))
        self.Erosion_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.Erosion_edit.setReadOnly(True)
        self.Dilation_edit = QtWidgets.QLineEdit(self.segmentation_widget)
        self.Dilation_edit.setGeometry(QtCore.QRect(80, 280, 61, 31))
        self.Dilation_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.Dilation_edit.setReadOnly(True)
        self.Open_edit = QtWidgets.QLineEdit(self.segmentation_widget)
        self.Open_edit.setGeometry(QtCore.QRect(80, 350, 61, 31))
        self.Open_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.Open_edit.setReadOnly(True)
        self.Close_edit = QtWidgets.QLineEdit(self.segmentation_widget)
        self.Close_edit.setGeometry(QtCore.QRect(80, 420, 61, 31))
        self.Close_edit.setStyleSheet("background-color: rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: rgb(255, 255, 255);")
        self.Close_edit.setReadOnly(True)
        
        self.Add_title = QtWidgets.QLabel(self.segmentation_widget)
        self.Add_title.setGeometry(QtCore.QRect(20, 513, 91, 21))
        self.Add_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.Add_title.setText("Add Change")
        self.New_button.setIconSize(QtCore.QSize(60, 35))
        self.new_title = QtWidgets.QLabel(self.segmentation_widget)
        self.new_title.setGeometry(QtCore.QRect(120, 513, 121, 21))
        self.new_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.new_title.setText("New Segmentation")
        self.back_title = QtWidgets.QLabel(self.segmentation_widget)
        self.back_title.setGeometry(QtCore.QRect(80, 593, 111, 21))
        self.back_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.back_title.setText("Binarized images")
        self.remove_title = QtWidgets.QLineEdit(self.segmentation_widget)
        self.remove_title.setGeometry(QtCore.QRect(80, 120, 141, 20))
        self.remove_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.remove_title.setReadOnly(True)
        self.remove_title.setText("Remove Small Object")
        self.dilation_title = QtWidgets.QLineEdit(self.segmentation_widget)
        self.dilation_title.setText("Dilation")
        self.dilation_title.setGeometry(QtCore.QRect(90, 260, 91, 20))
        self.dilation_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.dilation_title.setReadOnly(True)
        self.erosion_title = QtWidgets.QLineEdit(self.segmentation_widget)
        self.erosion_title.setGeometry(QtCore.QRect(90, 190, 91, 20))
        self.erosion_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.erosion_title.setReadOnly(True)
        self.erosion_title.setText("Erosion")
        self.open_title = QtWidgets.QLineEdit(self.segmentation_widget)
        self.open_title.setGeometry(QtCore.QRect(90, 330, 91, 21))
        self.open_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.open_title.setReadOnly(True) 
        self.open_title.setText("Opening")
        self.close_title = QtWidgets.QLineEdit(self.segmentation_widget)
        self.close_title.setGeometry(QtCore.QRect(90, 399, 91, 21))
        self.close_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.close_title.setReadOnly(True)
        self.close_title.setText("Closing")
        
        self.Raggio = QtWidgets.QDoubleSpinBox(self.segmentation_widget)
        self.Raggio.setGeometry(QtCore.QRect(120, 60, 91, 31))
        self.Raggio.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "border: 2px solid rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: blue;")
        self.Raggio.setDecimals(3)
        self.Raggio.setMaximum(255.0)
        self.Radius_title = QtWidgets.QLineEdit(self.segmentation_widget)
        self.Radius_title.setGeometry(QtCore.QRect(40, 60, 71, 31))
        self.Radius_title.setStyleSheet("font: 10pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.Radius_title.setReadOnly(True)
        self.Radius_title.setText("Radius")
        
    def binary_processing(self):
        self.binary_widget = QtWidgets.QWidget(self.principal_widget)
        self.binary_widget.setGeometry(QtCore.QRect(10, 80, 241, 361))
        self.binary_widget.setGraphicsEffect(self.applyShadow())
        self.binary_widget.setStyleSheet("background-color: rgb(255, 255, 255);\n" "border-radius: 30px;")

        self.binary_widget_3 = QtWidgets.QWidget(self.binary_widget)
        self.binary_widget_3.setGraphicsEffect(self.applyShadow())
        self.binary_widget_3.setGeometry(QtCore.QRect(10, 60, 211, 121))
        self.binary_widget_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "border-radius:15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 14pt \"Varela\" bold;\n"
            "color: rgb(19, 82, 255);")

        self.Min_Label = QtWidgets.QLabel(self.binary_widget_3)
        self.Min_Label.setText("Min Threashold")
        self.Min_Label.setGeometry(QtCore.QRect(100, 30, 111, 31))
        self.Min_Label.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.Max_Label = QtWidgets.QLabel(self.binary_widget_3)
        self.Max_Label.setGeometry(QtCore.QRect(100, 70, 111, 31))
        self.Max_Label.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.Max_Label.setText("Max Threashold")
        
        self.fontSizeSpinBox = QtWidgets.QDoubleSpinBox(self.binary_widget_3)
        self.fontSizeSpinBox.setGeometry(QtCore.QRect(10, 30, 91, 31))
        self.fontSizeSpinBox.setDecimals(3)
        self.fontSizeSpinBox.setMaximum(255.0)
        self.fontSizeSpinBox.setStyleSheet("background-color: white;\n"
            "border: 2px solid rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: blue;")
        self.fontSizeSpinBox2 = QtWidgets.QDoubleSpinBox(self.binary_widget_3)
        self.fontSizeSpinBox2.setGeometry(QtCore.QRect(10, 70, 91, 31))
        self.fontSizeSpinBox2.setDecimals(3)
        self.fontSizeSpinBox2.setMaximum(255.0)
        self.fontSizeSpinBox2.setStyleSheet("background-color: white;\n"
            "border: 2px solid rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: blue;")
        
        self.automatic_button = QtWidgets.QPushButton(self.binary_widget)
        self.automatic_button.setGraphicsEffect(self.applyShadow())
        self.automatic_button.setGeometry(QtCore.QRect(90, 200, 41, 41))
        self.automatic_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.automatic_button.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("Icon/processing.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.automatic_button.setIcon(icon6)
        self.automatic_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Automatic Threashold</span></p></body></html>")
        self.automatic_button.setIconSize(QtCore.QSize(60, 35))
        self.automatic_button.setStatusTip("Automatic Threashold")
        self.automatic_button.clicked.connect(self.Automatic_threshold)
        
        self.apply = QtWidgets.QPushButton(self.binary_widget)
        self.apply.setGraphicsEffect(self.applyShadow())
        self.apply.setGeometry(QtCore.QRect(90, 280, 41, 41))
        self.apply.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.apply.clicked.connect(self.runIntensityBinarization)
        self.apply.setStyleSheet("QPushButton {\n"
            "     background-color: rgb(255, 255, 255);\n"
            "    border-style: outset;\n"
            "    border: 2px;\n"
            "    border-width: 1px;\n"
            "    border-radius: 20px;\n"
            "    border-color: beige;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(180, 180, 180);\n"
            "}")
        self.apply.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Icon/confirm.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.apply.setIcon(icon3)
        self.apply.setIconSize(QtCore.QSize(60, 35))
        self.apply.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Binarize Image</span></p></body></html>")
        self.apply.setStatusTip("Binarize Image")
        
        self.Automatic_title = QtWidgets.QLabel(self.binary_widget)
        self.Automatic_title.setGeometry(QtCore.QRect(50, 240, 131, 31))
        self.Automatic_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.Automatic_title.setText("Automatic Threashold")
        self.Apply_title = QtWidgets.QLabel(self.binary_widget)
        self.Apply_title.setText("Binarize Image")
        self.Apply_title.setGeometry(QtCore.QRect(70, 310, 101, 31))
        self.Apply_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.binary_edit = QtWidgets.QLineEdit(self.binary_widget)
        self.binary_edit.setGeometry(QtCore.QRect(0, 0, 241, 41))
        self.binary_edit.setStyleSheet("background-color: rgb(19, 82, 255);\n"
            "border-radius:15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 14pt \"Varela\" bold;\n"
            "color: rgb(255, 255, 255);")
        self.binary_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.binary_edit.setReadOnly(True)
        self.binary_edit.setText("Binarize")
        
    def applyShadow(self):
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QtGui.QColor(209, 209, 209))
        return shadow
    
    def set_all_images(self):
        self.parent.set_image(self.parent.red_image, self.Original_Label, "red", mask=False)
        self.parent.set_image(self.parent.green_image, self.Original_Label1, "green", mask=False)
        self.parent.set_image(self.parent.blue_image, self.Original_Label2, "blue", mask=False)
        self.Repeat_Red=False
        self.Repeat_Green=False
        self.Repeat_Blue=False
    
    def back_binary(self):
        self.parent.set_image(self.parent.red_mask, self.Filtred_Label, "red", mask=False)
        self.parent.set_image(self.parent.green_mask, self.Filtred_Label1, "green", mask=False)
        self.parent.set_image(self.parent.blue_mask, self.Filtred_Label2, "blue", mask=False)
    
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
    
    def control(self, number):
        error=False
        if (self.valore==0):
            self.setEnabled_True_Button()
        for i in range (0, self.valore):
            if(self.selezioni[i]==number):
                self.error_message("Choice already selected, delete one to continue")
                error=True
        return error
    
    def set_edit_remove(self):
        if(self.control(1)==False):
            self.valore=self.valore+1
            self.selezioni[(self.valore-1)]=1
            self.Remove_edit.setText(str(self.valore))
    
    def set_edit_erosion(self):
        if(self.control(2)==False):
            self.valore=self.valore+1
            self.selezioni[(self.valore-1)]=2
            self.Erosion_edit.setText(str(self.valore))
    
    def set_edit_dilation(self):
        if(self.control(3)==False):
            self.valore=self.valore+1
            self.selezioni[(self.valore-1)]=3
            self.Dilation_edit.setText(str(self.valore))
    
    def set_edit_open(self):
        if(self.control(4)==False):
            self.valore=self.valore+1
            self.selezioni[(self.valore-1)]=4
            self.Open_edit.setText(str(self.valore))
    
    def set_edit_close(self):
        if(self.control(5)==False):
            self.valore=self.valore+1
            self.selezioni[(self.valore-1)]=5
            self.Close_edit.setText(str(self.valore))
        
    def apply_segmentation(self):
        self.notRed=True
        self.notGreen=True
        self.notBlue=True
        error=False
        if self.radioRed.isChecked():
            if(self.parent.red_mask is None):
                self.error_message("Binarize red image")
                error=True
            if(self.Repeat_Red):
                self.mask_red=None
        if self.radioGreen.isChecked():
            if(self.parent.green_mask is None):
                self.error_message("Binarize green image")
                error=True
            if(self.Repeat_Green):
                self.mask_green=None
        if self.radioBlue.isChecked():
            if(self.parent.blue_mask is None):
                self.error_message("Binarize blue image")
                error=True
            if(self.Repeat_Blue):
                self.mask_green=None
        if (error is False):
            for i in range (0,5):
                if (self.selezioni[i]==1):
                    raggio=self.Raggio.value()
                    if raggio==0:
                        self.error_message("Insert a radius!")
                        error=True
                    elif (self.radioRed.isChecked() and error==False):
                        if(self.mask_red is not None):
                            self.mask_red= morphology.remove_small_objects(self.mask_red.astype(np.bool), raggio)
                        else:
                            self.mask_red= morphology.remove_small_objects(self.parent.red_mask.astype(np.bool), raggio)
                        self.notRed=False
                        self.parent.set_image(self.mask_red, self.Filtred_Label, "red", mask=True)
                    if (self.radioGreen.isChecked() and error==False):
                        if(self.mask_green is not None):
                            self.mask_green= morphology.remove_small_objects(self.mask_green.astype(np.bool), raggio)
                        else:
                            self.mask_green= morphology.remove_small_objects(self.parent.green_mask.astype(np.bool), raggio)
                        self.notGreen=False
                        self.parent.set_image(self.mask_green, self.Filtred_Label1, "green", mask=True)
                    elif (self.radioBlue.isChecked() and error==False):
                        raggio=self.Raggio.value()
                        if (self.mask_blue is not None):
                            self.mask_blue= morphology.remove_small_objects(self.mask_blue.astype(np.bool), raggio)
                        else:
                            self.mask_blue= morphology.remove_small_objects(self.parent.blue_mask.astype(np.bool), raggio)
                        self.notBlue=False
                        self.parent.set_image(self.mask_blue, self.Filtred_Label2, "blue", mask=True) 
                elif (self.selezioni[i]==2 and error==False):
                    if self.radioRed.isChecked():
                        if(self.mask_blue is not None):
                            self.mask_red=morphology.binary_erosion(self.mask_red)
                        else:
                            self.mask_red=morphology.binary_erosion(self.parent.red_mask)
                        self.notRed=False
                        self.parent.set_image(self.mask_red, self.Filtred_Label, "red", mask=True)
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
                elif (self.selezioni[i]==3 and error==False):
                    if self.radioRed.isChecked():
                        if(self.mask_blue is not None):
                            self.mask_red=morphology.binary_dilation(self.mask_red)
                        else:
                            self.mask_red=morphology.binary_dilation(self.parent.red_mask)
                        self.notRed=False
                        self.parent.set_image(self.mask_red, self.Filtred_Label, "red", mask=True)
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
                elif (self.selezioni[i]==4 and error==False):
                    if self.radioRed.isChecked():
                        if(self.mask_blue is not None):
                            self.mask_red=morphology.binary_opening(self.mask_red)
                        else:
                            self.mask_red=morphology.binary_opening(self.parent.red_mask)
                        self.notRed=False
                        self.parent.set_image(self.mask_red, self.Filtred_Label, "red", mask=True)
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
                elif (self.selezioni[i]==5 and error==False):
                    if self.radioRed.isChecked():
                        if(self.mask_blue is not None):
                            self.mask_red=morphology.binary_closing(self.mask_red)
                        else:
                            self.mask_red=morphology.binary_closing(self.parent.red_mask)
                        self.notRed=False
                        self.parent.set_image(self.mask_red, self.Filtred_Label, "red", mask=True)
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
            if(error==False):
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
        self.parent.set_image(self.parent.red_mask, self.parent.RED_QLabel, "red", mask=True)
        self.parent.set_image(self.parent.green_mask, self.parent.GREEN_QLabel, "green", mask=True)
        self.parent.set_image(self.parent.blue_mask, self.parent.BLUE_QLabel, "blue", mask=True)
    
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
    

