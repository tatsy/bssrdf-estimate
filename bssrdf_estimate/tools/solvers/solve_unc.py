#-*- coding: utf-8 -*-

import numpy as np
import scipy as sp
import scipy.sparse
import scipy.sparse.linalg

import matplotlib.pyplot as plt

from .polyfit import cubic_fitting

class SolveUnc(object):
    def __init__(self, A, b):
        ATA = np.dot(A.T, A)
        ATb = np.dot(A.T, b)

        self.xx = np.zeros(ATb.shape)
        for c in range(ATb.shape[1]):
            self.xx[:,c] = sp.sparse.linalg.qmr(ATA, ATb[:,c])[0]

        self.save_curve_figure('result/Rd_curve_before_smoothing.png', self.xx)

        for c in range(ATb.shape[1]):
            self.xx[:,c] = cubic_fitting(self.xx[:,c])

        self.save_curve_figure('result/Rd_curve_after_smoothing.png', self.xx)

    @classmethod
    def save_curve_figure(cls, filename, xx):
        colors = [ 'r', 'g', 'b' ]

        sz = xx.shape[0]
        ds = [d for d in range(sz)]
        plt.clf()
        for i in range(3):
            plt.plot(ds, xx[:,i], colors[i])
        plt.savefig(filename, dpi=200)
