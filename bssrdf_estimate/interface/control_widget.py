# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ParameterWidget(QWidget):
    def __init__(self, parent=None):
        super(ParameterWidget, self).__init__(parent)

        self.formLayout = QFormLayout()

        self.widthLineEdit = QLineEdit()
        self.widthLineEdit.setText('800')
        self.formLayout.addRow('width', self.widthLineEdit)

        self.heightLineEdit = QLineEdit()
        self.heightLineEdit.setText('600')
        self.formLayout.addRow('height', self.heightLineEdit)

        self.sppLineEdit = QLineEdit()
        self.sppLineEdit.setText('1')
        self.formLayout.addRow('samples', self.sppLineEdit)

        self.nphotonLineEdit = QLineEdit()
        self.nphotonLineEdit.setText('1000000')
        self.formLayout.addRow('photons', self.nphotonLineEdit)

        self.scaleLineEdit = QLineEdit()
        self.scaleLineEdit.setText('0.01')
        self.formLayout.addRow('scale', self.scaleLineEdit)

        self.setLayout(self.formLayout)

class ControlWidget(QWidget):
    def __init__(self, parent=None):
        super(ControlWidget, self).__init__(parent)

        self.paramWidget = ParameterWidget()

        self.loadPushButton = QPushButton()
        self.loadPushButton.setText('Load')

        self.estimatePushButton = QPushButton()
        self.estimatePushButton.setText('Estimate')

        self.renderPushButton = QPushButton()
        self.renderPushButton.setText('Render')

        self.boxLayout = QVBoxLayout()
        self.boxLayout.addWidget(self.paramWidget)
        self.boxLayout.addWidget(self.loadPushButton)
        self.boxLayout.addWidget(self.estimatePushButton)
        self.boxLayout.addWidget(self.renderPushButton)
        self.setLayout(self.boxLayout)

    @property
    def width_value(self):
        return int(self.paramWidget.widthLineEdit.text())

    @width_value.setter
    def width_value(self, value):
        self.paramWidget.widthLineEdit.setText(str(value))

    @property
    def height_value(self):
        return int(self.paramWidget.heightLineEdit.text())

    @height_value.setter
    def height_value(self, value):
        self.paramWidget.heightLineEdit.setText(str(value))

    @property
    def sample_per_pixel(self):
        return int(self.paramWidget.sppLineEdit.text())

    @sample_per_pixel.setter
    def sample_per_pixel(self, value):
        self.paramWidget.sppLineEdit.setText(str(value))

    @property
    def num_photons(self):
        return int(self.paramWidget.nphotonLineEdit.text())

    @num_photons.setter
    def num_photons(self, value):
        self.paramWidget.nphotonLineEdit.setText(str(value))

    @property
    def bssrdf_scale(self):
        return float(self.paramWidget.scaleLineEdit.text())

    @bssrdf_scale.setter
    def bssrdf_scale(self, value):
        self.paramWidget.scaleLineEdit.setText(str(value))
