# -*- coding: utf-8 -*-

import os
import numpy as np
import scipy as sp
import scipy.misc

from xml.etree.ElementTree import ElementTree
import xml.dom.minidom

import bssrdf_estimate.hdr as hdr

from .diffuse_bssrdf import DiffuseBSSRDF

class Project(object):
    def __init__(self, filename):
        self.filename = filename
        self.dirname = os.path.dirname(filename)
        self.entries = {}

        tree = ElementTree()
        tree.parse(filename)
        elem = tree.getroot()
        for e in elem.findall('entry'):
            if e.get('type') == 'image':
                self.hdr = hdr.load(os.path.join(self.dirname, e.text))
                self.image = hdr.tonemap(self.hdr)
            elif e.get('type') == 'mask':
                self.mask = sp.misc.imread(os.path.join(self.dirname, e.text), flatten=True)
                self.mask[np.where(self.mask <  128)] = 0
                self.mask[np.where(self.mask >= 128)] = 1
            elif e.get('type') == 'bssrdf':
                self.bssrdf = DiffuseBSSRDF.load(os.path.join(self.dirname, e.text))
            self.entries[e.get('type')] = e.text

    def add_entry(self, key, val):
        self.entries[key] = val

    def overwrite(self):
        impl = xml.dom.minidom.getDOMImplementation()
        doc  = impl.createDocument(None, 'content', None)
        root = doc.documentElement
        for k, v in self.entries.items():
            node = doc.createElement('entry')
            text = doc.createTextNode(v)
            node.appendChild(text)
            attr = doc.createAttribute('type')
            attr.value = k
            node.setAttributeNode(attr)
            root.appendChild(node)

        with open(self.filename, 'w') as f:
            f.write(doc.toprettyxml())
