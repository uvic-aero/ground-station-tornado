from tornado import web
import tornado
import sys
sys.path.append('../database.py')
from ..database import database
from motor import motor_asyncio
import motor
import asyncio
import json

class ImageByCoordinateHandler(web.RequestHandler):
    @web.asynchronous
    def get(self):
        print('get image by cocordinate called')
        a = [-73.9376, 40.8302]
        b = [-73.9375, 40.8304]
        loop = asyncio.get_event_loop()
        loop.create_task(database.find_by_coordinates(a, b, self._images_received))
    def _images_received(self, images):
        # send json result
        self.write(json.dumps(images))
        self.finish()