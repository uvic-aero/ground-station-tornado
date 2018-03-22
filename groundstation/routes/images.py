import requests 
import json
import base64
from ..image_service import image_service
from tornado import web 
from ..database import database
import asyncio

class ImagesHandler (web.RequestHandler):
	def post(self):
		data = json.loads(self.request.body)
		timestamp = data ["timestamp"]
		image = base64.b64decode(data ["image"])

		image_service.add_new_image(timestamp,image)

	@web.asynchronous
	def get(self):
		asyncio.get_event_loop().create_task(database.do_find_images(self._images_received))

	def _images_received(self, images):
			self.write ({'images': images})
			self.finish()

class ImagesByIdHandler (web.RequestHandler):
	def post(self):
		pass


class ImagesNextHandler (web.RequestHandler):
	def post(self):
		pass


class ImagesTagHandler (web.RequestHandler):
	def post(self):
		pass