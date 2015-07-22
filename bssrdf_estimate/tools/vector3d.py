# -*- coding: utf-8 -*-

import math

class Vector3D(object):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    def dot(self, v):
        return self._x * v.x + self._y * v.y + self._z * v.z

    def norm(self):
        return math.sqrt(self.dot(self))

    def normalized(self):
        return self / self.norm()

    def __neg__(self):
        return Vector3D(-self._x, -self._y, -self._z)

    def __add__(self, v):
        return Vector3D(self._x + v.x, self._y + v.y, self._z + v.z)

    def __sub__(self, v):
        return Vector3D(self._x - v.x, self._y - v.y, self._z - v.z)

    def __mul__(self, s):
        return Vector3D(self._x * s, self._y * s, self._z * s)

    def __rmul__(self, s):
        return self.__mul__(s)

    def __truediv__(self, s):
        return self * (1.0 / s)
