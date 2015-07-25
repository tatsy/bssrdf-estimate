# -*- coding: utf-8 -*-

import math
import numpy as np
import scipy as sp
import scipy.misc
import scipy.ndimage.interpolation

from itertools import product

from .. import hdr
from .vector3d import Vector3D
from .affine_transform import AffineTransform
from .directional_light import DirectionalLight

import bssrdf_estimate.imfilter as imfilter

EPS = 1.0e-8

class Rect(object):
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._w = width
        self._h = height

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._w

    @property
    def height(self):
        return self._h

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

class LightEstimator(object):

    NUM_LIGHTS = 4
    NUM_ITER = 20

    def __init__(self):
        pass

    def process(self, image, mask):
        self.detect_silhouette(image, mask)
        self.contour_voting()
        self.estimate_zenith(image, mask)

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
                    sum_angl += math.atan2(dy[k], dx[k]) * wgt
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

    def estimate_zenith(self, image, mask):
        width = image.shape[1]
        height = image.shape[0]

        lum = np.zeros((height, width), dtype='float32')
        for y, x in product(range(height), range(width)):
            col = image[y,x,:]
            lum[y,x] = hdr.luminance(col[0], col[1], col[2])

        for it in range(10):
            lum = imfilter.bilateral_filter(lum, 5.0, 1.0, 15)

        clip_img, clip_mask, clip_rect = self.clip_masked_region(lum, mask)

        num_rot = 64
        clip_width = clip_img.shape[1]
        clip_height = clip_img.shape[0]
        rot_imgs = [None] * num_rot
        rot_masks = [None] * num_rot
        for i in range(num_rot):
            cx = clip_width / 2
            cy = clip_height / 2
            theta = - 360.0 * i / num_rot
            rot_imgs[i] = sp.ndimage.interpolation.rotate(clip_img, theta, reshape=False)
            rot_masks[i] = sp.ndimage.interpolation.rotate(clip_mask, theta, reshape=False)

        num_light = len(self.lights)
        num_cont = len(self.silhouette)

        for j in range(num_light):
            theta_ij = []
            L_ij = []
            for i in range(num_cont):
                l = self.lights[j]

                cx = clip_rect.x + clip_rect.width // 2
                cy = clip_rect.y + clip_rect.height // 2
                sx = self.silhouette[i].x - cx
                sy = self.silhouette[i].y - cy

                rot = math.atan2(sy, sx)
                rx = int(sx * math.cos(rot) - sy * math.sin(rot) + cx - clip_rect.x)
                ry = int(sx * math.sin(rot) + sy * math.cos(rot) + cy - clip_rect.y)
                rx = max(0, min(rx, clip_width - 1))
                ry = max(0, min(ry, clip_height - 1))

                rot_idx = int(l.phi * num_rot / (2.0 * math.pi))
                while rot_idx < 0:
                    rot_idx += num_rot
                rot_idx %= num_rot

                left_x = clip_width - 1
                right_x = 0
                for x in range(0, clip_width):
                    if rot_masks[rot_idx][ry,x] > 0.5:
                        left_x = min(x, left_x)
                        right_x = max(x, right_x)

                if left_x > right_x:
                    continue

                ext_x = left_x
                f1 = rot_imgs[rot_idx][ry,left_x-1]
                f2 = rot_imgs[rot_idx][ry,left_x+1]
                grad = (f2 - f1) * 0.5
                for x in range(left_x, right_x):
                    f1 = rot_imgs[rot_idx][ry,x-1]
                    f2 = rot_imgs[rot_idx][ry,x+1]
                    gg = (f2 - f1) * 0.5
                    if gg * grad < 0.0:
                        ext_x = x
                        break

                numer_mls = 0.0
                denom_mls = 0.0
                mid_x = (left_x + right_x) / 2.0
                radius = (right_x - left_x) / 2.0
                for x in range(left_x, right_x+1):
                    if rot_masks[rot_idx][ry,x] > 0.5:
                        dx = x - mid_x
                        a = math.sqrt(radius * radius - dx * dx)
                        l = lum[ry,x]
                        numer_mls += a * l
                        denom_mls += a * a
                ratio = numer_mls / (denom_mls + EPS)

                dx = abs(ext_x - mid_x)
                th = math.atan(math.sqrt(radius * radius - dx * dx) / (dx * ratio + EPS))
                th = th * (1.0 if grad > 0.0 else -1.0)
                theta_ij.append(th)
                L_ij.append(rot_imgs[rot_idx][ry, ext_x])

            numer = 0.0
            denom = 0.0
            for i in range(len(theta_ij)):
                numer += theta_ij[i] * L_ij[i]
                denom += L_ij[i]

            self.lights[j].theta = numer / (denom + EPS)

    @classmethod
    def clip_masked_region(cls, image, mask):
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

        sz = int(math.sqrt(2.0) * max(maxx - minx + 1, maxy - miny + 1))
        sx = (minx + maxx - sz) // 2
        sy = (miny + maxy - sz) // 2

        clip_img = np.zeros((sz, sz))
        clip_mask = np.zeros((sz, sz))
        clip_rect = Rect(sx, sy, sz, sz)
        for y, x in product(range(sz), range(sz)):
            nx = sx + x
            ny = sy + y
            if nx >= 0 and ny >= 0 and nx < width and ny < height:
                clip_img[y,x] = image[ny,nx]
                clip_mask[y,x] = mask[ny,nx]

        return clip_img, clip_mask, clip_rect
