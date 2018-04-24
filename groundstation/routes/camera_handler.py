from tornado import web
import requests

camera_url = "http://localhost:8000"

class ZoomInHandler(web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    def get(self):
      try:
        res = requests.get(camera_url + "/zoom/in")

        self.put_status(res.status_code)
        self.write({'result': 'zoomed in'})
      except:
        self.write({'error': 'camera not ready'})

    def options(self):
        self.set_status(204)
        self.finish()

class ZoomOutHandler(web.RequestHandler):
  
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    def get(self):
      try:
        res = requests.get(camera_url + "/zoom/out")

        self.put_status(res.status_code)
        self.write({'result': 'zoomed out'})
      except:
        self.write({'error': 'camera not ready'})

    def options(self):
        self.set_status(204)
        self.finish()

class CaptureStillHandler(web.RequestHandler):
  
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    def get(self):
      try:
        res = requests.get(camera_url + "/still")

        self.put_status(res.status_code)
        self.write({'result': 'captured still'})
      except:
        self.write({'error': 'camera not ready'})

    def options(self):
        self.set_status(204)
        self.finish()
