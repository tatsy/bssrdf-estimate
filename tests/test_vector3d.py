# -*- coding: utf-8 -*-

import math

try:
    import unittest2 as unittest
except:
    import unittest

from bssrdf_estimate.tools import Vector3D

class Vector3DTest(unittest.TestCase):
    def test_instance(self):
        v = Vector3D()
        self.assertEqual(v.x, 0.0)
        self.assertEqual(v.y, 0.0)
        self.assertEqual(v.z, 0.0)

        v = Vector3D(1.0, 2.0, 3.0)
        self.assertEqual(v.x, 1.0)
        self.assertEqual(v.y, 2.0)
        self.assertEqual(v.z, 3.0)

    def test_assign_exception(self):
        v = Vector3D()
        with self.assertRaises(Exception):
            v.x = 1.0
        with self.assertRaises(Exception):
            v.y = 1.0
        with self.assertRaises(Exception):
            v.z = 1.0

    def test_negation(self):
        v = Vector3D(1.0, 2.0, 3.0)
        u = -v
        self.assertEqual(-v.x, u.x)
        self.assertEqual(-v.y, u.y)
        self.assertEqual(-v.z, u.z)

    def test_add_and_sub(self):
        v = Vector3D(1.0, 2.0, 3.0)
        u = Vector3D(4.0, 5.0, 6.0)
        w = v + u
        self.assertEqual(w.x, 5.0)
        self.assertEqual(w.y, 7.0)
        self.assertEqual(w.z, 9.0)

        w = v - u
        self.assertEqual(w.x, -3.0)
        self.assertEqual(w.y, -3.0)
        self.assertEqual(w.z, -3.0)

    def test_mul_and_div(self):
        v = Vector3D(1.0, 2.0, 3.0)
        u = v * 2.0
        self.assertEqual(v.x * 2.0, u.x)
        self.assertEqual(v.y * 2.0, u.y)
        self.assertEqual(v.z * 2.0, u.z)

        u = 3.0 * v
        self.assertEqual(v.x * 3.0, u.x)
        self.assertEqual(v.y * 3.0, u.y)
        self.assertEqual(v.z * 3.0, u.z)

        w = v / 2.0
        self.assertAlmostEqual(v.x / 2.0, w.x)
        self.assertAlmostEqual(v.y / 2.0, w.y)
        self.assertAlmostEqual(v.z / 2.0, w.z)

        with self.assertRaises(Exception):
            w = u / 0.0

    def test_dot(self):
        u = Vector3D(1.0, 2.0, 3.0)
        v = Vector3D(2.0, 3.0, 4.0)
        self.assertAlmostEqual(v.dot(u), 20.0)
        self.assertEqual(u.dot(v), v.dot(u))

    def test_norm_and_normalized(self):
        u = Vector3D(1.0, 2.0, 3.0)
        self.assertAlmostEqual(u.norm(), math.sqrt(14.0))

        nrm = u.norm()
        v = u.normalized()
        self.assertAlmostEqual(u.x / nrm, v.x)
        self.assertAlmostEqual(u.y / nrm, v.y)
        self.assertAlmostEqual(u.z / nrm, v.z)

        w = Vector3D()
        with self.assertRaises(Exception):
            w.normalized()

if __name__ == '__main__':
    unittest.main()
