import requests 
import json
import base64
from image_service import image_service
from tornado import web 


class ImagesHandler (web.RequestHandler):
	def post(self):
		data = json.loads(self.request.body)
		timestamp = data ["timestamp"]
		image = base64.b64decode(data ["image"])

		image_service.add_new_image(timestamp,image)

	def get(self):
		pass

class ImagesByIdHandler (web.RequestHandler):
	def post(self):
		pass


class ImagesNextHandler (web.RequestHandler):
	def post(self):
		pass


class ImagesTagHandler (web.RequestHandler):
	def post(self):
		pass