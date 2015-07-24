# -*- coding: utf-8 -*-

import os
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import bssrdf_estimate.hdr as hdr
import bssrdf_estimate.tools as tools

from bssrdf_estimate.interface import *

config_file = 'config.ini'

class MainWindow(QWidget):
    ''' Main window of estimation system
    '''
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('BSSRDF Estimate')
        self.setFont(QFont('Meiryo UI'))

        self.boxLayout = QHBoxLayout()
        self.vboxLayout = QVBoxLayout()

        self.setLayout(self.vboxLayout)

        self.topContainer = QWidget()
        self.topContainer.setLayout(self.boxLayout)

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

        self.consoleWidget = ConsoleWidget()

        sizeForTop = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizeForTop.setVerticalStretch(3)
        self.topContainer.setSizePolicy(sizeForTop)
        sizeForConsole = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizeForConsole.setVerticalStretch(1)
        self.consoleWidget.setSizePolicy(sizeForConsole)

        self.vboxLayout.addWidget(self.topContainer)
        self.vboxLayout.addWidget(self.consoleWidget)

        self.setSignalSlots()

        self.project = None

    def setSignalSlots(self):
        self.tabWidgets.tabCloseRequested.connect(self.closeTabRequested)
        self.controlWidget.loadPushButton.clicked.connect(self.loadPushButtonClicked)
        self.controlWidget.estimatePushButton.clicked.connect(self.estimatePushButtonClicked)
        self.controlWidget.renderPushButton.clicked.connect(self.renderPushButtonClicked)

    def getOpenFileName(self):
        lastOpenedDir = self.getLastOpenedDirectory()
        filename = QFileDialog.getOpenFileName(self, 'Open project XML', lastOpenedDir, 'Project XML (*.xml)')[0]
        if filename == "":
            return ""
        self.rememberLastOpenedDirectory(filename)
        self.openedDirectory = os.path.dirname(filename)
        return filename

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
        filename = self.getOpenFileName()

        _ , ext = os.path.splitext(filename)
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
        cpw.setCurveData(be.bssrdf)
        self.tabWidgets.addTab(cpw, 'Curve')

        # Save BSSRDF file
        be.bssrdf.save(os.path.join(self.openedDirectory, 'Rd_curve.dat'))
        self.project.add_entry('bssrdf', 'Rd_curve.dat')
        self.project.overwrite()
        print('Finish!!')

    def renderPushButtonClicked(self):
        filename = self.getOpenFileName()
        if filename == "":
            return

        _ , ext = os.path.splitext(filename)
        if ext == '.xml':
            self.project = tools.Project(filename)

        if not 'bssrdf' in self.project.entries:
            self.showMessageBox('Estimate BSSRDF first!')

        self.project.bssrdf.scale(self.controlWidget.getScale())

        w = self.controlWidget.getWidthValue()
        h = self.controlWidget.getHeightValue()
        spp = self.controlWidget.getSamplePerPixel()
        photons = self.controlWidget.getNumberOfPhotons()
        renderparams = tools.RenderParameters(w, h, spp, photons)

        renderWidget = BSSRDFRenderWidget()
        self.tabWidgets.addTab(renderWidget, 'Render')
        renderWidget.startRendering(renderparams, self.project.bssrdf)

    @classmethod
    def showMessageBox(cls, msg):
        msgbox = QMessageBox()
        msgbox.setText(msg)
        msgbox.exec_()
