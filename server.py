import tornado.ioloop
import tornado.web
import tornado.httpserver
import simplejson
from pymongo import MongoClient

import os
from socket import AF_INET


class GetDataHandler(tornado.web.RequestHandler):
    def initialize(self, mongo):
        self.mongo = mongo
    
    def set_default_headers(self):
        # TODO: change to 'http://localhost:8080' after I am done developing
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type, Origin, Accept")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        
    def get(self, *args, **kwargs):
        db = self.mongo['ipmap']
        collection = db['locations']
        cursor = collection.find()
        for doc in cursor:
            print doc['loc']['coordinates']
        
    def x_get(self, *args, **kwargs):
        print "request: ", self.request.body
        lat1 = self.get_argument("lat1", None)
        long1 = self.get_argument("long1", None)
        lat2 = self.get_argument("lat2", None)
        long2 = self.get_argument("long2", None)
        print "point1: ", lat1, long1
        print "point2: ", lat2, long2
        
        points = [[35, -78, .2], 
            [35.97, -78.89, .2], 
            [35.97, -78.89, .2], 
            [35.97, -78.89, .2], 
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2],
            [35.97, -78.89, .2]]
        response = {'data': points}
        self.write(response);
        
    def options(self, *args, **kwargs):
        print "handling options"
        #self.write('200')
        

        
class DataLoader(object):
    BLOCK_FILE_NAME = "GeoLiteCity-latest\\GeoLiteCity_20160907\\GeoLiteCity-Blocks.csv"
    LOC_FILE_NAME = "GeoLiteCity-latest\\GeoLiteCity_20160907\\GeoLiteCity-Location.csv"
    
    def __init__(self, mongo, db_name, collection_name):
        self.mongo = mongo
        # TODO: test what happens if the database or collection doesn't exist
        self.coll = self.mongo[db_name][collection_name]
        
    def build_location_index(self):
        locations = {}
        with open(self.LOC_FILE_NAME) as datafile:
            for _ in xrange(2):
                next(datafile)

            for line in datafile:
                tokens = line.split(",")
                location_code = tokens[0]
                lat = tokens[5]
                lon = tokens[6]
                locations[location_code] = (lat, lon)
                  
        print "Read", len(locations), "locations"
        return locations
    
    def load_file(self, mongo_client):
        locations = self.build_location_index()

        i = 0
        with open(self.BLOCK_FILE_NAME) as datafile:
            # skip the header rows
            for _ in xrange(2):
                next(datafile)
                
            for line in datafile:
                tokens = line.split(",")
                print tokens
                # I don't actually need the ranges. It's only the points we care about, but let's put it in mongo anyway.
                ip_start = tokens[0][1:-2]
                ip_end = tokens[1][1:-2]
                location_code = tokens[2][1:-2]
                point = locations[location_code]
                #print "mongo doc:", self.build_mongo_doc(location_code, ip_start, ip_end, point[0], point[1])
                self.coll.insert_one(self.build_mongo_doc(
                        location_code, ip_start, ip_end, point[0], point[1]))
                
                i += 1
                if i == 10:
                    return

    def build_mongo_doc(self, location_code, ip_start, ip_end, lat, lon):
        doc = {}
        doc['ipstart'] = ip_start
        doc['ipend'] = ip_end
        doc['locationCode'] = location_code

        # NOTE: mongo coordinates are listed "backwards" in (long,lat) order!
        doc['loc'] = {"type": "Point", "coordinates": [float(lon), float(lat)]}
        
        return doc

def main():
    # TODO: pick up mongo URI from command line or a config file
    mongo_client = MongoClient()
    loader = DataLoader(mongo_client, "ipmap", "locations")
    loader.load_file(mongo_client)
    
    port = 8888

    application = tornado.web.Application([
        (r"/getdata", GetDataHandler, {"mongo": mongo_client}),
        ],
        static_path = os.path.join(os.path.dirname(__file__), "static")
    )

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.bind(port, family=AF_INET)
    http_server.start(1)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()