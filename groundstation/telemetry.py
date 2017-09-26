from .database import database

class TelemetryService:

    def __init__(self):
        # Should be a list of objects that map timestamp -> GPS
        self._telemetry = []

    # Search the telemetry list to find a GPS location nearest to the timestamp parameter
    def find_nearest_telemetry(self, timestamp):
        pass

    # Add a new timestamp -> GPS mapping
    # Persist telemetry to database
    def add_telemetry(self, timestamp, location):
        pass

    # Load all of the persisted telemetry data
    def load_from_database(self):
        pass

    # Persist all in-memory telemetry to DB
    def persist_to_database(self):
        pass
