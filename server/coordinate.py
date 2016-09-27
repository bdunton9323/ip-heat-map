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
            return []
        else:
            return [total_long/total_weight, total_lat/total_weight, total_weight]
        
    '''
    Divides a plane into a grid. The plane is given by two points: the upper-left corner
    and the lower-right corner.
    Returns a list of corner pairs, one for each grid square.
    '''
    @staticmethod
    def partition_grid(width, plane):
        LONG = 0
        LAT = 1
        # TODO: does it matter if these are lat,long or long,lat?
        upper_left = plane[0]
        lower_right = plane[1]
        
        if upper_left[LONG] > lower_right[LONG] or upper_left[LAT] < lower_right[LAT]:
            raise ValueError("The coordinates were backward UL: " + str(upper_left) + ", LR: " + str(lower_right))
            
        x_dist = abs(lower_right[LONG] - upper_left[LONG])
        y_dist = abs(upper_left[LAT] - lower_right[LAT])
        
            
        grid = []
        dx = x_dist / width
        dy = y_dist / width
        
        ul_x = upper_left[LONG]
        ul_y = upper_left[LAT]
        lr_x = ul_x + dx
        lr_y = ul_y - dy
        for y in xrange(width):
            for x in xrange(width):
                #print "appending UL:", ul_x, ul_y, ", LR: ", lr_x, lr_y
                grid.append([(ul_x, ul_y), (lr_x, lr_y)])
                ul_x += dx
                lr_x += dx
            ul_y -= dy
            lr_y -= dy
            ul_x = upper_left[LONG]
            lr_x = ul_x + dx
        
        return grid
        #return [[(0, 10), (0,0)], [(10,10), (10,0)]]