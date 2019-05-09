import requests 
import json
from ast import literal_eval
import base64
from ..image_service import image_service
from tornado import web 
from ..database import database
import asyncio
from ..image import Image
from ..constants import groundstation_url

class ImagesHandler (web.RequestHandler):
   
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    async def post(self):
        data = json.loads(self.request.body)
        timestamp = data ["timestamp"]
        image = base64.b64decode(data["image"])
        telemetry = data["telemetry"]

        await image_service.add_new_image(timestamp, image, telemetry)

    @web.asynchronous
    def get(self):
        asyncio.get_event_loop().create_task(database.find_all_images(self._images_received))

    def _images_received(self, images):
        for image in images:
            image['url'] = groundstation_url + "/" + image['file_location']
        
        self.write ({'images': images})
        self.finish()
    
    def options(self):
        self.set_status(204)
        self.finish()

class ImagesByIdHandler (web.RequestHandler):
    @web.asynchronous
    def post(self, id):
        asyncio.get_event_loop().create_task(database.find_image_by_id(id, self.image_result))

    def image_result(self, image):
        self.write (image)
        self.finish()

class ImagesByIdJpgHandler (web.RequestHandler):
    @web.asynchronous
    def get(self, id):
        asyncio.get_event_loop().create_task(database.find_image_by_id(id, self.image_result))

    def image_result(self, image):
        if image is None:
            self.set_status(404)
        else:
            with open(image['file_location'], 'rb') as f:
                jpeg =  f.read()
                self.write (jpeg)
                self.set_header('Content-Type', 'image/jpeg')
        self.finish()

class ImagesNextHandler (web.RequestHandler):
    def post(self):
        pass

class ImagesTagHandler (web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

    async def post(self, id):
        # TODO: Verify the id is an actual existing image
        await database.insert_image_tag(id)
        self.write({})

    def options(self, id):
        self.set_status(204)
        self.finish()

class ImagesUntagHandler (web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

    async def post(self, id):
        # TODO: Verify the id is an actual existing image
        await database.remove_image_tag(id)
        self.write({})

    def options(self, id):
        self.set_status(204)
        self.finish()
