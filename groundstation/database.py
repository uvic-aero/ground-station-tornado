from motor import motor_asyncio


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

database = Database()
