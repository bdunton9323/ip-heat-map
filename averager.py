'''
Applies averaging across a set of points to adjust the resolution of
the displayable data. This is necessary when the zoom is too low and
the number of points is too large.
'''
class PointAverager(object):
    def __init__(self):
        pass
        
    '''
    A point is a tuple or list of [longtitude, latitude, weight]
    '''
    def collapse(self, points):
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
        
    def find_center(self, points):
        pass