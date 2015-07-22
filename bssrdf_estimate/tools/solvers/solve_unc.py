#-*- coding: utf-8 -*-

import numpy as np
import scipy as sp
import scipy.sparse
import scipy.sparse.linalg

from .polyfit import cubic_fitting

class SolveUnc(object):
    def __init__(self, A, b):
        ATA = np.dot(A.T, A)
        ATb = np.dot(A.T, b)

        self.x = np.zeros(ATb.shape)
        for c in range(ATb.shape[1]):
            p = sp.sparse.linalg.qmr(ATA, ATb[:,c])[0]
            self.x[:,c] = cubic_fitting(p)
