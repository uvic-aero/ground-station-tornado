from .database import database
from .image import Image
from tornado import ioloop

class ImageService:

    def __init__(self):
        self._images = [] # List of Image instances
        self.loop = ioloop.IOLoop.instance().asyncio_loop

    def start(self):
        print("Starting image service")
        self.load_images_from_database()

    # Access database to load all image metadata
    def load_images_from_database(self):
        try:
            self.loop.create_task(database.do_find_images(self._load_images_callback))
        except:
            print("No images loaded from database")

    def _load_images_callback(self, images):
        print("Loaded %s initial images from database" % len(images))
        self._images = self._images + images

    # Find an image in the list using the uuid
    # If it does not exist, search the database and return it
    # If still not found, return None
    # Ensure that the jpg data for the image is loaded
    def get_image_by_id(self, uuid):
        image = next((img for img in self._images if img.uuid == uuid), None)

        if image is not None:
            if image.jpeg_data is None:
                image.load_from_filesystem()
            return image
        # TODO: Search database
        else:
            pass

        return None

    # If we receive a new image, store it & match telemetry
    def add_new_image(self, timestamp, jpeg):

        image = Image()
        image.timestamp = timestamp
        image.jpeg_data = jpeg
        image.timestamp = timestamp
        image.persist_to_database(self._add_image_callback)

    # If image successfully inserted, save the id & data to disk
    def _add_image_callback(self, image, id):

        image.uuid = id
        image.save_jpeg_to_filesystem()
        image.match_telemetry()

        self._images.append(image)

image_service = ImageService()

