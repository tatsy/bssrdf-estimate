# -*- coding: utf-8 -*-

import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .. import hdr
from .control_widget import ControlWidget
from .image_widget import ImageWidget

config_file = 'config.ini'

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('BSSRDF Estimate')

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

    @classmethod
    def rememberLastOpenedDirectory(cls, filename):
        d = os.path.dirname(filename)
        with open(config_file, 'w') as f:
            f.write(d)

    @classmethod
    def getLastOpenedDirectory(cls):
        d = ''
        if os.path.isfile(config_file):
            with open(config_file, 'r') as f:
                d = f.readline()
        return d

    def closeTabRequested(self, index):
        self.tabWidgets.removeTab(index)

    def loadPushButtonClicked(self):
        lastOpenedDir = self.getLastOpenedDirectory()
        filename = QFileDialog.getOpenFileName(self, 'Open HDR', lastOpenedDir, 'HDR (*.hdr)')[0]
        if filename == "":
            return

        self.rememberLastOpenedDirectory(filename)

        _, ext = os.path.splitext(filename)
        if ext == '.hdr':
            img = hdr.load(filename)
            img = hdr.tonemap(img)
        else:
            img = sp.misc.imread(filename)

        imgWidget = ImageWidget()
        imgWidget.showImage(img)
        self.tabWidgets.addTab(imgWidget, os.path.basename(filename))
