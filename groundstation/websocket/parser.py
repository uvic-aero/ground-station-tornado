from .pubsub import subscriptions
import json

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

    def parse_subscription(self, client, subscription):

        if isinstance(subscription, list):
            for _type in subscription:
                if isinstance(_type, str):
                    subscriptions.subscribe(client, _type)

        elif isinstance(subscription, str):
            subscriptions.subscribe(client, subscription)
        else:
            pass