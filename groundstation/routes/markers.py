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
        #Asyncronously call 'find_markers() from database'
        #Note: pass in markers received to the find_markers function
        pass
        
    def markers_received(self, markers):
        self.write ({'markers': markers})
        self.finish()
