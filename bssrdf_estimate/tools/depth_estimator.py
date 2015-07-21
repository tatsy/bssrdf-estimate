# -*- coding: utf-8 -*-
import sys
import math

import numpy as np
import scipy as sp
import scipy.misc
import matplotlib.pyplot as plt

from itertools import product

EPS = 1.0e-8
PIXEL_MASKED = 1
PIXEL_NOT_MASKED = 0

N_POW = 0.73

class DepthEstimator(object):
    def __init__(self, img, mask):
        self.img  = img
        self.mask = mask

    def process(self):
        width = self.img.shape[1]
        height = self.img.shape[0]
        luminance = np.zeros((height, width))

        pixel_count = 0
        sigma = 0.0
        for y, x in product(range(height), range(width)):
            if self.mask[y, x] == PIXEL_MASKED:
                c = self.img[y, x, :]
                luminance[y, x] = c[0] * 0.2126 + c[1] * 0.7152 + c[2] * 0.0722
                sigma += math.log(luminance[y, x] + EPS)
                pixel_count += 1
        sigma = math.exp(sigma / pixel_count)

        for y, x in product(range(height), range(width)):
            l = luminance[y, x]
            luminance[y, x] = math.pow(l, N_POW) / (math.pow(l, N_POW) + math.pow(sigma, N_POW))

        # TODO: apply bilateral filter

        # Invert sigmoidal compression in Eq.11 of [Khan et al. 2006]
        self.depth = np.zeros((height, width))
        dscale = min(width, height) * 0.01
        for y, x in product(range(height), range(width)):
            if self.mask[y, x] == PIXEL_MASKED:
                d = luminance[y, x]
                b = - math.pow(sigma, N_POW) * d / min(d - 1.0, -EPS)
                dp = math.pow(b, 1.0 / N_POW)
                self.depth[y, x] = dp * dscale

        # Solve for depth
        self._solve_depth2()

        sp.misc.imsave('depth_map.png', self.depth)

    def save_mesh(self, filename):
        width = self.depth.shape[1]
        height = self.depth.shape[0]
        vertices = []
        faces = []
        vert_count = 1
        for y, x in product(range(1, height-1), range(1, width-1)):
            if self.mask[y, x] == PIXEL_MASKED:
                vertices.append((x, y, self.depth[y, x]))
                vertices.append((x+1, y, self.depth[y, x+1]))
                vertices.append((x, y+1, self.depth[y+1, x]))
                vertices.append((x+1, y+1, self.depth[y+1, x+1]))

                faces.append((vert_count, vert_count + 3, vert_count + 2))
                faces.append((vert_count, vert_count + 1, vert_count + 3))
                vert_count += 4

        with open(filename, 'w') as fp:
            for v in vertices:
                fp.write('v %f %f %f\n' % (v[0], v[1], v[2]))

            for f in faces:
                fp.write('f %d %d %d\n' % (f[0], f[1], f[2]))

    def _solve_depth(self):
        width = self.depth.shape[1]
        height = self.depth.shape[0]
        siz = width * height
        lap = self._make_laplacian(width, height)
        lmbd = 50.0

        dd = np.reshape(self.depth, (siz, 1))

        AA = 0.5 * sp.sparse.identity(siz) + lmbd * (sp.sparse.csr_matrix.dot(lap.T, lap))
        xx = sp.sparse.linalg.bicgstab(AA, dd)[0]

        self.depth = np.reshape(xx, (height, width))

    def _solve_depth2(self):
        width = self.depth.shape[1]
        height = self.depth.shape[0]

        temp = self.depth.copy()

        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]
        print('Gauss Seidel', end='')
        for t in range(20):
            print('.', end='')
            for y, x in product(range(1, height-1), range(1, width-1)):
                sumD = 0.0
                sumW = 0.0
                for k in range(4):
                    nx = x + dx[k]
                    ny = y + dy[k]
                    d1 = self.depth[y, x] - self.depth[ny, nx]
                    d2 = temp[y, x] - temp[ny, nx]
                    d2 = min(1.0, max(-1.0, d2))
                    d2 = self._reshape(abs(d2), 1) * (1.0 if d2 > 0.0 else -1.0)
                    sumD += d2 - d1
                    sumW += 1.0
                self.depth[y, x] += 0.5 * sumD / (sumW + EPS)

    @classmethod
    def _reshape(cls, x, d=0):
        if d == 0:
            return (3.0 + (-6.0 + 4.0 * x) * x) * x
        else:
            return cls._reshape(cls._reshape(x, d-1))


    def _make_laplacian(self, width, height):
        rows = []
        cols = []
        vals = []
        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]
        for y, x in product(range(1, height-1), range(1, width-1)):
            rows.append(y * width + x)
            cols.append(y * width + x)
            vals.append(-1.0)
            for k in range(4):
                nx = x + dx[k]
                ny = y + dy[k]
                rows.append(y * width + x)
                cols.append(ny * width + nx)
                vals.append(0.25)

        siz = width * height
        return sp.sparse.csr_matrix((vals, (rows, cols)), shape=(siz, siz))
