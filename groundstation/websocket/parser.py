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
                asyncio.get_event_loop().create_task(self.parse_image_catchup(client))

    def parse_subscription(self, client, subscription):

        if isinstance(subscription, list):
            for _type in subscription:
                if isinstance(_type, str):
                    subscriptions.subscribe(client, _type)

        elif isinstance(subscription, str):
            subscriptions.subscribe(client, subscription)
        else:
            pass

    async def parse_image_catchup(self, client):
        
        images = await database.get_next_images()

        for image in images:

            img = {
                'url': groundstation_url + "/" + image['file_location'],
                '_id': str(image['_id']),
                'timestamp': image['timestamp'],
                'telemetry': {
                    **image['telemetry'],
                    '_id': str(image['telemetry']['_id'])
                },
                'type': "image" # Tell webclient this is an image message
            }

            client.write_message(json.dumps(img))
