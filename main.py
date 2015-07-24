# -*- coding: utf-8 -*-

import os
import sys

import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5.QtWidgets import QApplication
from bssrdf_estimate.interface import MainWindow

if __name__ == '__main__':
    # Create directory for intermediate results
    try:
        os.mkdir('result')
        print('[INFO] result directory is created!')
    except:
        print('[INFO] result directory already exists. Skip creating.')

    # Start application
    app = QApplication(sys.argv)
    win = MainWindow()
    win.showMaximized()
    sys.exit(app.exec_())
