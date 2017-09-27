from .database import database
from .image import Image

class ImageService:

    def __init__(self):
        self._images = [] # List of Image instances

        self.load_images_from_database()

    # Access database to load all image metadata
    def load_images_from_database(self):
        pass

    # Find an image in the list using the uuid
    def get_image_by_id(self, uuid):
        pass

    # If we receive a new image, store it & match telemetry
    def add_new_image(self, jpeg):
        
        image = Image()
        image.jpeg_data = jpeg
        image.save_jpeg_to_filesystem()
        image.match_telemetry()

        self._images.append(image)
        
image_service = ImageService()
