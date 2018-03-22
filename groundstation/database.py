from motor import motor_asyncio
from tornado import ioloop
import motor
import asyncio
import pprint
import time
import pymongo
from bson.objectid import ObjectId


class Database:
    def __init__(self):
        # Configure motor to use tornado's native asyncio loop
        self._client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017, io_loop=ioloop.IOLoop.instance().asyncio_loop)
        self._db = self._client.get_database('aero')
        self._image_collection = self._db.get_collection('images')
        self._telemetry_collection = self._db.get_collection('telemetry')
        self._image_tag_collection = self._db.get_collection('image_tags')
        self._log_collection = self._db.get_collection('logs')

        return None
    
        
    @property 
    def image_collection(self):
        return self._image_collection

    @property
    def telemetry_collection(self):
        return self._telemetry_collection

    # write new image to image collection: params(image object)
    async def insert_image(self, document):
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


    async def find_image_by_id(self, id):
        result = self._image_collection.find({"_id": ObjectId(id)})
        return result

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
        #pprint.pprint(result)
        return result

    #Pass to sets of coordinate to retreive an group of images
    async def find_by_coordinates(self, coordinate_a = None, coordinate_b = None, callback = None):
        #coord_a is bottom left | coord_b is upper right
        if(coordinate_a == None or coordinate_b == None):
            return('Coordinate parameter is missing')
        cursor = self._image_collection.find({ 'location': { '$geoWithin':{ '$box': [ coordinate_a, coordinate_b ] } } })
        temp = []
        for document in await cursor.to_list(length=None):
            temp.append({**document, **{'_id': str(document['_id'])}})
        x = {'result':temp}
        callback(x)



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
    
    async def insert_log(self, document):
        msg = document["message"]
        sys = document['system']
        ts = document['timestamp']
        result = await self._log_collection.insert({'Time Stamp': ts, 'Message': msg, 'System': sys})

database = Database()

loop = asyncio.get_event_loop()
loop.create_task(database.do_find_images())

