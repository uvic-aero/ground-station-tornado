from motor import motor_asyncio
import motor
import asyncio
import pprint
import time
import pymongo
from bson.objectid import ObjectId


class Database:
    def __init__(self):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(
            'localhost', 27017)
        self.loop = asyncio.get_event_loop()
        self._db = self._client.get_database('aero')
        self._image_collection = self._db.get_collection('images')
        self._telemetry_collection = self._db.get_collection('telemetry')
        self._image_tag_collection = self._db.get_collection('image_tags')
        return None

    @property
    async def image_collection(self):
        return self._image_collection

    @property
    async def telemetry_collection(self):
        return self._telemetry_collection

    # write new image to image collection: params(image object)
    async def add_image(self, document):
        result = await self._image_collection.insert_one(document)

    async def insert_telemetry(self, document):
        result = await self._telemetry_collection.insert_one(document)

    async def insert_image_telemetry(self, document):
        result = await self._image_collection.insert_one(document)

    # returns all "image_objects" in the image collection
    async def do_find_images(self):
        cursor = self._image_collection.find({})
        temp = []
        for document in await cursor.to_list(length=None):
            temp.append(document)
        return temp

    # If image_id is a valid image id, then return the next 'count' images that have a timestamp
    # less than the image referenced by image_id
    # The purpose is for pagination. Assuming sorted by timestamp greatest to least,
    # if we load the newest 20 images, then this function would allow us to load the next 20 images
    # that come after the last image in the previous set. Newer images have a larger timestamp
    # This requires sorting by timestamp, searching for images with lesser timestamp than image_id, and limiting
    # the return to 'count' number of results

    async def get_next_images(self, _id = None, count = 3):
        if(_id == None):
            cursor = await self._image_collection.find_one({})
        else: 
            cursor = await self._image_collection.find_one({"_id": ObjectId(_id)})
        
        # check for cursor existince
        if cursor == None:
            return
    
        result = await self._image_collection.find({'timestamp': {'$not': {'$gt': cursor['timestamp']}}}, sort=[('timestamp', pymongo.DESCENDING)], limit=count).to_list(length=None)
        pprint.pprint(result)
        return result

    # returns all telemetry objects in telemetry collection
    async def do_find_telemetry(self):
        cursor = self._telemetry_collection.find({'type': 'telemetry'})
        temp = []
        for document in await cursor.to_list(length=None):
            temp.append(document)
        return temp

    #----important images----#

    # write new image tag to image_tag collection: params(uuid)
    async def insert_image_tag(self, tag_id):
        result = await self._image_tag_collection.insert({'uuid': tag_id})

    # remove specified image tag from image_tag collection: params(uuid)
    async def remove_image_tag(self, tag_id):
        result = await self._image_tag_collection.remove({'uuid': tag_id})

    # return a list of all image_tag objects from image_tag collection
    async def find_all_image_tags(self):
        cursor = self._image_tag_collection.find({})
        temp = []
        for document in await cursor.to_list(length=None):
            temp.append(document)
        return temp


database = Database()

loop = asyncio.get_event_loop()
#loop.run_until_complete(database.get_next_images(count = 3, _id = '5a17825b399d9250423c06c3'))
loop.run_until_complete(database.find_all_image_tags())

#To Test
#1. find images.
#
#
#
#
#
#