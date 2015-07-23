# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ConsoleWidget(QWidget):

    def __init__(self, parent=None):
        super(ConsoleWidget, self).__init__(parent)

        self.textEdit = QTextEdit()
        self.clearButton = QPushButton()
        self.clearButton.setText('Clear')

        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.addWidget(self.textEdit)
        self.vboxLayout.addWidget(self.clearButton)
        self.setLayout(self.vboxLayout)

        self.clearButton.clicked.connect(self.clearConsoleTexts)

    def clearConsoleTexts(self):
        self.textEdit.clear()

    @pyqtSlot()
    def consolOutput(self, msg):
        self.textEdit.append(msg)
