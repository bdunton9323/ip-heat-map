import tornado.ioloop
import tornado.web
import tornado.httpserver
import simplejson
from pymongo import MongoClient
from pymongo import GEOSPHERE

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

'''
Imports the full data set into a mongo collection in a single operation. It
does this by building a temporary collection and then swapping it with the
real collection.
'''
class MongoFullImporter(object):
    def __init__(self, mongo, db_name, collection_name):
        self.mongo = mongo
        self.coll = collection_name
        self.old_collection = self.mongo[db_name][self.coll]
        self.new_collection = self.mongo[db_name][self.coll + "_next"]
    
    def import_data(self):
        try:
            self._run_import()
        except Exception as e:
            print "Exception while importing. Database left intact. Error:", e
            self.new_collection.drop()
            
    def _run_import(self):
        # Clean up if the previous import failed
        if self.new_collection.count() > 0:
            self.new_collection.drop()

        self.new_collection.create_index([("loc", GEOSPHERE)])
        loader = DataLoader(self.mongo, self.new_collection)
        loader.import_data()

        # Don't import if something went catastrophically wrong
        if self.new_collection.count() > 0:
            # swapping the collections
            self.old_collection.drop()
            self.new_collection.rename(self.coll)
            
'''
Loads data into an existing mongo collection
'''
class DataLoader(object):
    BLOCK_FILE_NAME = "GeoLiteCity-latest\\GeoLiteCity_20160907\\GeoLiteCity-Blocks.csv"
    LOC_FILE_NAME = "GeoLiteCity-latest\\GeoLiteCity_20160907\\GeoLiteCity-Location.csv"
    
    def __init__(self, mongo_client, db_collection):
        self.db_collection = db_collection
        
    def _build_location_index(self):
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
    
    def import_data(self):
        locations = self._build_location_index()

        i = 0
        with open(self.BLOCK_FILE_NAME) as datafile:
            # skip the header rows
            for _ in xrange(2):
                next(datafile)
                
            for line in datafile:
                tokens = line.split(",")
                ip_start = tokens[0][1:-2]
                ip_end = tokens[1][1:-2]
                location_code = tokens[2][1:-2]
                point = locations[location_code]
                self.db_collection.insert_one(self._build_mongo_doc(
                        location_code, ip_start, ip_end, point[0], point[1]))
                
                #i += 1
                #if i == 10:
                #    return

    def _build_mongo_doc(self, location_code, ip_start, ip_end, lat, lon):
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
    loader = MongoFullImporter(mongo_client, "ipmap", "locations")
    loader.import_data()
    
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