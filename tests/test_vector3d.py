# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except:
    import unittest

from bssrdf_estimate import *

class Vector3DTest(unittest.TestCase):
    def test_instance(self):
        v = Vector3D()
        self.assertEqual(v.x, 0.0)
        self.assertEqual(v.y, 0.0)
        self.assertEqual(v.z, 0.0)

    def test_assign_exception(self):
        v = Vector3D()
        with self.assertRaises(Exception):
            v.x = 1.0
        with self.assertRaises(Exception):
            v.y = 1.0
        with self.assertRaises(Exception):
            v.z = 1.0

if __name__ == '__main__':
    unittest.main()
