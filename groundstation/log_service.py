class LogService():
    
    def handle_log(self, timestamp, system, message):
        print("TEST: time: " + str(timestamp) + " system: " + system + " message: " + message)
        # TODO: send to database

log_service = LogService()