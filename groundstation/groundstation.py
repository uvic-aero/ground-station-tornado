
from tornado import ioloop

# Preconfigure global asyncio loop
ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')

# Import groundstation services
from .websocket import websocket
from .gps_receiver import GPSReceiver
from .image_receiver import ImageReceiver
from .api import API
from .simulator import Simulator

import sys
import signal

class GroundStation:

    def __init__(self):
        self._websocket = websocket.WebSocket()
        self._gps_receiver = GPSReceiver()
        self._image_receiver = ImageReceiver()
        self._api = API()

    @staticmethod
    def signal_handler(*args):

        # A SIGINT is a request for the application to stop; kill the event loop
        ioloop.IOLoop.instance().add_callback_from_signal(ioloop.IOLoop.instance().stop)

    # An empty function is enough to wake up event loop so interrupts can be handled
    def check_should_exit(self):
        pass

    def start(self):

        print("Starting ground station")
        
        self._gps_receiver.start()
        self._websocket.start(24000)
        self._api.start(24002)
        self._image_receiver.start()

        # Handle interruption events
        signal.signal(signal.SIGINT, self.signal_handler)

        # Force IOLoop to wake up so interrupts can be handled
        ioloop.PeriodicCallback(self.check_should_exit, 100).start()

        if 'simulate' in sys.argv:
            Simulator().start()

        ioloop.IOLoop.instance().start()

        print("Stopping ground station")
