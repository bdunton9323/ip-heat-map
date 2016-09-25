import tornado.ioloop
import tornado.web
import tornado.httpserver
import simplejson
from pymongo import MongoClient
from coordinate import CoordinateUtils

import os
from socket import AF_INET

class GetDataHandler(tornado.web.RequestHandler):
         
    # TODO: this is called for every request. I might want to just use the
    # adapter that I had before
    def initialize(self, mongo, db_name, collection_name):
        self.mongo = mongo
        self.collection = self.mongo[db_name][collection_name]
    
    def set_default_headers(self):
        # TODO: change to the web server's domain after I am done developing
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type, Origin, Accept")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    '''
    Build a mongo query to get the points in a given plane. The plane
    is a list of size 2, containing tuples representing the upper-right and
    lower-left corners, for example: [(40.78, -73.97), (40.80, -73.50)]
    
    Note: The points have to be in (longitude,lat) order
    '''
    def build_query(self, plane):
        LONG = 0
        LAT = 1
        point1 = plane[LONG]
        point2 = plane[LAT]
        
        coords = []
        # mongo expects the points in long,lat order
        coords.append([point1[LONG], point1[LAT]])
        coords.append([point1[LONG], point2[LAT]])
        coords.append([point2[LONG], point2[LAT]])
        coords.append([point2[LONG], point1[LAT]])
        # Add the first point again to close the polygon
        coords.append([point1[LONG], point1[LAT]])
        
        query = {"loc": {"$geoWithin": {"$geometry": {"type": "Polygon", "coordinates": [coords]}}}}
        #print query
        return query
        
    '''
    Extract the arguments and check for errors in the GET request
    '''
    def parse_args(self):
        error = False
        lat1, long1, lat2, long2, zoom = (None, None, None, None, None)
        try:
            lat1 = float(self.get_argument("lat1", None))
            long1 = float(self.get_argument("long1", None))
            lat2 = float(self.get_argument("lat2", None))
            long2 = float(self.get_argument("long2", None))
            zoom = int(self.get_argument("zoom", None))
        except:
            error = True
        if error or None in [lat1, long1, lat2, long2, zoom]:
            raise tornado.web.HTTPError(400)

        return lat1, long1, lat2, long2, zoom
            
    def get(self, *args, **kwargs):
        lat1, long1, lat2, long2, zoom = self.parse_args()
        
        plane = [(long1, lat1), (long2, lat2)]
        squares = [plane]
        apply_averaging = False
        
        count = self.collection.count(self.build_query(plane))
        print "Got", count, "documents from mongo"
        
        if count > 1000:
            apply_averaging = True
            squares = CoordinateUtils.partition_grid(5, plane)
        
        points = []
        for square in squares:
            cursor = self.collection.find(self.build_query(square))
            points_in_square = self.get_points_from_result(cursor)
            
            if points_in_square:
                if apply_averaging:
                    center = CoordinateUtils.find_center(points_in_square)
                    points.append(center)
                else:
                    points.extend(points_in_square)
        
        response = {'data': points}
        self.write(response);
        
    def get_points_from_result(self, cursor):
        points = []
        for doc in cursor:
            result = doc['loc']['coordinates']
            # TODO: intensity needs to take into account the number of points.
            # Also something needs to change with the zoom factor (higher blur? bigger 
            # circles?) When doing the partitioned version, the radius should reflect the
            # spread of points. Maybe I can base the radius on the maximum distance within 
            # that grid cell.
            
            # The map wants it in lat/long order, so just do it here to avoid
            # reordering the list later
            points.append((result[1], result[0], 5))
        return points

    def options(self, *args, **kwargs):
        print "handling options"
        #self.write('200')

def main():
    db_name = "ipmap"
    collection_name = "locations"
    
    mongo_client = MongoClient()
    port = 8888
    application = tornado.web.Application([
        (r"/getdata", GetDataHandler, {"mongo": mongo_client, "db_name": db_name, "collection_name": collection_name}),
        ],
        static_path = os.path.join(os.path.dirname(__file__), "static")
    )

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.bind(port, family=AF_INET)
    http_server.start(1)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()