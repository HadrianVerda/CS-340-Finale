# Imported Libaries # my code
from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint

# class structure initalization # not my code

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to access the MongoDB
        # databases and collections. This is hard-wired to use the aac
        # database, the animals collection, and the aac user.
        #
        # You must edit the password below for your environment.
        #
        # Connection Variables
        #
        HOST = 'localhost'
        PORT = 27017
        DB = 'aac'
        COL = 'animals'

        # Initialize Connection
        uri = f"mongodb://{username}:{password}@{HOST}:{PORT}"

        self.client = MongoClient(uri)
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]


# record_number helper function # my code
# this code finds the last record in the collection by creating a list in
# reverse order than retrieving the top of that list

    def findNextRecNum(self):

        last_record = self.collection.find_one(sort = [("rec_num", -1)])
        # if statement to prevent crash

        if last_record is None:
            pprint("No Last Document Defaulting To 1")
            return 1


        #pprint("successfully retrieved rec_num") # debug line
        return last_record["rec_num"] + 1


# Create Method # my code
# returns true if successful returns false when not successful.
    def create(self, data):
        if data is not None:

            data["rec_num"] = self.findNextRecNum()

            result = self.collection.insert_one(data)  # data should be in dictionary format

            if result.inserted_id:
                return True

        else:
            raise Exception("Nothing to save, because data parameter is empty")
        return False

#Retrieve Method # my code
#This method works by using a MongoDB query and passing it as an input
#This method uses MongoClient to achieve this
    def read(self, query):

        cursor = self.collection.find(query)

        return list(cursor)
# Update Method # my code
#This method works by using the $set operator to gather a set of documents
# and than passing them through update many.
# Update many can be used for One document which negates the need for update_One.

    def update(self, query, data):

        result = self.collection.update_many(query,{"$set": data})

        return result.modified_count # returns the amount of changed documents.

# Delete Method
# This is the delete method/
    def delete(self, query):

        result = self.collection.delete_many(query)

        return result.deleted_count


    #Adrian Azevedo




