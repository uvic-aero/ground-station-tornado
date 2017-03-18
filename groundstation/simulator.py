from .websocket import pubsub
from tornado import ioloop
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
                sub.write_message(json.dumps(test_images[random.randint(0, len(test_images)-1)]))

    def send_telemetry(self):

        subscribers = pubsub.subscriptions.get_subscribers()

        for type in subscribers:
            if type != 'telemetry':
                continue
            for sub in subscribers[type]:
                sub.write_message(json.dumps(test_telemetry))