import requests 
import json
import base64
from ..image_service import image_service
from tornado import web 
from ..database import database
import asyncio

class MarkerHandler(web.RequestHandler):
    
    @web.asynchronous
    def get(self):
        asyncio.get_event_loop().create_task(database.do_find_markers(self.markers_received))

    def markers_received(self, markers):
        self.write ({'markers': markers})
        self.finish()
