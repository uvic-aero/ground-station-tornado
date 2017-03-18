from .websocket import pubsub
from tornado import ioloop
import json

test_image = {
    'type': 'image',
    'width': 671,
    'height': 475,
    'url': 'http://stories.barkpost.com/wp-content/uploads/2015/04/husky.jpg'
}

test_telemetry = {
    'type': 'telemetry',
    'lat': 45.709,
    'lon': 104.3467
}

class Simulator:
    def __init__(self):
        pass

    def start(self):
        
        ioloop.PeriodicCallback(self.send_images, 1000).start()
        ioloop.PeriodicCallback(self.send_telemetry, 500).start()

    def send_images(self):

        subscribers = pubsub.subscriptions.get_subscribers()

        for type in subscribers:
            if type != 'images':
                continue
            for sub in subscribers[type]:
                print("Sending images")
                sub.write_message(json.dumps(test_image))

    def send_telemetry(self):

        subscribers = pubsub.subscriptions.get_subscribers()

        for type in subscribers:
            if type != 'telemetry':
                continue
            for sub in subscribers[type]:
                sub.write_message(json.dumps(test_telemetry))