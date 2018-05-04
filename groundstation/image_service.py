from .database import database
from .image import Image
from .websocket import pubsub
from tornado import ioloop
from .constants import groundstation_url
import json

class ImageService:

    def __init__(self):
        self.loop = ioloop.IOLoop.instance().asyncio_loop

    def start(self):
        print("Starting image service")

    # If we receive a new image, store it & match telemetry
    async def add_new_image(self, timestamp, jpeg):

        image = Image()
        image.timestamp = timestamp
        image.jpeg_data = jpeg
        await image.match_telemetry()
        await image.persist_to_database()

        # Send to webclients
        await self.publish_image(image)

    async def publish_image(self, image):

        subscribers = pubsub.subscriptions.get_subscribers()

        for type in subscribers:
            if type != 'images':
                continue
            for sub in subscribers[type]:
                img = {
                    'url': groundstation_url + "/" + image.file_location,
                    '_id': str(image.uuid),
                    'timestamp': image.timestamp,
                    'telemetry': {
                        **image.telemetry,
                        '_id': str(image.telemetry['_id'])
                    },
                    'type': "image" # Tell webclient this is an image message
                }

                sub.write_message(json.dumps(img))

image_service = ImageService()

