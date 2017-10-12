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
        self.telemetry_array_from_db = []
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
        #params : (entry for upload); this function adds a telemetry object to DB
        result = await self._telemetry_collection.insert_one(document)
        print('result %s' % repr(result.inserted_id))
    
    async def get_image(self): 
        #params : (time stamp for desired object); function is designed to retreive object form DB
        pprint.pprint(self._image_collection.find({"type": "image"}))

    async def do_find(self): 
        cursor = self._telemetry_collection.find({'type': 'telemetry'})
        #telemetry_arr = []
        for document in await cursor.to_list(length = 100):
            self.telemetry_array_from_db.append(document);
            #pprint.pprint(document)
        
        

        

#Test Code
database = Database()
image = {
    'type': 'image',
    'width': 671,
    'height': 475,
    'url': 'test'
}
telemetry = {
    'type': 'telemetry',
    'lat': 45.709,
    'lon': 104.3467
}
#loop = asyncio.get_event_loop()
#loop.run_until_complete(database.add_image(image))
#loop = asyncio.get_event_loop()
#loop.run_until_complete(database.do_find())

#loop = asyncio.get_event_loop()
#loop.run_until_complete(database.insert_telemetry(telemetry))



