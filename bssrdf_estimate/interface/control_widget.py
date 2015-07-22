# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ParameterWidget(QWidget):
    def __init__(self, parent=None):
        super(ParameterWidget, self).__init__(parent)

        self.formLayout = QFormLayout()

        self.widthLineEdit = QLineEdit()
        self.widthLineEdit.setMaximumWidth(100)
        self.widthLineEdit.setText('800')
        self.formLayout.addRow('width', self.widthLineEdit)

        self.heightLineEdit = QLineEdit()
        self.heightLineEdit.setMaximumWidth(100)
        self.heightLineEdit.setText('600')
        self.formLayout.addRow('height', self.heightLineEdit)

        self.sppLineEdit = QLineEdit()
        self.sppLineEdit.setMaximumWidth(100)
        self.sppLineEdit.setText('1')
        self.formLayout.addRow('samples', self.sppLineEdit)

        self.nphotonLineEdit = QLineEdit()
        self.nphotonLineEdit.setMaximumWidth(100)
        self.nphotonLineEdit.setText('1000000')
        self.formLayout.addRow('photons', self.nphotonLineEdit)

        self.scaleLineEdit = QLineEdit()
        self.scaleLineEdit.setMaximumWidth(100)
        self.scaleLineEdit.setText('0.01')
        self.formLayout.addRow('scale', self.scaleLineEdit)

        self.setLayout(self.formLayout)

class ControlWidget(QWidget):
    def __init__(self, parent=None):
        super(ControlWidget, self).__init__(parent)

        self.paramWidget = ParameterWidget()

        self.loadPushButton = QPushButton()
        self.loadPushButton.setMaximumWidth(100)
        self.loadPushButton.setText('Load')

        self.estimatePushButton = QPushButton()
        self.estimatePushButton.setMaximumWidth(100)
        self.estimatePushButton.setText('Estimate')

        self.renderPushButton = QPushButton()
        self.renderPushButton.setMaximumWidth(100)
        self.renderPushButton.setText('Render')

        self.boxLayout = QVBoxLayout()
        self.boxLayout.addWidget(self.paramWidget)
        self.boxLayout.addWidget(self.loadPushButton)
        self.boxLayout.addWidget(self.estimatePushButton)
        self.boxLayout.addWidget(self.renderPushButton)
        self.setLayout(self.boxLayout)

    def getWidthValue(self):
        return int(self.paramWidget.widthLineEdit.text())

    def getHeightValue(self):
        return int(self.paramWidget.heightLineEdit.text())

    def getSamplePerPixel(self):
        return int(self.paramWidget.sppLineEdit.text())

    def getNumberOfPhotons(self):
        return int(self.paramWidget.nphotonLineEdit.text())

    def getScale(self):
        return float(self.paramWidget.scaleLineEdit.text())
