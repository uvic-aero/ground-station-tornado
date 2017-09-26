
# Basic concept of an image
# Can have image data received over the network or loaded from the filesystem,
# telemetry data that's been matched in, and the idea of a persistent file location
class Image:
    def __init__(self, uuid=None):

        self._uuid = uuid # Unique identifier used by database. If it does not exist, create it
        self.jpeg_data = None
        self.file_location = None
        self.timestamp = None
        self.telemetry = None

    # Use the filesystem location to open this image
    # File location must exist
    def load_jpeg_from_filesysem(self):
        pass

    # Save jpeg data in memory to the filesystem & record file location
    def save_jpeg_to_filesystem(self):
        pass

    # Use telemetry service to find telemetry for this image/timestamp
    # The timestamp in this image must exist and be valid
    def match_telemetry(self):
        pass

    # Use the unique image ID to retrieve all information in the DB for this image
    def load_from_database(self):
        pass

    # (over)write this image data to database
    def persist_to_database(self):
        pass