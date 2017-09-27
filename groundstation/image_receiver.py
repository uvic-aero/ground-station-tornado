from .udp_handler import UDPHandler
from .image_service import image_service

class ImageReceiver(UDPHandler):

    def __init__(self):
        self._port = 24003
        self._receive_func = self.handle_image

    # Parse incoming images and determine what to do with them
    def handle_image(self, data, address):
        
        # After parsing image, send it to the image service
        #image_service.add_new_image()

        pass