from database import database
from motor import motor_asyncio
import asyncio

class TelemetryService:

    def __init__(self):
        # Should be a list of telemetry objects
        # Ex: [ { 'lat': 0', 'lon': 0, 'timestamp:' 0, '_id': 0 } ]
        self._telemetry = []

    # Search self._telemetry to find a GPS location nearest to the timestamp parameter
    def find_nearest_telemetry(self, timestamp):
        pass

    # Add a new timestamp -> GPS mapping
    # Persist telemetry to database
    # Telemetry -> object following above data structure
    def add_telemetry(self, telemetry):
        
        # Append
        self._telemetry.append(telemetry)
        # Then add it to database
        self.persist_single_to_database(telemetry)

    # Load all of the persisted telemetry data
    def load_from_database(self): #set to print right now
        loop = asyncio.get_event_loop()
        loop.run_until_complete(database.do_find())
        self._telemetry = self._telemetry + database.telemetry_array_from_db

        

    # Persist telemetry object to DB
    def persist_single_to_database(self, telemetry):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(database.insert_telemetry(test_telemetry))


#Database test 
test_telemetry = {
    'type': 'telemetry',
    'lat': 45.709,
    'lon': 101.1
}
telemetry = TelemetryService()
telemetry.persist_single_to_database(test_telemetry)
telemetry.load_from_database()
print ("Tesing if telemetry has obtained values from db")
print(telemetry._telemetry)

