from pymongo import MongoClient
from importer import MongoFullImporter
import sys

'''
Loads the IPv6 data into a given mongo collection
'''
class IPv6DataLoader(object):   
    def __init__(self, file_name):
        self.file_name = file_name

    def import_data(self, collection):

        with open(self.file_name) as datafile:
            for line in datafile:
                tokens = line.split(",")
                lat = tokens[7]
                lon = tokens[8]
                collection.insert_one(self._build_mongo_doc(lat, lon))

    def _build_mongo_doc(self, lat, lon):
        doc = {}

        # NOTE: mongo coordinates are listed "backwards" in (long,lat) order!
        doc['loc'] = {"type": "Point", "coordinates": [float(lon), float(lat)]}
        
        return doc


def print_usage():
    print "Usage: python etl6.py <data-file> <mongo-uri>"
        
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_usage()
    else:
        file_name = sys.argv[1]
        mongo_uri = sys.argv[2]
        mongo = MongoClient(mongo_uri)
        data_loader = IPv6DataLoader(file_name)
        importer = MongoFullImporter(mongo, "ipmap", "locations_v6", data_loader)
        print "Importing IPv6 data"
        importer.import_data()
        print "Done!"