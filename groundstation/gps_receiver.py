from .udp_handler import UDPHandler
import json
from .telemetry_service import telemetry_service
import time

class GPSReceiver(UDPHandler):
    def __init__(self):
        self._port = 24001
        self._last_received_time = 0
        self._resolution = 200 # 5 times per second (1000ms / 5)

    # What to do when we receive GPS data
    async def data_received(self, data, addr):
        cur_time = time.time() * 1000

        if (cur_time > self._last_received_time):

            try:
                payload = json.loads(data)
                telemetry = payload['telemetry_data']

                converted = {
                    'lat': telemetry['lat'],
                    'lon': telemetry['long'],
                    'alt': telemetry['alt_rel'],
                    'timestamp': cur_time
                }

                telemetry_service.add_telemetry(converted)
            except e:
                print(e)
                pass

            self._last_received_time = cur_time + self._resolution
