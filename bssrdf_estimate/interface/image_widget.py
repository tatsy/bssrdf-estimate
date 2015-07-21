# -*- coding: utf-8 -*-

import numpy as np

from itertools import product

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import matplotlib.pyplot as plt

class ImageWidget(QWidget):
    def __init__(self, parent=None):
        super(ImageWidget, self).__init__(parent)

        self.imageScale = 1.0
        self.prevMousePos = QPoint(0, 0)

        self.imageLabel = QLabel()
        self.gridLayout = QGridLayout()
        self.scrollArea = QScrollArea()
        self.scrollArea.viewport().installEventFilter(self)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setWidgetResizable(True)

        self.gridLayout.addWidget(self.scrollArea)
        self.setLayout(self.gridLayout)

        self.pixmap = None

    def showImage(self, image):
        if isinstance(image, np.ndarray):
            image = self.numpy2qimage(image)
        self.pixmap = QPixmap(QPixmap.fromImage(image))
        self.imageLabel.setPixmap(self.pixmap)
        self.show()

    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            self.prevMousePos.setX(ev.x())
            self.prevMousePos.setY(ev.y())

    def mouseMoveEvent(self, ev):
        if ev.buttons() & Qt.LeftButton:
            dx = ev.x() - self.prevMousePos.x()
            dy = ev.y() - self.prevMousePos.y()
            self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().value() - dy)
            self.scrollArea.horizontalScrollBar().setValue(self.scrollArea.horizontalScrollBar().value() - dx)
            self.prevMousePos.setX(ev.x())
            self.prevMousePos.setY(ev.y())

    def wheelEvent(self, ev):
        scale = (1.0 / 0.95) if ev.angleDelta().y() > 0.0 else 0.95
        self.imageScale *= scale
        self.imageScale = max(self.imageScale, 0.2)
        self.imageScale = min(self.imageScale, 3.0)

        newSize = self.imageScale * self.pixmap.size()
        self.imageLabel.setPixmap(self.pixmap.scaled(newSize))
        self.imageLabel.resize(newSize)

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.Wheel:
            ev.ignore()
            return True
        return False

    @classmethod
    def numpy2qimage(cls, image):
        w = image.shape[1]
        h = image.shape[0]
        ret = QImage(w, h, QImage.Format_RGB888)
        for y, x in product(range(h), range(w)):
            if image.ndim == 3:
                c = image[y,x,:]
                r = int(min(c[0], 1.0) * 255.0)
                g = int(min(c[1], 1.0) * 255.0)
                b = int(min(c[2], 1.0) * 255.0)
                ret.setPixel(x, y, qRgb(r, g, b))
            else:
                c = int(min(image[y, x], 1.0) * 255.0)
                ret.setPixel(x, y, qRgb(c, c, c))
        return ret
