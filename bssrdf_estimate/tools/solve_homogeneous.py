#-*- coding: utf-8 -*-
import os
import sys
import struct
from optparse import OptionParser

import numpy as np
import matplotlib.pyplot as plt

import hdr
from utils import *
from solvers import *

def save_curves_sub(filename, Rd):
    fp = open(filename, 'wb')
    for i in range(3):
        sz = len(Rd[i][0])
        fp.write(struct.pack('i', sz))
        fp.write(struct.pack('f' * sz, *Rd[i][0]))
        fp.write(struct.pack('f' * sz, *Rd[i][1]))
    fp.close()

def save_curves(filename, x, verbose=False):
    colors = [ 'r', 'g', 'b' ]
    Rd = []
    if x.ndim == 2:
        for i in range(3):
            xs, ys = spline_interpolate(x[:,i])
            Rd.append((xs, ys))
            plt.plot(xs, ys, colors[i])
    save_curves_sub(filename, Rd)

    base, ext = os.path.splitext(filename)
    plt.savefig(base + '.png')

    if verbose:
        plt.show()

def main():
    parser = OptionParser()
    parser.add_option('-a', '--mata', action='store', type='string', dest='matA')
    parser.add_option('-b', '--matb', action='store', type='string', dest='matB')
    parser.add_option('-x', '--matx', action='store', type='string', dest='matX')
    parser.add_option('-c', '--constrained', action='store_true', dest='is_con', default=False)
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False)

    opts, args = parser.parse_args()

    if opts.matA is None or opts.matB is None or opts.matX is None:
        parser.print_help()
        sys.exit(1)

    matA = matrix_load(opts.matA)
    matB = matrix_load(opts.matB)

    x = None
    if opts.is_con:
        print('Use constrained solver...')
        x = SolveCon(matA, matB).x
    else:
        print('Use unconstrained solver...')
        x = SolveUnc(matA, matB).x

    assert x is not None, "Solution x is invalid"

    save_curves(opts.matX, x, opts.verbose)

if __name__ == '__main__':
    main()
