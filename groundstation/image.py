import uuid
from .database import database #place period directly before first database on this line
import asyncio
#from PIL import Image as PILImage


# Basic concept of an image
# Can have image data received over the network or loaded from the filesystem,
# telemetry data that's been matched in, and the idea of a persistent file location
class Image:
    def __init__(self, uuid_param=None):
        self.loop = asyncio.get_event_loop()
        #self._uuid = uuid.uuid4() if uuid_param is None else uuid_param  # Unique identifier used by database. If it does not exist, create it
        self.jpeg_data = None
        self.file_location = None
        self.timestamp = None
        self.telemetry = None

    # Use the filesystem location to open this image
    # File location must exist
    def load_jpeg_from_filesystem(self):  # typo
        self.jpeg_data = PILImage.open(self.file_location)

    # Save jpeg data in memory to the filesystem & record file location
    # Save to './images/{self._uuid}.jpg'
    def save_jpeg_to_filesystem(self):
        location = "./images/" + str(self._uuid) + ".jpg"
        self.jpeg_data.save(location)
        self.file_location = location

    # Garbage collect unneeded image data to save memory
    def discard_jpeg_data(self):
        self.jpeg_data = None

    # Use telemetry service to find telemetry for this image/timestamp
    # The timestamp in this image must exist and be valid
    def match_telemetry(self):
        pass

    # (over)write this image data to database
    def persist_to_database(self):
        document = {
        'timestamp' : self.timestamp, 
        'file_location' : self.file_location,
        'telemetry_id' : self.telemetry._uuid if self.telemetry is not None else None
        }
        self.loop.run_until_complete(database.insert_image_telemetry(document))

