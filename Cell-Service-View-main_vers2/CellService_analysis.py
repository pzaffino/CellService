from PyQt5.QtWidgets import QPushButton, QLabel, QWidget, QCheckBox, QVBoxLayout
import numpy as np

class CellServiceIntensityAnalysis(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Analysis")

        self.init_ui()
        #self.show()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.averageCheck = QCheckBox("Average")
        layout.addWidget(self.averageCheck)

        self.rangeCheck = QCheckBox("Min-max range")
        layout.addWidget(self.rangeCheck)

        self.averageLabel = QLabel(self)
        self.averageLabel.setText("Average intensities: Red -, Green -, Blue -")
        layout.addWidget(self.averageLabel)

        self.rangeLabel = QLabel(self)
        self.rangeLabel.setText("Intensity ranges (min/max): Red -, Green -, Blue -")
        layout.addWidget(self.rangeLabel)

        self.runComputationButton = QPushButton(self)
        self.runComputationButton.setText("Compute")
        self.runComputationButton.clicked.connect(self.runIntensityCompuation)
        layout.addWidget(self.runComputationButton)

    def runIntensityCompuation(self):

        # Reset report 
        self.averageLabel.setText("Average intensities: Red -, Green -, Blue -")
        self.rangeLabel.setText("Intensity ranges (min/max): Red -, Green -, Blue -")

        if self.averageCheck.isChecked():
            red_average = np.mean(self.parent.red_image)
            green_average = np.mean(self.parent.green_image)
            blue_average = np.mean(self.parent.blue_image)
            self.averageLabel.setText("Average intensities: Red %.1f, Green %.1f, Blue %.1f" % (red_average, green_average, blue_average))
        if self.rangeCheck.isChecked():
            self.rangeLabel.setText("Intensity ranges (min/max): Red %.1f/%.1f, Green %.1f/%.1f, Blue %.1f/%.1f" % (
                                    np.min(self.parent.red_image), np.max(self.parent.red_image),
                                    np.min(self.parent.green_image), np.max(self.parent.green_image),
                                    np.min(self.parent.blue_image), np.max(self.parent.blue_image)))

