# -*- coding: utf-8 -*-

import os
import scipy as sp
import scipy.misc

from PyQt5.QtCore import QTimer, QThread

from .image_widget import ImageWidget
from bssrdf_estimate.render import render

class BSSRDFRenderThread(QThread):
    def __init__(self, render_params, bssrdf):
        super(BSSRDFRenderThread, self).__init__()
        self.render_params = render_params
        self.bssrdf = bssrdf

    def run(self):
        render(self.render_params.image_width,
               self.render_params.image_height,
               self.render_params.spp,
               self.render_params.photons,
               self.bssrdf.distances,
               self.bssrdf.colors)

class BSSRDFRenderWidget(ImageWidget):
    def __init__(self, parent=None):
        super(BSSRDFRenderWidget, self).__init__(parent)

        self.timer = QTimer()
        self.timer.setInterval(30)
        self.timer.timeout.connect(self.timerTick)
        self.timer.start()

        self.imageIndex = 1

        self.renderThread = None

    def timerTick(self):
        imagename = 'sss_sppm_%02d.bmp' % self.imageIndex
        if imagename in os.listdir('.'):
            img = sp.misc.imread(imagename) / 255.0
            self.showImage(img)
            self.imageIndex += 1

    def startRendering(self, render_params, bssrdf):
        self.show()
        self.renderThread = BSSRDFRenderThread(render_params, bssrdf)
        self.renderThread.start()
        print('hogehogehogeho')
