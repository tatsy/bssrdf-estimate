# -*- coding: utf-8 -*-

class RenderParameters(object):
    def __init__(self, image_width=400, image_height=300, spp=1, photons=1000000):
        self._image_width = image_width
        self._image_height = image_height
        self._spp = spp
        self._photons = photons

    @property
    def image_width(self):
        return self._image_width

    @property
    def image_height(self):
        return self._image_height

    @property
    def spp(self):
        return self._spp

    @property
    def photons(self):
        return self._photons
