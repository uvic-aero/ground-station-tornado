from .database import database
from motor import motor_asyncio
import asyncio

class TelemetryService:

    def __init__(self):
        # Should be a list of telemetry objects
        # Ex: [ { 'lat': 0', 'lon': 0, 'alt', 'timestamp:' 0, '_id': 0 } ]
        self.loop = asyncio.get_event_loop()

    def find_nearest_telemetry(self, timestamp):
        pass

    # Add a new timestamp -> GPS mapping
    # Persist telemetry to database
    # Telemetry -> object following above data structure
    def add_telemetry(self, telemetry):

        self.persist_single_to_database(telemetry)

    # Persist telemetry object to DB
    def persist_single_to_database(self, telemetry):
        loop = asyncio.get_event_loop()
        loop.create_task(database.insert_telemetry(telemetry))

telemetry_service = TelemetryService()
