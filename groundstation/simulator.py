from .websocket import pubsub
from tornado import ioloop
from uuid import uuid4
import socket
import json
import random

test_images = [{
    'type': 'image',
    'width': 671,
    'height': 475,
    'url': 'http://stories.barkpost.com/wp-content/uploads/2015/04/husky.jpg'
}, {
    'type': 'image',
    'width': 1280,
    'height': 854,
    'url': 'https://www.pets4homes.co.uk/images/breeds/43/large/81f6538eb4101d364ac0588b10040f0e.jpg'
}, {
    'type': 'image',
    'width': 880,
    'height': 564,
    'url': 'http://static.boredpanda.com/blog/wp-content/uploads/2015/08/siberian-husky-dog-instagram-erica-tcogoeva-20.jpg'
}, {
    'type': 'image',
    'width': 960,
    'height': 648,
    'url': 'https://pbs.twimg.com/media/CUb38ljVAAENDyE.jpg:large'
}, {
    'type': 'image',
    'width': 620,
    'height': 443,
    'url': 'http://i.dailymail.co.uk/i/pix/2014/01/10/article-2537126-1A8B1A2E00000578-874_634x453.jpg'
}]

test_telemetry = {
    
    'lat': 45.709,
    'lon': 104.3467,
    'timestamp': 0
}

class Simulator:
    def __init__(self):
        pass

    def start(self):
        
        ioloop.PeriodicCallback(self.send_images_webclient, 1000).start()
        ioloop.PeriodicCallback(self.send_telemetry_webclient, 500).start()
        ioloop.PeriodicCallback(self.send_telemetry_internal, 1000).start()

    def send_images_webclient(self):

        subscribers = pubsub.subscriptions.get_subscribers()

        for type in subscribers:
            if type != 'images':
                continue
            for sub in subscribers[type]:
                print("Sending images")

                # Select a random image
                img = test_images[random.randint(0, len(test_images)-1)]

                # Give each image a unique ID to be more realistic
                img['_id'] = str(uuid4())

                sub.write_message(json.dumps(img))

    def send_telemetry_webclient(self):

        subscribers = pubsub.subscriptions.get_subscribers()

        for type in subscribers:
            if type != 'telemetry':
                continue
            for sub in subscribers[type]:
                sub.write_message(json.dumps(test_telemetry))

    def send_telemetry_internal(self):

        # Send UDP data to GPS receiver server
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(json.dumps(test_telemetry).encode(), ("127.0.0.1", 24001))
