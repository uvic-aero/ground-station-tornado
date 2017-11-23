from motor import motor_asyncio
import motor
import asyncio
import pprint
import time


class Database:
    def __init__(self):
        self._client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
        self._db = self._client.get_database('aero')
        self._image_collection = self._db.get_collection('images')
        self._telemetry_collection = self._db.get_collection('telemetry')
        self._telemetry_collection = self._db.get_collection('important_images')
        return None
    
        
    @property 
    async def image_collection(self):
        return self._image_collection

    @property
    async def telemetry_collection(self):
        return self._telemetry_collection

    async def add_image(self, document): 
        result = await self._image_collection.insert_one(document)

    async def insert_telemetry(self, document): 
        result = await self._telemetry_collection.insert_one(document)

    async def insert_image_telemetry(self, document):
        result = await self._image_collection.insert_one(document)

    
    async def do_find_images(self): 
        cursor = self._image_collection.find({'type': 'image_object'})
        temp = []
        for document in await cursor.to_list(length = None):
            temp.append(document);     
        return temp


#for important images 
    async def insert_image_tag(self, tag_id):
        result = await self._image_tag_collection.insert({'type': 'image_tag', 'uuid': tag_id})

    async def remove_image_tag(self, tag_id):
        result = await self._image_tag_collection.remove({'type': 'image_tag', 'uuid': tag_id})

    async def find_all_image_tags(self): 
        cursor = self._image_tag_collection.find({'type': 'image_tag'})
        temp = []
        for document in await cursor.to_list(length = None):
            temp.append(document);
        return temp

    # If image_id is a valid image id, then return the next 'count' images that have a timestamp
    # less than the image referenced by image_id
    # The purpose is for pagination. Assuming sorted by timestamp greatest to least, 
    # if we load the newest 20 images, then this function would allow us to load the next 20 images
    # that come after the last image in the previous set. Newer images have a larger timestamp
    # This requires sorting by timestamp, searching for images with lesser timestamp than image_id, and limiting
    # the return to 'count' number of results
    async def get_next_images(self, image_id, count):
        pass
        
    async def do_find_telemetry(self): 
        cursor = self._telemetry_collection.find({'type': 'telemetry'})
        temp = []
        for document in await cursor.to_list(length = None):
            temp.append(document);
        return temp
        
database = Database()
