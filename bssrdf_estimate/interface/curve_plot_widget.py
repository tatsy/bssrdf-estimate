# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        super(MplCanvas, self).__init__(fig)
        self.setParent(parent)

        super(MplCanvas, self).setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        super(MplCanvas, self).updateGeometry()

class CurvePlotWidget(QWidget):
    def __init__(self, parent=None):
        super(CurvePlotWidget, self).__init__(parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.mplCanvas = MplCanvas()
        self.layout.addWidget(self.mplCanvas)

    def setCurveData(self, bssrdf):
        colors = [ 'r', 'g', 'b' ]
        for i in range(3):
            self.mplCanvas.axes.plot(bssrdf.distances, bssrdf.colors[:,i], colors[i])
