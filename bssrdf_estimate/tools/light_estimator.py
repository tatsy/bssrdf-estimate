# -*- coding: utf-8 -*-

import math
from itertools import product

from .. import hdr
from .vector3d import Vector3D

EPS = 1.0e-8

class SilhouettePoint(object):
    def __init__(self, x, y, lum, angle):
        self._x = x
        self._y = y
        self._lum = lum
        self._angle = angle

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def luminance(self):
        return self._lum

    @property
    def angle(self):
        return self._angle

class DirectionalLight(object):
    def __init__(self, phi, theta):
        self.phi = phi
        self.theta = theta
        self.weight = 0.0

class LightEstimator(object):

    NUM_LIGHTS = 4
    NUM_ITER = 20

    def __init__(self):
        pass

    def process(self, image, mask):
        self.detect_silhouette(image, mask)
        self.contour_voting()

    def detect_silhouette(self, image, mask):
        dx = [-1, 0, 1, -1, 1, -1, 0, 1]
        dy = [-1, -1, -1, 0, 0, 1, 1, 1]

        width = image.shape[1]
        height = image.shape[0]

        self.silhouette = []
        for y, x in product(range(1,height-1), range(1,width-1)):
            if mask[y,x] != 1:
                continue

            is_silhouette = False
            for k in range(8):
                nx = x + dx[k]
                ny = y + dy[k]
                if mask[ny,nx] != 1:
                    is_silhouette = True
                    break

            if is_silhouette:
                sum_angl = 0.0
                sum_wgt  = 0.0
                for k in range(8):
                    nx = x + dx[k]
                    ny = y + dy[k]
                    m1 = mask[y,x]
                    m2 = mask[ny,nx]
                    wgt = max(0, m1 - m2)
                    sum_angl = math.atan2(dy[k], dx[k]) * wgt
                    sum_wgt += wgt

                col = image[y,x,:]
                lum = hdr.luminance(col[0], col[1], col[2])
                angl = sum_angl / sum_wgt if abs(sum_wgt) > EPS else 0.0
                self.silhouette.append(SilhouettePoint(x, y, lum, angl))

    def contour_voting(self):
        # Initialize lights
        self.lights = []
        for i in range(self.NUM_LIGHTS):
            self.lights.append(DirectionalLight(2.0 * math.pi * i / self.NUM_LIGHTS - math.pi, 0.0))

        # Iloyd iteration
        numSP = len(self.silhouette)
        for it in range(self.NUM_ITER):
            sum_omega = [0.0] * numSP
            for i in range(numSP):
                phi_i_n = self.silhouette[i].angle
                n_i = Vector3D(math.cos(phi_i_n), math.sin(phi_i_n), 0.0)

                for j in range(self.NUM_LIGHTS):
                    phi_j_l = self.lights[j].phi
                    omega_j = Vector3D(math.cos(phi_j_l), math.sin(phi_j_l), 0.0)
                    sum_omega[i] += max(0.0, n_i.dot(omega_j))

            for j in range(self.NUM_LIGHTS):
                phi_j_l = self.lights[j].phi
                omega_j = Vector3D(math.cos(phi_j_l), math.sin(phi_j_l), 0.0)

                sum_phi = 0.0
                sum_wgt = 0.0
                for i in range(numSP):
                    phi_i_n = self.silhouette[i].angle
                    n_i = Vector3D(math.cos(phi_i_n), math.sin(phi_i_n), 0.0)
                    omg = max(0.0, n_i.dot(omega_j))
                    alph_ij = self.silhouette[i].luminance * omg / (sum_omega[i] + EPS)

                    new_phi = self.lights[j].weight * self.lights[j].phi + alph_ij * phi_i_n
                    new_wgt = self.lights[j].weight + alph_ij

                    self.lights[j].weight = new_wgt
                    self.lights[j].phi = new_phi / (new_wgt + EPS)

        for i in range(self.NUM_LIGHTS):
            print('phi = %f' % self.lights[i].phi)

    def estimate_zenith(self, image, mask):
        width = image.shape[1]
        height = image.shape[0]

        lum = np.zeros((height, width))
        for y, x in product(range(height), range(width)):
            col = image[y,x,:]
            lum[y,x] = hdr.luminance(col[0], col[1], col[2])

        clip_img, clip_mask = self.clip_masked_region(lum, mask)

        num_rot = 64
        clip_width =clip_img.shape[1]
        clip_height = clip_img.shape[0]
        rot_imgs = [None] * num_rot
        rot_masks = [None] * num_rot
        for i in range(num_rot):
            pass

    def clip_masked_region(image, mask):
        width = image.shape[1]
        height = image.shape[0]

        minx = width - 1
        miny = height - 1
        maxx = 0
        maxy = 0
        for y, x in product(range(height), range(width)):
            if mask[y,x] == 1:
                minx = min(x, minx)
                miny = min(y, miny)
                maxx = max(x, maxx)
                maxy = max(y, maxy)

        sz = math.sqrt(2.0) * max(maxx - minx + 1, maxy - miny + 1)
        sx = (minx + maxx - sz) // 2
        sy = (miny + maxy - sz) // 2

        clip_img = np.zeros((sz, sz))
        clip_mask = np.zeros((sz, sz))
        for y, x in product(range(height), range(width)):
            nx = sx + x
            ny = sy + y
            if nx >= 0 and ny >= 0 and nx < width and ny < height:
                clip_img[y,x] = image[ny,nx]
                clip_mask[y,x] = mask[ny,nx]

        return clip_img, clip_mask
