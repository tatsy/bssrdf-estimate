# -*- coding: utf-8 -*-

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
