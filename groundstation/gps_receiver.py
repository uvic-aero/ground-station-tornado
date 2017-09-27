from .udp_handler import UDPHandler

class GPSReceiver(UDPHandler):
    def __init__(self):
        self._port = 24001
        self._receive_func = self.handle_gps

    # What to do when we receive GPS data
    def handle_gps(self, data, address):
       
        # Call telemetry service

        pass