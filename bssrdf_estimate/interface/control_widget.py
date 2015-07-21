# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ControlWidget(QWidget):
    def __init__(self, parent=None):
        super(ControlWidget, self).__init__(parent)

        self.loadPushButton = QPushButton()
        self.loadPushButton.setText('Load')

        self.estimatePushButton = QPushButton()
        self.estimatePushButton.setText('Estimate')

        self.boxLayout = QVBoxLayout()
        self.boxLayout.addWidget(self.loadPushButton)
        self.boxLayout.addWidget(self.estimatePushButton)
        self.setLayout(self.boxLayout)
