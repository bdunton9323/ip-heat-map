import unittest
from averager import PointAverager

class TestPointAverager(unittest.TestCase):
    def setUp(self):
        self.averager = PointAverager()

    def test_parameter_bounds(self):        
        self.assertRaises(ValueError, self.averager.collapse, [])
        self.assertRaises(ValueError, self.averager.collapse, None)
        
    def test_center_on_origin(self):
        avg = self.averager.collapse([[1, 1, .5], [-1, -1, .5]])
        self.assertEqual(avg, [0,0,.5])
        
        avg = self.averager.collapse([[2, 1, 3], [-2, -1, 3]])
        self.assertEqual(avg, [0,0,3])
        
        avg = self.averager.collapse([[2.5, -1.9987, .2], [-2.5, 1.9987, .2]])
        self.assertEqual(avg, [0, 0, .2])
    
    def test_all_zero_weight(self):
        avg = self.averager.collapse([[1,1,0], [-1,-1,0]])
        
    def test_center_not_on_origin(self):
        avg = self.averager.collapse([[4, 2, .5], [2, 1, .5]])
        self.assertEqual(avg, [3, 1.5, .5])