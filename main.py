# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import *
from bssrdf_estimate import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
