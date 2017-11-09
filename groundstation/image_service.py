from .database import database
from .image import Image
from motor import motor_asyncio
import asyncio

class ImageService:

    def __init__(self):
        self._images = [] # List of Image instances
        self.loop = asyncio.get_event_loop()
        self.load_images_from_database()
        
    # Access database to load all image metadata
    def load_images_from_database(self):
        try:
            self._images = self.loop.run_until_complete(database.do_find_images())
        except:
            print("No images available")        

    # Find an image in the list using the uuid
    # If it does not exist, search the database and return it
    # If still not found, return None
    # Ensure that the jpg data for the image is loaded
    def get_image_by_id(self, uuid):
        image = next((img for img in self._images if img._uuid == uuid), None)

        if image is not None:
            if image.jpeg_data is None:
                image.load_from_filesystem()
            return image
        # TODO: Search database
        else:
            pass

        return None

    # If we receive a new image, store it & match telemetry
    def add_new_image(self, jpeg, timestamp):
        
        image = Image()
        image.timestamp = timestamp
        image.jpeg_data = jpeg
        image.save_jpeg_to_filesystem()
        image.match_telemetry()

        self._images.append(image)

image_service = ImageService()
