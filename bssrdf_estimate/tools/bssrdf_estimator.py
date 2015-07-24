# -*- coding: utf-8 -*-

import math
import struct
import numpy as np

from itertools import product
from random import *

from .vector3d import Vector3D
from .diffuse_bssrdf import DiffuseBSSRDF
from .solvers import *

IOR_VACCUM = 1.0
IOR_OBJECT = 1.5
light_E = 32.0
eta = 1.3
NUM_BASES = 30
EPS = 1.0e-8

def Ft(eta, ddn):
    nnt = IOR_VACCUM / IOR_OBJECT
    cos2t = 1.0 - nnt * nnt * (1.0 - ddn * ddn)
    if cos2t < 0.0:
        return 0.0

    a = IOR_OBJECT - IOR_VACCUM
    b = IOR_OBJECT + IOR_VACCUM
    R0 = (a * a) / (b * b)

    c = 1.0 - ddn
    Fr = R0 + (1.0 - R0) * (c ** 5.0)
    return 1.0 - Fr

class PixelConstraint(object):
    def __init__(self, color, pos, normal):
        self.color  = color
        self.pos    = pos
        self.normal = normal
        self.front_E = 0.0
        self.back_E  = 0.0

class BSSRDFEstimator(object):
    def __init__(self):
        pass

    def process(self, image, mask, depth, lights):
        width = image.shape[1]
        height = image.shape[0]

        self.pixels = self.extract_pixel_constraints(image, mask, depth)
        self.translucent_shadowmap(lights)

        # Build up system of linear equations
        inv_pi = 1.0 / math.pi
        num_pixels = len(self.pixels)
        dscale = NUM_BASES / (0.5 * (width + height))
        A = np.zeros((num_pixels, NUM_BASES))
        for i in range(num_pixels):
            for k in range(num_pixels):
                # Front side
                p_f = self.pixels[k].pos
                r_f = (self.pixels[i].pos - p_f).norm()
                j_f = int(r_f * dscale)

                if j_f >= 0 and j_f < NUM_BASES:
                    delta_A = 1.0 / (abs(self.pixels[i].normal.z) + EPS)
                    A[i,j_f] += self.pixels[k].front_E * delta_A

                # Back side
                p_b = Vector3D(p_f.x, p_f.y, 0.0)
                r_b = (self.pixels[i].pos - p_b).norm()
                j_b = int(r_b * dscale)

                if j_b >= 0.0 and j_b < NUM_BASES:
                    delta_A = 1.0
                    A[i,j_b] += self.pixels[k].back_E * delta_A

            angl = self.pixels[i].normal.z
            fresnel = Ft(eta, angl)
            A[i,:] *= fresnel

        bb = np.zeros((num_pixels, 3))
        for i in range(num_pixels):
            bb[i,:] = self.pixels[i].color[:]

        self.solve_linear_system(A, bb)

    def extract_pixel_constraints(self, image, mask, depth):
        width = image.shape[1]
        height = image.shape[0]

        ret = []
        for y, x in product(range(1,height-1), range(1,width-1)):
            if mask[y,x] == 1:
                col = image[y,x,:]
                pos = Vector3D(x, y, depth[y,x])

                dx = (depth[y,x+1] - depth[y,x-1]) * 0.5
                dy = (depth[y+1,x] - depth[y+1,x]) * 0.5
                normal = Vector3D(-dx, -dy, 1.0).normalized()
                ret.append(PixelConstraint(col, pos, normal))

        max_const = 5000
        num_const = len(ret)

        if num_const > max_const:
            print('[INFO] Masked pixels are too many. Sample to reduce the number!')
            temp = ret
            ret = []
            for i in range(max_const):
                r = randint(i, num_const - 1)
                temp[i], temp[r] = temp[r], temp[i]
            ret.append(temp[i])

        return ret

    def translucent_shadowmap(self, lights):
        num_pixels = len(self.pixels)
        num_lights = len(lights)

        for i in range(num_pixels):
            f_normal = self.pixels[i].normal
            f_E = 0.0
            for j in range(num_lights):
                light_dir = lights[j].direction()
                angl = - light_dir.dot(f_normal)
                if angl > 0.0:
                    f_E += Ft(eta, angl) * angl * light_E
            self.pixels[i].front_E = f_E

            b_normal = Vector3D(0.0, 0.0, -1.0)
            b_E = 0.0
            for j in range(num_lights):
                light_dir = lights[j].direction()
                angl = -light_dir.dot(b_normal)
                if angl >= 0.0:
                    b_E += Ft(eta, angl) * angl * light_E
            self.pixels[i].back_E = b_E

    def solve_linear_system(self, A, bb, constrained=False):
        if constrained:
            print('[INFO] Use constrained solver...')
            xx = SolveCon(A, bb).xx
        else:
            print('[INFO] Use unconstrained solver...')
            xx = SolveUnc(A, bb).xx

        assert xx is not None, "[ASSERT] Solution x is invalid"

        self.set_curves(xx)

    def set_curves(self, xx):
        # Smoothing the Rd curve
        self.bssrdf = DiffuseBSSRDF()
        for i in range(3):
            xs, ys = spline_interpolate(xx[:,i])
            if i == 0:
                self.bssrdf.distances = np.array(xs)
                self.bssrdf.colors = np.zeros((self.bssrdf.distances.size, 3))
            self.bssrdf.colors[:,i] = np.array(ys)
