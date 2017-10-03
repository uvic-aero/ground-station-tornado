from .udp_handler import UDPHandler

class GPSReceiver(UDPHandler):
    def __init__(self):
        self._port = 24001

    # What to do when we receive GPS data
    async def data_received(self, data, addr):
 
         # Call telemetry service

        pass