'''
Applies averaging across a set of points to adjust the resolution of
the displayable data. This is necessary when the zoom is too low and
the number of points is too large.
'''
class CoordinateUtils(object):
        
    '''
    A point is a tuple or list of [latitude, longitude, weight]
    Returns the weighted average of the points (the center of mass)
    '''
    @staticmethod
    def find_center(points):
        if not points:
            raise ValueError("List of points cannot be empty")
            
        sum = [0, 0, 0]
        total_weight, total_long, total_lat = (0.0, 0.0, 0.0)
        for p in points:
            total_long += float(p[0]) * float(p[2])
            total_lat += float(p[1]) * float(p[2])
            total_weight += p[2]

        if total_weight == 0:
            return [0, 0, 0]
        else:
            return [total_long/total_weight, total_lat/total_weight, total_weight/len(points)]
        
    '''
    Divides a plane into a grid. The plane is given by two points: the upper-left corner
    and the lower-right corner.
    Returns a list of corner pairs, one for each grid square.
    '''
    @staticmethod
    def partition_grid(width, plane):
        point1 = plane[0]
        point2 = plane[1]
        
        return [[(0, 10), (0,0)], [(10,10), (10,0)]]