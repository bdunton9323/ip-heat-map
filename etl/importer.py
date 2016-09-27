from pymongo import GEOSPHERE

'''
Imports the full data set into a mongo collection in a single operation. It
does this by building a temporary collection and then swapping it with the
real collection.
'''
class MongoFullImporter(object):
    def __init__(self, mongo, db_name, collection_name, loader):
        self.mongo = mongo
        self.loader = loader
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
        self.loader.import_data(self.new_collection)

        # Don't import if something went catastrophically wrong
        if self.new_collection.count() > 0:
            # swapping the collections
            self.old_collection.drop()
            self.new_collection.rename(self.coll)