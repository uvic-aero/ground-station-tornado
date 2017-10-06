from motor import motor_asyncio
import motor.motor_asyncio
import asyncio
import pprint
import time


class Database:
    def __init__(self):
        self._client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
        self._db = self._client.get_database('aero')
        self._image_collection = self._db.get_collection('images')
        self._telemetry_collection = self._db.get_collection('telemetry')
        
    @property
    def image_collection(self):
        return self._image_collection

    @property
    def telemetry_collection(self):
        return self._telemetry_collection

    async def add_image(self, entry): 
        result = await self._image_collection.insert(entry)
        print('result %s' % repr(result))

    async def add_telemetry(self, entry): 
        #params : (entry for upload); this function adds a telemetry object to DB
        result = await self._telemetry_collection.insert(entry)
        print('result %s' % repr(result))
    
    async def get_image(self): 
        #params : (time stamp for desired object); function is designed to retreive object form DB
        pprint.pprint(self._image_collection.find({"type": "image"}))
        

#Test Code
database = Database()

