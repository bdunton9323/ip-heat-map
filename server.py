import tornado.ioloop
import tornado.web
import tornado.httpserver
import simplejson
from pymongo import MongoClient
from coordinate import CoordinateUtils

import os
from socket import AF_INET

class GetDataHandler(tornado.web.RequestHandler):
         
    # TODO: this is called for every requeest. I might want to just use the  adapter that I had before
    def initialize(self, mongo, db_name, collection_name):
        print "in initialize"
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
    
    Note: The points have to be in lat,long order
    '''
    def build_query(self, plane):
        point1 = plane[0]
        point2 = plane[1]
        
        coords = []
        # mongo expects the points in long,lat order
        coords.append([point1[1], point1[0]])
        coords.append([point1[1], point2[0]])
        coords.append([point2[1], point2[0]])
        coords.append([point2[1], point1[0]])
        # Add the first point again to close the polygon
        coords.append([point1[1], point1[0]])
        
        query = {"loc": {"$geoWithin": {"$geometry": {"type": "Polygon", "coordinates": [coords]}}}}
        print query
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
        print "request: ", self.request.body
        lat1, long1, lat2, long2, zoom = self.parse_args()
       
        print "point1: ", lat1, long1
        print "point2: ", lat2, long2
        print "zoom: ", zoom
        
        plane = [(lat1, long1), (lat2, long2)]
        squares = plane
        apply_averaging = False
        
        count = self.collection.count(self.build_query(plane))
        print "Got", count, "documents from mongo"
        
        if count > 5000:
            apply_averaging = True
            squares = CoordinateUtils.partition_grid(10, plane)
        
        points = []
        for square in squares:
            cursor = self.collection.find(self.build_query(plane))
            points_in_square = []
            for doc in cursor:
                result = doc['loc']['coordinates']
                # TODO: the intensity might need to be scaled by the zoom factor
                points_in_square.append((result[1], result[0], .2))
            if apply_averaging:
                points.append( CoordinateUtils.find_center(points_in_square) )
            else:
                points.extend(points_in_square)
        
        #points = []
        #for doc in cursor:
        #    result = doc['loc']['coordinates']
        #    # tuple is (lat, long, weight)
        #    points.append((result[1], result[0], 10))
        
        
        response = {'data': points}
        self.write(response);
        
    #def apply_averaging(self, points, zoom):
    #    CartesianUtils.partition_grid(10, )
    #    PointAverager.collapse([[1, 1, 1], [-1, -1, 1]]);

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