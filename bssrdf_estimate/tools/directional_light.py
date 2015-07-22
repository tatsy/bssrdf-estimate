# -*- coding: utf-8 -*-

import math
from .vector3d import Vector3D

class DirectionalLight(object):
    def __init__(self, phi, theta):
        self.phi    = phi
        self.theta  = theta
        self.weight = 0.0

    def direction(self):
        x = math.cos(self.phi) * math.cos(self.theta)
        y = math.sin(self.phi) * math.cos(self.theta)
        z = math.sin(self.theta)
        return Vector3D(x, y, z)
