#-*- coding: utf-8 -*-

''' Polynomial fitting '''

import functools

import numpy as np
import scipy as sp
import scipy.optimize

def spline_interpolate(p, n_div = 10):
    n = p.shape[0]

    A = np.zeros((n, n))
    b = np.zeros(n)
    A[0, 0] = 1.0
    b[0]    = 0.0
    for i in range(1, n - 1):
        A[i, i - 1] = 1.0
        A[i, i]     = 4.0
        A[i, i + 1] = 1.0
        b[i] = 3.0 * (p[i + 1] - p[i]) - 3.0 * (p[i] - p[i - 1])
    A[n - 1, n - 1] = 1.0
    b[n - 1]        = 0.0

    cs = np.linalg.solve(A, b)
    bs = np.zeros(n)
    ds = np.zeros(n)
    for i in range(n - 1):
        bs[i] = (p[i + 1] - p[i]) - (2.0 * cs[i] + cs[i + 1]) / 3.0
        ds[i] = (cs[i + 1] - cs[i]) / 3.0

    xs = []
    ys = []
    for i in range(n - 1):
        for k in range(n_div):
            t = k / n_div
            xs.append(i + t)
            ys.append(p[i] + bs[i] * t + cs[i] * (t * t) + ds[i] * t * t * t)

    return xs, ys

def lin_interp(a, b, n_div = 10):
    fun = lambda a, b, t: a * t + (1.0 - t) * b
    return [fun(a, b, i / n_div) for i in range(n_div)]

def cubic_fitting(p):
    n_div = 5

    x0 = p.copy()
    p = [lin_interp(p[i], p[i+1], n_div) for i in range(len(p) - 1)]
    p = np.array(functools.reduce(lambda a, b: a + b, p))
    n = p.shape[0]

    def func(x, p = p):
        w_d = 1.0
        w_p = 10.0
        w_s = 1.0e-4

        # Hermite interpolation
        _ , xs = spline_interpolate(x, n_div)

        # Error between original
        cost = 0.0
        for i in range(n):
            cost += w_d * ((xs[i] - p[i]) ** 2.0)

        # Penalize increase
        for i in range(n - 1):
            gap = xs[i + 1] - xs[i]
            if gap > 0.0:
                cost += w_p * gap

        # Penalize non-negativity
        if xs[n - 1] < 0.0:
            cost += w_p * abs(xs[n - 1])

        # Penalize smoothness
        for i in range(1, n - 1):
            ddf = xs[i - 1] - 2.0 * xs[i] + xs[i + 1]
            cost += w_s * ddf

        return cost

    opt = { 'maxiter': 2000 }
    res = sp.optimize.minimize(func, x0, method='L-BFGS-B', options=opt)

    return res.x
