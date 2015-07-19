# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.estimateButton = QPushButton()
        self.estimateButton.setText('Estimate')
        self.estimateButton.clicked.connect(self.estimateButtonClicked)

        self.boxLayout = QVBoxLayout()
        self.boxLayout.addWidget(self.estimateButton)
        self.setLayout(self.boxLayout)

    def estimateButtonClicked(self):
        print('Estimate')
