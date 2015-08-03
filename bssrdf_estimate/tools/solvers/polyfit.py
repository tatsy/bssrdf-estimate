#-*- coding: utf-8 -*-

''' Polynomial fitting '''

from itertools import chain

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

def linear_interpolation(a, b, n_div = 10):
    fun = lambda a, b, t: a * t + (1.0 - t) * b
    return [fun(a, b, i / n_div) for i in range(n_div)]

def cubic_fitting(ps):
    n_div = 5

    x0 = ps.copy()

    # Linear interpolation
    ps = map(lambda p0, p1: linear_interpolation(p0, p1, n_div), ps, ps[1:])
    ps = np.array(list(chain(*ps)))

    def func(x, ps = ps):
        w_d = 1.0
        w_p = 10.0
        w_s = 1.0e-4

        # Hermite interpolation
        _ , xs = spline_interpolate(x, n_div)

        cost = 0.0

        # Error between original
        cost += w_d * sum(map(lambda x, p: (x - p) ** 2.0, xs, ps))

        # Penalize increase
        cost += w_p * sum(map(lambda x0, x1: (x0 - x1) ** 2.0 if x0 - x1 < 0.0 else 0.0, xs, xs[1:]))
        cost += w_p * xs[-1] * xs[-1] if xs[-1] < 0.0 else 0.0

        # Penalize smoothness
        cost += w_s * sum(map(lambda x0, x1, x2: (x0 - 2.0 * x1 + x2) ** 2.0, xs, xs[1:], xs[2:]))

        return cost

    opt = { 'maxiter': 2000, 'disp': False }
    res = sp.optimize.minimize(func, x0, method='L-BFGS-B', options=opt)

    if not res.success:
        print('[ERROR] failed: %s' % res.message)
    else:
        print('[INFO] L-BFGS-B Success!!')

    return res.x
