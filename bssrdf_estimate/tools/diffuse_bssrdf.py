# -*- coding: utf-8 -*-

import struct
import numpy as np

class DiffuseBSSRDF(object):
    def __init__(self):
        self.distances = None
        self.colors    = None

    @staticmethod
    def load(filename):
        ret = DiffuseBSSRDF()
        with open(filename, 'rb') as fp:
            ret.colors = [None] * 3
            sz = struct.unpack('i', fp.read(4))[0]
            ret.distances = np.array(struct.unpack('f' * sz, fp.read(4 * sz)), dtype='float32')
            ret.colors = np.zeros((sz,3), dtype='float32')
            ret.colors[:,0] = np.array(struct.unpack('f' * sz, fp.read(4 * sz)), dtype='float32')
            ret.colors[:,1] = np.array(struct.unpack('f' * sz, fp.read(4 * sz)), dtype='float32')
            ret.colors[:,2] = np.array(struct.unpack('f' * sz, fp.read(4 * sz)), dtype='float32')
        return ret

    def save(self, filename):
        with open(filename, 'wb') as fp:
            sz = self.distances.size
            fp.write(struct.pack('i', sz))
            fp.write(struct.pack('f' * sz, *self.distances))
            fp.write(struct.pack('f' * sz, *self.colors[:,0]))
            fp.write(struct.pack('f' * sz, *self.colors[:,1]))
            fp.write(struct.pack('f' * sz, *self.colors[:,2]))

    def scale(self, sc):
        self.distances = self.distances / sc
        self.colors = self.colors / (sc * sc)
