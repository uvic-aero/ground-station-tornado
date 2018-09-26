from tornado import web
import tornado
from ..database import database
from motor import motor_asyncio
import motor
import asyncio
import json
import array
from bson.json_util import loads

class TelemetryHandler(web.RequestHandler):
    @web.asynchronous
    def get(self):

        loop = asyncio.get_event_loop()
        loop.create_task(database.get_latest_telemetry_callback(self._telemetry_received))
    def _telemetry_received(self, telemetry):
        if telemetry is None:
          self.write({})
        else:
          self.write(telemetry)
        self.finish()