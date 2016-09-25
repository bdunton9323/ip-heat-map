import unittest
from coordinate import CoordinateUtils

class TestPointAverager(unittest.TestCase):
    #def setUp(self):
    #    self.averager = PointAverager()

    def test_parameter_bounds(self):        
        self.assertRaises(ValueError, CoordinateUtils.find_center, [])
        self.assertRaises(ValueError, CoordinateUtils.find_center, None)
        
    def test_center_on_origin(self):
        avg = CoordinateUtils.find_center([[1, 1, .5], [-1, -1, .5]])
        self.assertEqual(avg, [0,0,.5])
        
        avg = CoordinateUtils.find_center([[2, 1, 3], [-2, -1, 3]])
        self.assertEqual(avg, [0,0,3])
        
        avg = CoordinateUtils.find_center([[2.5, -1.9987, .2], [-2.5, 1.9987, .2]])
        self.assertEqual(avg, [0, 0, .2])
    
    def test_all_zero_weight(self):
        avg = CoordinateUtils.find_center([[1,1,0], [-1,-1,0]])
        
    def test_center_not_on_origin(self):
        avg = CoordinateUtils.find_center([[4, 2, .5], [2, 1, .5]])
        self.assertEqual(avg, [3, 1.5, .5])