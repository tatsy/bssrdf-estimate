# -*- coding: utf-8 -*-

import math
import numpy as np
from itertools import product

EPS = 1.0e-8

class AffineTransform(object):
    def __init__(self):
        self.data = np.identity(3)

    @classmethod
    def rotation2D(cls, center, theta):
        cx = center[0]
        cy = center[1]
        t1 = cls._translate2D(-cx, -cy)
        rot = cls._rotation2D(theta)
        t2 = cls._translate2D(cx, cy)
        af = AffineTransform()
        af.data = np.dot(t2.data, np.dot(rot.data, t1.data))
        return af

    @classmethod
    def _rotation2D(cls, theta):
        af = AffineTransform()
        af.data[0,0] =  math.cos(theta)
        af.data[0,1] = -math.sin(theta)
        af.data[1,0] =  math.sin(theta)
        af.data[1,1] =  math.cos(theta)
        return af

    @classmethod
    def _translate2D(cls, dx, dy):
        af = AffineTransform()
        af.data[0,2] = dx
        af.data[1,2] = dy
        return af

    def apply(self, image):
        if image.ndim >= 3:
            raise Exception('This method is applicable for images with less than 3 channels!')

        dx = [0, 1, 0, 1]
        dy = [0, 0, 1, 1]

        w = image.shape[1]
        h = image.shape[0]
        ret = np.zeros((h,w))
        for y, x in product(range(h), range(w)):
            v = np.array((x, y, 1))
            v = np.dot(self.data, v)
            if v[0] >= 0 and v[1] >= 0 and v[0] < w and v[1] < h:
                vx = int(v[0])
                vy = int(v[1])
                fx = v[0] - vx
                fy = v[1] - vy
                cx = [1.0-fx, fx, 1.0-fx, fx]
                cy = [1.0-fy, 1.0-fy, fy, fy]

                sc = 0.0
                sw = 0.0
                for k in range(4):
                    nx = vx + dx[k]
                    ny = vy + dy[k]
                    if nx >= 0 and ny >= 0 and nx < w and ny < h:
                        sc += cx[k] * cy[k] * image[ny,nx]
                        sw += cx[k] * cy[k]
                ret[y,x] = sc / (sw + EPS)
        return ret
