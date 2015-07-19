# -*- coding: utf-8 -*-

import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .control_widget import ControlWidget
from .image_widget import ImageWidget

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.tabWidgets = QTabWidget()
        self.tabWidgets.setTabsClosable(True)

        self.controlWidget = ControlWidget()

        self.setSignalSlots()

        self.boxLayout = QHBoxLayout()
        self.boxLayout.addWidget(self.tabWidgets)
        self.boxLayout.addWidget(self.controlWidget)
        self.setLayout(self.boxLayout)

    def setSignalSlots(self):
        self.tabWidgets.tabCloseRequested.connect(self.closeTabRequested)
        self.controlWidget.loadPushButton.clicked.connect(self.loadPushButtonClicked)

    def closeTabRequested(self, index):
        self.tabWidgets.removeTab(index)

    def loadPushButtonClicked(self):
        filename = QFileDialog.getOpenFileName()[0]
        if filename == "":
            return

        img = QImage(filename)

        imgWidget = ImageWidget()
        imgWidget.showImage(img)
        self.tabWidgets.addTab(imgWidget, os.path.basename(filename))
