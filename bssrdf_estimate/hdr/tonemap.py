# -*- coding: utf-8 -*-

import math
import numpy as np
from itertools import product

from .luminance import luminance

def tonemap(image):
    '''
    Tone mapping with [Reinhard 2002]
    '''

    if image.ndim != 3:
        raise Exception('Image dimension invalid')

    height = image.shape[0]
    width = image.shape[1]

    delta = 1.0e-8
    a = 0.18

    Lw_bar = 0.0
    L_white = 0.0

    lum = image[:,:,0] * 0.2126 + image[:,:,1] * 0.7152 + image[:,:,2] * 0.0722
    lw_bar = math.exp(np.log(lum + delta).sum() / lum.size)
    l_white2 = lum.max() ** 2.0

    ret = image * a / lw_bar
    ret = ret * (1.0 + ret / l_white2) / (1.0 + ret)
    return ret
