from PyQt5.QtWidgets import (QMessageBox, QMainWindow)
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
import numpy as np
from skimage import filters, morphology

class Processing_cellService(QMainWindow):
    
    def __init__(self, parent):
        super().__init__()
        
        self.filtred_red_mask=None
        self.filtred_green_mask=None
        self.filtred_blue_mask=None
        self.clear=False
        
        self.parent = parent
        self.setWindowTitle("Processing")
        
        self.setupUI()
        self.binary_processing()
        self.set_segmentation()
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)
        
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
        self.radioRed.setText("Red Image")
        self.radioRed.setChecked(True)
        self.radioRed.setGeometry(QtCore.QRect(320, 20, 101, 20))
        self.radioRed.setStyleSheet("font: 8pt \"Arial\";\n" "color: red;\n")
        self.radioGreen = QtWidgets.QRadioButton(self.principal_widget)
        self.radioGreen.setText("Green Image")
        self.radioGreen.setGeometry(QtCore.QRect(490, 20, 101, 20))
        self.radioGreen.setStyleSheet("font: 8pt \"Arial\";\n" "color: Green;")
        self.radioBlue = QtWidgets.QRadioButton(self.principal_widget)
        self.radioBlue.setGeometry(QtCore.QRect(670, 20, 101, 20))
        self.radioBlue.setStyleSheet("font: 8pt \"Arial\";\n" "color: Blue;")
        self.radioBlue.setText("Blue Image")
        
        self.help_button = QtWidgets.QPushButton(self.principal_widget)
        self.help_button.setGraphicsEffect(self.applyShadow())
        self.help_button.setGeometry(QtCore.QRect(880, 720, 41, 41))
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
        icon2.addPixmap(QtGui.QPixmap("Icon/help_page.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.help_button.setIcon(icon2)
        self.help_button.setIconSize(QtCore.QSize(65, 30))
        self.help_button.clicked.connect(self.help_message)
        self.help_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Help </span></p></body></html>")
        self.help_button.setStatusTip("Help")
       
        self.save_button = QtWidgets.QPushButton(self.principal_widget)
        self.save_button.setGraphicsEffect(self.applyShadow())
        self.save_button.setGeometry(QtCore.QRect(950, 720, 41, 41))
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
        icon3.addPixmap(QtGui.QPixmap("Icon/images (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_button.setIcon(icon3)
        self.save_button.setIconSize(QtCore.QSize(65, 30))
        self.save_button.clicked.connect(self.save)
        self.save_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Save all changes</span></p></body></html>")
        self.save_button.setStatusTip("Save all changes")
        
        self.delete_button = QtWidgets.QPushButton(self.principal_widget)
        self.delete_button.setGraphicsEffect(self.applyShadow())
        self.delete_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Delete </span></p></body></html>")
        self.delete_button.setStatusTip("Delete")
        self.delete_button.setGeometry(QtCore.QRect(1020, 720, 41, 41))
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
        icon1.addPixmap(QtGui.QPixmap("Icon/canc_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_button.setIcon(icon1)
        self.delete_button.setIconSize(QtCore.QSize(35, 30))
        self.delete_button.clicked.connect(self.deleteall_message)
        self.setCentralWidget(self.principal_widget)
        
        self.selezioni=np.array([0,0,0,0,0])
        self.valore=0
        self.set_all_images()

    def set_segmentation(self):
        self.segmentation_widget = QtWidgets.QWidget(self.principal_widget)
        self.segmentation_widget.setGeometry(QtCore.QRect(840, 50, 245, 630))
        self.segmentation_widget.setGraphicsEffect(self.applyShadow())
        self.segmentation_widget.setStyleSheet("background-color: rgb(255, 255, 255);\n" "border-radius: 35px;")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Icon/accept.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.Add_button = QtWidgets.QPushButton(self.segmentation_widget)
        self.Add_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Add Changes to the filtred image</span></p></body></html>")
        self.Add_button.setStatusTip("Add Changes to the filtred image")
        self.Add_button.clicked.connect(self.apply_segmentation)
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
        self.Add_button.setIconSize(QtCore.QSize(30, 35))
        icon_not = QtGui.QIcon()
        icon_not.addPixmap(QtGui.QPixmap("Icon/not_accept.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.No_button = QtWidgets.QPushButton(self.segmentation_widget)
        self.No_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Not Changes to the filtred image</span></p></body></html>")
        self.No_button.setStatusTip("Not Changed")
        self.No_button.clicked.connect(self.clear_edit_label)
        self.No_button.setGraphicsEffect(self.applyShadow())
        self.No_button.setGeometry(QtCore.QRect(150, 470, 41, 41))
        self.No_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.No_button.setStyleSheet("QPushButton {\n"
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
        self.No_button.setIcon(icon_not)
        self.No_button.setIconSize(QtCore.QSize(30, 35))
        self.Undo_button = QtWidgets.QPushButton(self.segmentation_widget)
        self.Undo_button.setGraphicsEffect(self.applyShadow())
        self.Undo_button.setToolTip("<html><head/><body><p><span style=\" color:#80b7ff;\">Undo Change</span></p></body></html>")
        self.Undo_button.setStatusTip("Undo change")
        self.Undo_button.clicked.connect(self.back)
        self.Undo_button.setGeometry(QtCore.QRect(100, 550, 41, 41))
        self.Undo_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Undo_button.setStyleSheet("QPushButton {\n"
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
        icon4.addPixmap(QtGui.QPixmap("Icon/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Undo_button.setIcon(icon4)
        self.Undo_button.setIconSize(QtCore.QSize(30, 35))

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
        self.segmentation_edit.setGeometry(QtCore.QRect(0, 0, 245, 41))
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
        self.Add_title.setGeometry(QtCore.QRect(30, 513, 91, 21))
        self.Add_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.Add_title.setText("Apply Change")
        self.No_title = QtWidgets.QLabel(self.segmentation_widget)
        self.No_title.setGeometry(QtCore.QRect(140, 513, 91, 21))
        self.No_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.No_title.setText("Not Change")
        
        self.undo_title = QtWidgets.QLabel(self.segmentation_widget)
        self.undo_title.setGeometry(QtCore.QRect(90, 593, 121, 21))
        self.undo_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.undo_title.setText("Undo Change")
        
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
        self.Raggio.setGeometry(QtCore.QRect(140, 60, 91, 31))
        self.Raggio.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "border: 2px solid rgb(128, 183, 255);\n"
            "    border-radius: 15px;\n"
            "    font: bold 14px;\n"
            "    padding: 6px;\n"
            "font: 10pt \"Varela\";\n"
            "color: blue;")
        self.Raggio.setDecimals(3)
        self.Raggio.setMaximum(500.0)
        self.Radius_title = QtWidgets.QLineEdit(self.segmentation_widget)
        self.Radius_title.setGeometry(QtCore.QRect(15, 60, 121, 31))
        self.Radius_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.Radius_title.setReadOnly(True)
        self.Radius_title.setText("Minimum island size")
        
        self.setEnabled_Button(False)
        self.Undo_button.setEnabled(False)
        
    def binary_processing(self):
        self.binary_widget = QtWidgets.QWidget(self.principal_widget)
        self.binary_widget.setGeometry(QtCore.QRect(10, 60, 241, 361))
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
        self.Min_Label.setText("Min Threshold")
        self.Min_Label.setGeometry(QtCore.QRect(100, 30, 111, 31))
        self.Min_Label.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.Max_Label = QtWidgets.QLabel(self.binary_widget_3)
        self.Max_Label.setGeometry(QtCore.QRect(100, 70, 111, 31))
        self.Max_Label.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.Max_Label.setText("Max Threshold")
        
        self.fontSizeSpinBox = QtWidgets.QDoubleSpinBox(self.binary_widget_3)
        self.fontSizeSpinBox.setGeometry(QtCore.QRect(10, 30, 91, 31))
        self.fontSizeSpinBox.setDecimals(2)
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
        self.fontSizeSpinBox2.setDecimals(2)
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
        self.automatic_button.setGeometry(QtCore.QRect(90, 273, 41, 41))
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
        self.apply.setGeometry(QtCore.QRect(90, 200, 41, 41))
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
        self.Automatic_title.setGeometry(QtCore.QRect(50, 315, 131, 21))
        self.Automatic_title.setStyleSheet("font: 8pt \"Arial\";\n" "color: rgb(19, 82, 255);")
        self.Automatic_title.setText("Automatic Threshold")
        self.Apply_title = QtWidgets.QLabel(self.binary_widget)
        self.Apply_title.setText("Binarize Image")
        self.Apply_title.setGeometry(QtCore.QRect(70, 242, 101, 21))
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
    
    def runIntensityBinarization(self):
        if self.radioRed.isChecked():
            if (self.parent.red_image is None):
                self.error_message("Missing red image! Insert an image")
            else:
                self.mask=self.binarizeImage(self.parent.red_image)
                if (self.mask is not None):
                    self.parent.red_mask = self.mask
                    self.parent.set_image(self.parent.red_mask, self.Filtred_Label, "red", mask=True)
        elif self.radioGreen.isChecked():
            if (self.parent.green_image is None):
                self.error_message("Missing green image! Insert an image")
            else:
                self.mask=self.binarizeImage(self.parent.green_image)
                if (self.mask is not None):
                    self.parent.green_mask = self.mask
                    self.parent.set_image(self.parent.green_mask, self.Filtred_Label1, "green", mask=True)
        elif self.radioBlue.isChecked():
            if (self.parent.blue_image is None):
                self.error_message("Missing blue image! Insert an image")
            else:
                self.mask=self.binarizeImage(self.parent.blue_image)
                if (self.mask is not None):
                    self.parent.blue_mask = self.mask
                    self.parent.set_image(self.parent.blue_mask, self.Filtred_Label2, "blue", mask=True)
        else:
            pass
    
    def Automatic_threshold(self):
        self.soglia1=0
        if self.radioRed.isChecked():
            if(self.parent.red_image is None):
                self.error_message("Missing red image! Upload image to continue.")
            else:
                self.soglia1 = filters.threshold_otsu(self.parent.red_image)
        elif self.radioGreen.isChecked():
            if(self.parent.green_image is None):
                self.error_message("Missing green image! Upload image to continue.")
            else:
                self.soglia1 = filters.threshold_otsu(self.parent.green_image)
        elif self.radioBlue.isChecked():
            if(self.parent.blue_image is None):
                self.error_message("Missing blue image! Upload image to continue.")
            else:
                self.soglia1 = filters.threshold_otsu(self.parent.blue_image)
        else:
            pass
        if (self.soglia1!=0):
            self.fontSizeSpinBox.setValue(self.soglia1)
            self.runIntensityBinarization()
    
    def binarizeImage(self,img):
        valore1 = self.fontSizeSpinBox.value()
        valore2 =self.fontSizeSpinBox2.value()
        binarymat = np.zeros_like(img, dtype=np.uint8)
        if (valore1==0):
            self.error_message("Insert a minimum threshold")
        else:
            if (valore2!=0):
                mask=np.logical_and(img > valore1, img < valore2)
                binarymat[mask]=1
            if (valore2==0):
                mask=img>valore1
                binarymat[mask]=1
            return binarymat
    
    def control(self, number):
        error=False
        for i in range (0, self.valore):
            if(self.selezioni[i]==number):
                self.error_message("Choice already selected, delete one to continue")
                error=True
        if(error==False):
            self.No_button.setEnabled(True)
        return error
    
    def set_edit_remove(self):
        if(self.control(1)==False):
            self.valore=self.valore+1
            self.selezioni[(self.valore-1)]=1
            self.Remove_edit.setText(str(self.valore))
            self.Remove_canc.setEnabled(True)
    
    def set_edit_erosion(self):
        if(self.control(2)==False):
            self.valore=self.valore+1
            self.selezioni[(self.valore-1)]=2
            self.Erosion_edit.setText(str(self.valore))
            self.Erosion_canc.setEnabled(True)
    
    def set_edit_dilation(self):
        if(self.control(3)==False):
            self.valore=self.valore+1
            self.selezioni[(self.valore-1)]=3
            self.Dilation_edit.setText(str(self.valore))
            self.Dilation_canc.setEnabled(True)
    
    def set_edit_open(self):
        if(self.control(4)==False):
            self.valore=self.valore+1
            self.selezioni[(self.valore-1)]=4
            self.Open_edit.setText(str(self.valore))
            self.Open_canc.setEnabled(True)
    
    def set_edit_close(self):
        if(self.control(5)==False):
            self.valore=self.valore+1
            self.selezioni[(self.valore-1)]=5
            self.Close_edit.setText(str(self.valore))
            self.Close_canc.setEnabled(True)
    
    #controlla errori prima di procedere per la segmentazione
    def TrueORFalse_error(self,mask):
        error=False
        if mask is None:
            self.error_message("Binarize this image")
            error=True
        for i in range (0,5):
            if(self.selezioni[i]==1):
                self.raggio=self.Raggio.value()
                if self.raggio==0:
                    self.error_message("Insert a minimum island size!")
                    error=True
        return error
    
    #applica segmentazione dato che non ci sono errori
    def segmentation_RadioButton(self, mask):
        self.clear=False
        self.Undo_button.setEnabled(True)
        for i in range (0,5): #scorrere il vettore delle selezioni per svolgere in ordine quanto richiesto
            if (self.selezioni[i]==1):
                mask=morphology.remove_small_objects(mask.astype(np.bool), self.raggio)
            elif (self.selezioni[i]==2):
                mask=morphology.binary_erosion(mask)
            elif (self.selezioni[i]==3):
                mask=morphology.binary_dilation(mask)
            elif (self.selezioni[i]==4):
                mask=morphology.binary_opening(mask)
            elif (self.selezioni[i]==5):
                mask=morphology.binary_closing(mask)
        return mask
    
    #scelta immagine da segmentare, richiama le due precedenti applicandole alle immagini selezionate
    def apply_segmentation(self):
        error=False
        if self.radioRed.isChecked():
            error=self.TrueORFalse_error(self.parent.red_mask)
            if(error==False):
                self.filtred_red_mask=self.parent.red_mask
                self.parent.red_mask=self.segmentation_RadioButton(self.parent.red_mask)
                self.parent.set_image(self.parent.red_mask, self.Filtred_Label, "red", mask=True)
        if self.radioGreen.isChecked():
            error=self.TrueORFalse_error(self.parent.green_mask)
            if(error==False):
                self.filtred_green_mask=self.parent.green_mask
                self.parent.green_mask=self.segmentation_RadioButton(self.parent.green_mask)
                self.parent.set_image(self.parent.green_mask, self.Filtred_Label1, "green", mask=True)
        if self.radioBlue.isChecked():
            error=self.TrueORFalse_error(self.parent.blue_mask)
            if(error==False):
                self.filtred_blue_mask=self.parent.blue_mask
                self.parent.blue_mask=self.segmentation_RadioButton(self.parent.blue_mask)
                self.parent.set_image(self.parent.blue_mask, self.Filtred_Label2, "blue", mask=True)
        if(error==False):
            self.clear_edit_label() #ripulisce label numerazione dopo aver apportato modifiche
    
    #delete numeration
    def clear_edit_label(self):
        self.valore=0
        self.selezioni=np.array([0,0,0,0,0])
        self.Remove_edit.clear()
        self.Erosion_edit.clear()
        self.Dilation_edit.clear()
        self.Open_edit.clear()
        self.Close_edit.clear()
        self.setEnabled_Button(False)
    
    #delete all
    def Clear_filtred_label(self):
        self.Filtred_Label.clear()
        self.Filtred_Label1.clear()
        self.Filtred_Label2.clear()
        self.clear_edit_label()
        self.filtred_red_mask=self.parent.red_mask
        self.filtred_green_mask=self.parent.green_mask
        self.filtred_blue_mask=self.parent.blue_mask
        self.parent.red_mask=None
        self.parent.green_mask=None
        self.parent.blue_mask=None
        self.clear=True
        self.Undo_button.setEnabled(True)
        
    #back to the last segmentation
    def back(self):
        if (self.clear): #se in passato è stato cancellato tutto allora riportami al cambiamento più recente
            self.parent.red_mask=self.filtred_red_mask
            self.parent.set_image(self.parent.red_mask, self.Filtred_Label, "red", mask=True)
            self.parent.green_mask=self.filtred_green_mask
            self.parent.set_image(self.parent.green_mask, self.Filtred_Label1, "green", mask=True)
            self.parent.blue_mask=self.filtred_blue_mask
            self.parent.set_image(self.parent.blue_mask, self.Filtred_Label2, "blue", mask=True)
            self.clear=False
        elif(self.radioRed.isChecked()):
            self.parent.red_mask=self.filtred_red_mask
            self.parent.set_image(self.parent.red_mask, self.Filtred_Label, "red", mask=True)
        elif(self.radioGreen.isChecked()):
            self.parent.green_mask=self.filtred_green_mask
            self.parent.set_image(self.parent.green_mask, self.Filtred_Label1, "green", mask=True)
        elif(self.radioBlue.isChecked()):
            self.parent.blue_mask=self.filtred_blue_mask
            self.parent.set_image(self.parent.blue_mask, self.Filtred_Label2, "blue", mask=True)
        self.Undo_button.setEnabled(False)
    
    #attivare/disattivare button canc
    def setEnabled_Button(self, b):
        self.Remove_canc.setEnabled(b)
        self.Dilation_canc.setEnabled(b)
        self.Erosion_canc.setEnabled(b)
        self.Open_canc.setEnabled(b)
        self.Close_canc.setEnabled(b)
        self.No_button.setEnabled(b)

    #canc button
    def delete_edit_remove(self):
        self.delete(self.Remove_edit)
        self.Remove_edit.clear()
        self.Remove_canc.setEnabled(False)
        
    def delete_edit_erosion(self):
        self.delete(self.Erosion_edit)
        self.Erosion_edit.clear()
        self.Erosion_canc.setEnabled(False)
    
    def delete_edit_dilation(self):
        self.delete(self.Dilation_edit)
        self.Dilation_edit.clear()
        self.Dilation_canc.setEnabled(False)
    
    def delete_edit_open(self):
        self.delete(self.Open_edit)
        self.Open_edit.clear()
        self.Open_canc.setEnabled(False)
    
    def delete_edit_close(self):
        self.delete(self.Close_edit)
        self.Close_edit.clear()
        self.Close_canc.setEnabled(False)
        
    def delete(self, label):
        current_number=int(label.text())-1 #legge numero dalla label
        for i in range (current_number, (len(self.selezioni))): #scala tutto ciò che sta dopo questo numero (valore corrente-1)
            if(i==(len(self.selezioni)-1)):
                self.selezioni[i]=0
            else:
                self.selezioni[i]=self.selezioni[i+1]
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
        self.valore=self.valore-1
        if (self.valore==0):
            self.setEnabled_Button(False)
    
    #save all
    def save(self):
        if((self.parent.red_mask is None) and (self.parent.green_mask is None) and (self.parent.blue_mask is None)):
            self.error_message("Attention: the images haven't been binarized")
        else:
            self.parent.set_image(self.parent.red_mask, self.parent.RED_QLabel, "red", mask=True)
            self.parent.set_image(self.parent.green_mask, self.parent.GREEN_QLabel, "green", mask=True)
            self.parent.set_image(self.parent.blue_mask, self.parent.BLUE_QLabel, "blue", mask=True)
            
    def deleteall_message(self):
        mbox = QMessageBox(self)
        mbox.setIcon(QMessageBox.Question)
        mbox.setWindowTitle("Delete All Dialog")
        mbox.setText("Do you want to delete your changes?")
        mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        returnValue = mbox.exec()
        if returnValue == QMessageBox.Yes:
            self.Clear_filtred_label()
        else:
            pass
        
    def error_message(self, text_error):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(text_error)
        msg.setWindowTitle("Error")
        msg.exec_()
        
    def remove_message(self):
        mbox = QMessageBox(self)
        mbox.setIcon(QMessageBox.Information)
        mbox.setWindowTitle("Remove Help")
        mbox.setText("What does it?")
        mbox.setInformativeText("Remove objects smaller than the specified size.")
        mbox.exec_()
    
    def dilation_message(self):
        mbox = QMessageBox(self)
        mbox.setIcon(QMessageBox.Information)
        mbox.setWindowTitle("Dilation Help")
        mbox.setText("What does it?")
        mbox.setInformativeText("Dilation enlarges bright regions and shrinks dark regions.")
        mbox.exec_()
    
    def erosion_message(self):
        mbox = QMessageBox(self)
        mbox.setIcon(QMessageBox.Information)
        mbox.setWindowTitle("Erosion Help")
        mbox.setText("What does it?")
        mbox.setInformativeText("Erosion shrinks bright regions and enlarges dark regions.")
        mbox.exec_()
    
    def open_message(self):
        mbox = QMessageBox(self)
        mbox.setIcon(QMessageBox.Information)
        mbox.setWindowTitle("Opening Help")
        mbox.setText("What does it?")
        mbox.setInformativeText("The morphological opening on an image is defined as an erosion followed by a dilation. Opening can remove small bright spots (i.e. “salt”) and connect small dark cracks. This tends to “open” up (dark) gaps between (bright) features")
        mbox.exec_()
    
    def close_message(self):
        mbox = QMessageBox(self)
        mbox.setIcon(QMessageBox.Information)
        mbox.setWindowTitle("Closing Help")
        mbox.setText("What does it?")
        mbox.setInformativeText("The morphological closing on an image is defined as a dilation followed by an erosion. Closing can remove small dark spots (i.e. “pepper”) and connect small bright cracks. This tends to “close” up (dark) gaps between (bright) features.")
        mbox.exec_()
    
    def help_message(self):
        mbox = QMessageBox(self)
        mbox.setIcon(QMessageBox.Information)
        mbox.setWindowTitle("Help")
        mbox.setText("Processing")
        mbox.setInformativeText ("In the field of image processing, the ability to distinguish different objects, shapes and contours present in the image under analysis plays a fundamental role. This is possible thanks to thresholding techniques: techniques that consider pixels with intensity higher than a minimum threshold and, if this is present, lower than a maximum threshold. In this case, the threshold can be set by the user (choosing a minimum threshold and a maximum threshold of intensity of the pixels to be considered). If you don't know which one to choose, you can use the automatic threshold method: this uses the Otsu threshold to choose a minimum threshold, but does not set any maximum threshold. Remember to choose the image to binarize before applying the threshold to the images and to confirm the choice with the Binarize image button to apply the thresholding.")
        mbox.exec_()
    

