from pymongo import MongoClient
from importer import MongoFullImporter
import sys

'''
Loads the IPv4 data into a given mongo collection
'''
class DataLoader(object):
    def __init__(self, block_file, location_file):
        self.block_file = block_file
        self.location_file = location_file
        
    def _build_location_index(self):
        locations = {}
        with open(self.location_file) as datafile:
            for _ in xrange(2):
                next(datafile)

            for line in datafile:
                tokens = line.split(",")
                location_code = tokens[0]
                lat = tokens[5]
                lon = tokens[6]
                locations[location_code] = (lat, lon)
                  
        print "Read in {0} locations".format(len(locations))
        return locations

    def import_data(self, collection):
        locations = self._build_location_index()

        with open(self.block_file) as datafile:
            # skip the header rows
            for _ in xrange(2):
                next(datafile)

            for line in datafile:
                tokens = line.split(",")
                ip_start = tokens[0][1:-2]
                ip_end = tokens[1][1:-2]
                location_code = tokens[2][1:-2]
                point = locations[location_code]
                collection.insert_one(self._build_mongo_doc(
                        location_code, ip_start, ip_end, point[0], point[1]))

    def _build_mongo_doc(self, location_code, ip_start, ip_end, lat, lon):
        doc = {}
        doc['ipstart'] = ip_start
        doc['ipend'] = ip_end
        doc['locationCode'] = location_code

        # NOTE: mongo coordinates are listed "backwards" in (long,lat) order!
        doc['loc'] = {"type": "Point", "coordinates": [float(lon), float(lat)]}
        
        return doc

def print_usage():
    print "Usage: python etl4.py <block-file> <location-file> <mongo-uri>"
        
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print_usage()
    else:
        block_file = sys.argv[1]
        location_file = sys.argv[2]
        mongo_uri = sys.argv[3]

        mongo = MongoClient(mongo_uri)
        data_loader = DataLoader(block_file, location_file)
        mongo_importer = MongoFullImporter(mongo, "ipmap", "locations_v4", data_loader)
        print "Importing IPv4 data"
        mongo_importer.import_data()
        print "Done!"