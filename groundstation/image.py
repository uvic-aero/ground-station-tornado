import uuid
from .database import database #place period directly before first database on this line
import asyncio

# Basic concept of an image
# Can have image data received over the network or loaded from the filesystem,
# telemetry data that's been matched in, and the idea of a persistent file location
class Image:
    def __init__(self, uuid_param=None):
        self.loop = asyncio.get_event_loop()
        self.uuid = None
        self.jpeg_data = None
        self.file_location = None
        self.timestamp = None
        self.telemetry = None

    # Use the filesystem location to open this image
    # File location must exist
    def load_jpeg_from_filesystem(self):  # typo
        with open(self.file_location, 'rb') as f:
            self.jpeg_data = f.read()

    # Save jpeg data in memory to the filesystem & record file location
    # Save to './images/{self._uuid}.jpg'
    def save_jpeg_to_filesystem(self):
        self.file_location = "images/" + str(self.uuid) + ".jpg"
        print('Saving new image: %s' % self.file_location)
        with open(self.file_location, 'wb') as f:
            f.write(self.jpeg_data)

        self.loop.create_task(database.update_image(self.uuid, {'$set': {'file_location': self.file_location}}))

    # Garbage collect unneeded image data to save memory
    def discard_jpeg_data(self):
        self.jpeg_data = None

    # Use telemetry service to find telemetry for this image/timestamp
    # The timestamp in this image must exist and be valid
    async def match_telemetry(self):
        self.telemetry = await database.get_nearest_telemetry(self.timestamp)
        print("found telemetry")
        print(self.telemetry)

        return self.telemetry

    # (over)write this image data to database
    async def persist_to_database(self):
        document = {
            'timestamp' : self.timestamp, 
            'file_location' : self.file_location,
            'telemetry' : self.telemetry
        }

        self.uuid = await database.insert_image(document)

        self.save_jpeg_to_filesystem()

