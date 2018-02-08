from .udp_handler import UDPHandler
import json
from .telemetry_service import telemetry_service

class GPSReceiver(UDPHandler):
    def __init__(self):
        self._port = 24001

    # What to do when we receive GPS data
    async def data_received(self, data, addr):
        telemetry = json.loads(data)
         # Call telemetry service
        telemetry_service.add_telemetry(telemetry)
