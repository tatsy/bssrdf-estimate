#-*- coding: utf-8 -*-
import numpy as np
from cvxopt import matrix, solvers

from .polyfit import cubic_fitting

class SolveCon(object):
    def __init__(self, A, b):
        self.xx = np.zeros((A.shape[1], b.shape[1]))
        for c in range(b.shape[1]):
            p = self._solve_sub(A, b[:,c])
            self.xx[:,c] = p

    @classmethod
    def _solve_sub(cls, A, b):
        nb = A.shape[1]

        Q = matrix(np.dot(A.T, A))
        p = matrix(-2.0 * np.dot(A.T, b))

        G = np.zeros((nb, nb))
        for i in range(nb-1):
            G[i, i]   = -1.0
            G[i, i+1] =  1.0
        G[nb-1, nb-1] = -1.0

        G = matrix(G)
        h = matrix(np.zeros(nb))

        sol = solvers.qp(Q, p, G, h)
        x   = np.reshape(sol['x'], nb)

        return x
