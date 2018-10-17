import requests 
import json
import base64
from ..image_service import image_service
from tornado import web 
from ..database import database
import asyncio

class MarkerHandler(web.RequestHandler):
    
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    @web.asynchronous
    def get(self):
        #Asyncronously call 'find_markers() from database'
        #Note: pass in markers received to the find_markers function
        loop = asyncio.get_event_loop()
        loop.create_task(database.find_all_markers(self.markers_received))
        pass
        
    def markers_received(self, markers):
        self.write ({'markers': markers})
        self.finish()
    
    def options(self):
        self.set_status(204)
        self.finish()
