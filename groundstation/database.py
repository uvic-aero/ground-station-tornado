from motor import motor_asyncio
import pprint


class Database:
    def __init__(self):
        self._client = motor_asyncio.AsyncIOMotorClient()
        self._db = self._client.get_database('aero')
        self._image_collection = self._db.get_collection('images')
        self._telemetry_collection = self._db.get_collection('telemetry')

    @property
    def image_collection(self):
        return self._image_collection

    @property
    def telemetry_collection(self):
        return self._telemetry_collection

        #takes in collection and entry as params
    def add_entry(self, entry):
        images = database.image_collection
        self._image_collection.insert(entry)
        print('new entry: ', entry)
       

#Test Code
database = Database()
image = {'type': 'image', 'name': 'this entry is added through def'}
database.add_entry(image)
