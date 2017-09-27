from .udp_handler import UDPHandler

class ImageReceiver(UDPHandler):

    def __init__(self):
        self._port = 24003
        self._receive_func = self.handle_image

    # Parse incoming images and determine what to do with them
    def handle_image(self, data, address):
        pass