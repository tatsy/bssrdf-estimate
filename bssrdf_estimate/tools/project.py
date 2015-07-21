# -*- coding: utf-8 -*-

import os
import numpy as np
import scipy as sp
import scipy.misc

from xml.etree.ElementTree import ElementTree
from .. import hdr

class Project(object):
    def __init__(self, filename):
        self.dirname = os.path.dirname(filename)

        self.tree = ElementTree()
        self.tree.parse(filename)
        elem = self.tree.getroot()
        for e in elem.findall('entry'):
            if e.get('type') == 'image':
                self.hdr = hdr.load(os.path.join(self.dirname, e.text))
                self.image = hdr.tonemap(self.hdr)
            elif e.get('type') == 'mask':
                self.mask = sp.misc.imread(os.path.join(self.dirname, e.text), flatten=True)

                self.mask[np.where(self.mask <  128)] = 0
                self.mask[np.where(self.mask >= 128)] = 1
