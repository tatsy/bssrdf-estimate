# -*- coding: utf-8 -*-

import math
import numpy as np
from itertools import product

from .luminance import luminance

def tonemap(image):
    if image.ndim != 3:
        raise Exception('Image dimension invalid')

    height = image.shape[0]
    width = image.shape[1]

    delta = 1.0e-8
    a = 0.18

    Lw_bar = 0.0
    L_white = 0.0
    for y, x in product(range(height), range(width)):
        c = image[y,x,:]
        l = luminance(c[0], c[1], c[2])
        Lw_bar += math.log(l + delta)
        L_white = max(l, L_white)
    Lw_bar = math.exp(Lw_bar / (width * height))
    L_white2 = L_white * L_white

    ret = image * (1.0 + image / L_white2) / (1.0 + image)
    return image