# -*- coding: utf-8 -*-

import os
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from bssrdf_estimate import hdr
from bssrdf_estimate import tools
from bssrdf_estimate.render import render

from .control_widget import ControlWidget
from .image_widget import ImageWidget
from .curve_plot_widget import CurvePlotWidget

config_file = 'config.ini'

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('BSSRDF Estimate')
        self.boxLayout = QHBoxLayout()
        self.setFont(QFont('Meiryo UI'))

        self.tabWidgets = QTabWidget()
        self.tabWidgets.setTabsClosable(True)
        sizeForTabs = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizeForTabs.setHorizontalStretch(5)
        self.tabWidgets.setSizePolicy(sizeForTabs)
        self.boxLayout.addWidget(self.tabWidgets)

        self.controlWidget = ControlWidget()
        sizeForControls = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizeForControls.setHorizontalStretch(1)
        self.controlWidget.setSizePolicy(sizeForControls)
        self.boxLayout.addWidget(self.controlWidget)

        self.setSignalSlots()

        self.setLayout(self.boxLayout)

        self.project = None

    def setSignalSlots(self):
        self.tabWidgets.tabCloseRequested.connect(self.closeTabRequested)
        self.controlWidget.loadPushButton.clicked.connect(self.loadPushButtonClicked)
        self.controlWidget.estimatePushButton.clicked.connect(self.estimatePushButtonClicked)
        self.controlWidget.renderPushButton.clicked.connect(self.renderPushButtonClicked)

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

        de = tools.DepthEstimator(self.project.hdr, self.project.mask)
        de.process()
        de.save_mesh('depth_mesh.obj')

        le = tools.LightEstimator()
        le.process(self.project.image, self.project.mask)

        be = tools.BSSRDFEstimator()
        be.process(self.project.image, self.project.mask, de.depth, le.lights)

        cpw = CurvePlotWidget()
        cpw.setCurveData(be.Rd)
        self.tabWidgets.addTab(cpw, 'Curve')

        self.Rd_distances = np.array(be.Rd[0][0], dtype='float32')
        self.Rd_colors = np.zeros((self.Rd_distances.size, 3), dtype='float32')
        for c in range(3):
            self.Rd_colors[:,c] = np.array(be.Rd[c][1])

    def renderPushButtonClicked(self):
        w = self.controlWidget.getWidthValue()
        h = self.controlWidget.getHeightValue()
        spp = self.controlWidget.getSamplePerPixel()
        photons = self.controlWidget.getNumberOfPhotons()
        scale = self.controlWidget.getScale()

        render(w, h, spp, photons, scale, self.Rd_distances, self.Rd_colors)

    @classmethod
    def showMessageBox(cls, msg):
        msgbox = QMessageBox()
        msgbox.setText(msg)
        msgbox.exec_()
