from pymongo import MongoClient
from pymongo import GEOSPHERE

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
    BLOCK_FILE_NAME = "geodata\\GeoLiteCity-Blocks.csv"
    LOC_FILE_NAME = "geodata\\GeoLiteCity-Location.csv"
    
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

    def _build_mongo_doc(self, location_code, ip_start, ip_end, lat, lon):
        doc = {}
        doc['ipstart'] = ip_start
        doc['ipend'] = ip_end
        doc['locationCode'] = location_code

        # NOTE: mongo coordinates are listed "backwards" in (long,lat) order!
        doc['loc'] = {"type": "Point", "coordinates": [float(lon), float(lat)]}
        
        return doc

if __name__ == "__main__":
    # TODO: pick up mongo URI from command line or a config file
    mongo = MongoClient()
    loader = MongoFullImporter(mongo, "ipmap", "locations")
    loader.import_data()