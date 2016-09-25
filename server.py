import tornado.ioloop
import tornado.web
import tornado.httpserver
import simplejson
from pymongo import MongoClient

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
    The points are in lat,long order
    '''
    def build_query(self, point1, point2):
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
        
    def get(self, *args, **kwargs):
        print "request: ", self.request.body
        # TODO: handle bad requests
        lat1 = float(self.get_argument("lat1", None))
        long1 = float(self.get_argument("long1", None))
        lat2 = float(self.get_argument("lat2", None))
        long2 = float(self.get_argument("long2", None))
        print "point1: ", lat1, long1
        print "point2: ", lat2, long2
        
        points = []
        cursor = self.collection.find(self.build_query((lat1, long1), (lat2, long2)))

        points = []
        for doc in cursor:
            result = doc['loc']['coordinates']
            # lat, long, weight
            points.append((result[1], result[0], .3))
        
        response = {'data': points}
        self.write(response);
        
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