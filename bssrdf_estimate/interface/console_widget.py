# -*- coding: utf-8 -*-

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import pyqtSlot

class ConsoleWidget(QWidget):

    def __init__(self, parent=None):
        super(ConsoleWidget, self).__init__(parent)

        self.textEdit = QTextEdit()
        self.textEdit.setFont(QFont('Consolas'))
        self.clearButton = QPushButton()
        self.clearButton.setText('Clear')

        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.addWidget(self.textEdit)
        self.vboxLayout.addWidget(self.clearButton)
        self.setLayout(self.vboxLayout)

        self.clearButton.clicked.connect(self.clearConsoleTexts)

    def clearConsoleTexts(self):
        self.textEdit.clear()

    @pyqtSlot(str)
    def consoleOutput(self, msg):
        self.textEdit.append(msg)
