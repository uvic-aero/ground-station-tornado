from .websocket import websocket
from .udp_handler import UDPHandler
from .api import API

from tornado import ioloop
import signal


class GroundStation:

    def __init__(self):
        self._websocket = websocket.WebSocket()
        self._udp_handler = UDPHandler()
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

        self._websocket.start(24000)
        self._udp_handler.start(24001)
        self._api.start(24002)

        # Handle interruption events
        signal.signal(signal.SIGINT, self.signal_handler)

        # Force IOLoop to wake up so interrupts can be handled
        ioloop.PeriodicCallback(self.check_should_exit, 100).start()

        ioloop.IOLoop.instance().start()

        print("Stopping ground station")