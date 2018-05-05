from .pubsub import subscriptions
from ..database import database
from ..constants import groundstation_url
import json
import asyncio

class Parser:
    def __init__(self, client, message):
        self._client = client

        self.parse_websocket_message(client, message)

    def parse_websocket_message(self, client, message):
        try:
            payload = json.loads(message)
        except:
            payload = None

        if payload is None:
            return

        if 'subscribe' in payload:
            self.parse_subscription(client, payload['subscribe'])
        if 'type' in payload:
            if payload['type'] == 'request_image_catchup':
                last = payload['last'] if 'last' in payload else None
                asyncio.get_event_loop().create_task(self.parse_image_catchup(client, last))

    def parse_subscription(self, client, subscription):

        if isinstance(subscription, list):
            for _type in subscription:
                if isinstance(_type, str):
                    subscriptions.subscribe(client, _type)

        elif isinstance(subscription, str):
            subscriptions.subscribe(client, subscription)
        else:
            pass

    async def parse_image_catchup(self, client, last):
        
        try:
            images = await database.get_next_images(last)

            for image in images:

                img = {
                    'url': groundstation_url + "/" + image['file_location'],
                    '_id': str(image['_id']),
                    'timestamp': image['timestamp'],
                    'telemetry': None,
                    'tagged': image['tagged'],
                    'type': "image" # Tell webclient this is an image message
                }

                if 'telemetry' in image and image['telemetry'] is not None:
                    img['telemetry'] = {
                        **image['telemetry'],
                        '_id': str(image['telemetry']['_id'])
                    }

                client.write_message(json.dumps(img))
        except Exception as e:
            print(str(e))
        
        # Tell webclient load complete
        client.write_message(json.dumps({'type': "image_load_complete"}))
