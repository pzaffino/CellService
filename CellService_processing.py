from PyQt5.QtWidgets import QPushButton, QLabel, QWidget, QCheckBox, QVBoxLayout, QRadioButton, QLineEdit
import numpy as np

class CellServiceBinaryProcessing(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Binary processing")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.redRadioButton = QRadioButton("Red")
        layout.addWidget(self.redRadioButton)

        self.greenRadioButton = QRadioButton("Green")
        layout.addWidget(self.greenRadioButton)

        self.blueRadioButton = QRadioButton("Blue")
        layout.addWidget(self.blueRadioButton)

        self.QLineThreshold = QLineEdit(self)
        layout.addWidget(self.QLineThreshold)

        self.runBinarizationButton = QPushButton(self)
        self.runBinarizationButton.setText("Binarize")
        self.runBinarizationButton.clicked.connect(self.runIntensityBinarization)
        layout.addWidget(self.runBinarizationButton)

    def binarizeImage(self, img, thr):
        mask = np.zeros_like(img, dtype=np.uint8)
        mask[img>=thr]=255
        return mask

    def runIntensityBinarization(self):

        if self.redRadioButton.isChecked():
            self.parent.red_mask = self.binarizeImage(self.parent.red_image, int(self.QLineThreshold.text()))
            self.parent.set_image(self.parent.red_mask, self.parent.Red_QLabel, "red")
        elif self.greenRadioButton.isChecked():
            self.parent.green_mask = self.binarizeImage(self.parent.green_image, int(self.QLineThreshold.text()))
            self.parent.set_image(self.parent.green_mask, self.parent.Green_QLabel, "green")
        elif self.blueRadioButton.isChecked():
            self.parent.blue_mask = self.binarizeImage(self.parent.blue_image, int(self.QLineThreshold.text()))
            self.parent.set_image(self.parent.blue_mask, self.parent.Blue_QLabel, "blue")
        else:
            pass


