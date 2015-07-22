# -*- coding: utf-8 -*-

import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .. import hdr
from .. import tools
from .control_widget import ControlWidget
from .image_widget import ImageWidget
from .curve_plot_widget import CurvePlotWidget

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

        self.project = None

    def setSignalSlots(self):
        self.tabWidgets.tabCloseRequested.connect(self.closeTabRequested)
        self.controlWidget.loadPushButton.clicked.connect(self.loadPushButtonClicked)
        self.controlWidget.estimatePushButton.clicked.connect(self.estimatePushButtonClicked)

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
        filename = QFileDialog.getOpenFileName(self, 'Open project XML', lastOpenedDir, 'Project XML (*.xml)')[0]
        if filename == "":
            return

        self.rememberLastOpenedDirectory(filename)

        _, ext = os.path.splitext(filename)
        if ext == '.xml':
            self.project = tools.Project(filename)

        imgWidget = ImageWidget()
        imgWidget.showImage(self.project.image)
        self.tabWidgets.addTab(imgWidget, os.path.basename(filename))
        maskWidget = ImageWidget()
        maskWidget.showImage(self.project.mask)
        self.tabWidgets.addTab(maskWidget, 'Mask')

    def estimatePushButtonClicked(self):
        if self.project is None:
            self.showMessageBox('Load project first!')
            return

        de = tools.DepthEstimator(self.project.image, self.project.mask)
        de.process()
        de.save_mesh('depth_mesh.obj')

        le = tools.LightEstimator()
        le.process(self.project.image, self.project.mask)

        be = tools.BSSRDFEstimator()
        be.process(self.project.image, self.project.mask, de.depth, le.lights)

        cpw = CurvePlotWidget()
        cpw.setCurveData(be.Rd)
        self.tabWidgets.addTab(cpw, 'Curve')

    @classmethod
    def showMessageBox(cls, msg):
        msgbox = QMessageBox()
        msgbox.setText(msg)
        msgbox.exec_()
