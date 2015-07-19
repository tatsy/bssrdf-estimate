# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ControlWidget(QWidget):
    def __init__(self, parent=None):
        super(ControlWidget, self).__init__(parent)

        self.loadPushButton = QPushButton()
        self.loadPushButton.setText('Load')

        self.boxLayout = QVBoxLayout()
        self.boxLayout.addWidget(self.loadPushButton)
        self.setLayout(self.boxLayout)
