from motor import motor_asyncio
import motor
import asyncio
import pprint
import time

#delete after testing
import uuid


class Database:
    def __init__(self):
        self._client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
        self.loop = asyncio.get_event_loop()
        self._db = self._client.get_database('aero')
        self._image_collection = self._db.get_collection('images')
        self._telemetry_collection = self._db.get_collection('telemetry')
        self._image_tag_collection = self._db.get_collection('image_tags')
        #self.telemetry_array_from_db = []
        #self.image_array_from_db = []
        return None
    
        
    @property 
    async def image_collection(self):
        return self._image_collection

    @property
    async def telemetry_collection(self):
        return self._telemetry_collection

    async def add_image(self, document): 
        result = await self._image_collection.insert_one(document)
        print('result %s' % repr(result.inserted_id))
      
    async def insert_telemetry(self, document): 
        result = await self._telemetry_collection.insert_one(document)
        print('result %s' % repr(result.inserted_id))
    
    async def do_find_images(self): 
        cursor = self._image_collection.find({'type': 'image'})
        temp = []
        for document in await cursor.to_list(length = None):
            temp.append(document);     
        return temp
        
    async def do_find_telemetry(self): 
        cursor = self._telemetry_collection.find({'type': 'telemetry'})
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
        
        

        

#Test Code
database = Database()

#x = database.loop.run_until_complete(database.find_all_image_tags())
#print(x)


#loop = asyncio.get_event_loop()
#loop.run_until_complete(database.do_find())

#loop = asyncio.get_event_loop()
#loop.run_until_complete(database.insert_telemetry(telemetry))



#event loop.starttask