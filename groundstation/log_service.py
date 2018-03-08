import asyncio
from .database import database 

class LogService():
    
    def handle_log(self, document):
        #print("TEST: time: " + document['timestamp'] + " system: " + document['system'] + " message: " + document['message'])
        # TODO: send to database
        loop = asyncio.get_event_loop()
        loop.create_task(database.insert_log(document))


log_service = LogService()