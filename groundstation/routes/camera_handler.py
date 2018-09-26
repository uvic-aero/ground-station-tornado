from tornado import web
import requests
import json
import traceback
from ..constants import camera_url

class ZoomInHandler(web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    def get(self):
      try:
        res = requests.get(camera_url + "/zoom/in")
        print(res.status_code)
        self.set_status(res.status_code)
        self.write({'result': 'zoomed in'})
      except Exception as e:
        print(str(e))
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

        self.set_status(res.status_code)
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

        self.set_status(res.status_code)
        self.write({'result': 'captured still'})
      except:
        self.write({'error': 'camera not ready'})

    def options(self):
        self.set_status(204)
        self.finish()

class ModeHandler(web.RequestHandler):
  
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    def get(self):
      try:
        res = requests.get(camera_url + "/mode", timeout=2)

        self.set_status(res.status_code)
        self.write(res.json())
      except Exception as e:
        print(str(e))
        self.write({'error': 'camera not ready'})

    def post(self):
      print('post')
      try:
        res = requests.post(camera_url + "/mode", json=json.loads(self.request.body), timeout=2)
        print(res)
        self.set_status(res.status_code)
        self.write({'result': 'changed mode'})
      except Exception as e:
        print(e)
        traceback.print_exc()
        self.write({'error': 'camera not ready'})

    def options(self):
        self.set_status(204)
        self.finish()

class StatusHandler(web.RequestHandler):
  
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    def get(self):
      try:
        res = requests.get(camera_url + "/status")

        self.set_status(res.status_code)
        self.write(res.json())
      except:
        self.write({'error': 'camera not ready'})

    def options(self):
        self.set_status(204)
        self.finish()