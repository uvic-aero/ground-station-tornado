from .websocket import pubsub
from tornado import ioloop
from uuid import uuid4
import socket
import json
import random
import requests
import base64
import time
import asyncio
import functools

test_images = [{
    'url': 'http://stories.barkpost.com/wp-content/uploads/2015/04/husky.jpg'
}, {
    'url': 'https://www.pets4homes.co.uk/images/breeds/43/large/81f6538eb4101d364ac0588b10040f0e.jpg'
}, {
    'url': 'http://static.boredpanda.com/blog/wp-content/uploads/2015/08/siberian-husky-dog-instagram-erica-tcogoeva-20.jpg'
}, {
    'url': 'https://pbs.twimg.com/media/CUb38ljVAAENDyE.jpg:large'
}, {
    'url': 'http://i.dailymail.co.uk/i/pix/2014/01/10/article-2537126-1A8B1A2E00000578-874_634x453.jpg'
}]


test_telemetry = {}

class Simulator:
    def __init__(self):
        pass

    def start(self):
        
        ioloop.PeriodicCallback(self.send_images_internal, 3000).start()
        ioloop.PeriodicCallback(self.send_images_webclient, 1000).start()
        ioloop.PeriodicCallback(self.send_telemetry_webclient, 500).start()
        ioloop.PeriodicCallback(self.send_telemetry_internal, 1000).start()

    def send_images_internal(self):
  
        img = test_images[random.randint(0, len(test_images)-1)]
        img_data = requests.get(img['url']).content

        img_payload = {
            'image': base64.b64encode(img_data).decode('utf-8', "ignore"),
            'timestamp': time.time() * 1000
        }

        # Send UDP data to GPS receiver server
        loop = asyncio.get_event_loop()

        loop.run_in_executor(None, functools.partial(requests.post,
            'http://localhost:24002/images',
            timeout=3, json=img_payload))

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

                test_telemetry = {
                    'telemetry_data': {
                        'lat': random.uniform(46.7,45.8),
                        'long': random.uniform(104.3, 104.4),
                        'alt_rel': 25,
                        'timestamp': 0
                    }
                }
                sub.write_message(json.dumps(test_telemetry))

    # Generate telemetry data with random lat and long coordinates
    def send_telemetry_internal(self):
        # Send UDP data to GPS receiver server
        test_telemetry = {
            'telemetry_data': {
                'lat': random.uniform(46.7,45.8),
                'long': random.uniform(104.3, 104.4),
                'alt_rel': 25,
                'timestamp': 0
            }
        }
        print('Inserting random telemetry point: ' + str(test_telemetry))
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(json.dumps(test_telemetry).encode(), ("127.0.0.1", 24001))
