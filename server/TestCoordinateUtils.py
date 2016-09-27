import unittest
from coordinate import CoordinateUtils

class TestPointAverager(unittest.TestCase):
    #def setUp(self):
    #    self.averager = PointAverager()

    def test_center_param_bounds(self):        
        self.assertRaises(ValueError, CoordinateUtils.find_center, [])
        self.assertRaises(ValueError, CoordinateUtils.find_center, None)
        
    def test_center_on_origin(self):
        avg = CoordinateUtils.find_center([[1, 1, .5], [-1, -1, .5]])
        self.assertEqual(avg, [0,0,1])
        
        avg = CoordinateUtils.find_center([[2, 1, 3], [-2, -1, 3]])
        self.assertEqual(avg, [0,0,6])
        
        avg = CoordinateUtils.find_center([[2.5, -1.9987, .2], [-2.5, 1.9987, .2]])
        self.assertEqual(avg, [0, 0, .4])
    
    def test_center_zero_weight(self):
        avg = CoordinateUtils.find_center([[1,1,0], [-1,-1,0]])
        self.assertEqual(avg, [])
        
    def test_center_not_on_origin(self):
        avg = CoordinateUtils.find_center([[4, 2, .5], [2, 1, .5]])
        self.assertEqual(avg, [3, 1.5, 1])
    
    # This case was causing a bug in the application, so I added this test
    def test_partition_NW_hemisphere(self):
        partitions = CoordinateUtils.partition_grid(1, [
            [-74.088191986084, 40.80601358609009, 1], 
            [-73.85421752929689, 40.760130667719636, 1]])
        self.assertEqual(partitions, [
            [(-74.088191986084, 40.80601358609009), (-73.85421752929689, 40.760130667719636)]])
        
    def test_partition(self):
        # the grid is the whole rectangle
        squares = CoordinateUtils.partition_grid(1, [[0.5, 10.5], [2, 0]])
        expected = [[(0.5, 10.5), (2, 0)]]
       
        # a unit grid
        squares = CoordinateUtils.partition_grid(2, [[0, 2], [2, 0]])
        expected = [
            [(0,2), (1,1)],
            [(1,2), (2,1)],
            [(0,1), (1,0)],
            [(1,1), (2,0)]]
        self.assertEqual(squares, expected)
        
        # a grid that has corners in all quadrants
        squares = CoordinateUtils.partition_grid(2, [[-1,1], [1,-1]])
        expected = [
            [(-1,1), (0,0)],
            [(0,1), (1,0)],
            [(-1,0), (0,-1)],
            [(0,0), (1,-1)]]
        self.assertEqual(squares, expected)
        