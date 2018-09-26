from .parser import Parser
from .pubsub import subscriptions
from tornado import websocket
from uuid import uuid4

class WebSocketHandler(websocket.WebSocketHandler):

    def __init__(self, application, request, **kwargs):
        super(WebSocketHandler, self).__init__(application, request, **kwargs)
        self._identifier = uuid4()

    def open(self):
        print("New client connected")

    def on_message(self, message):
        Parser(self, message)

    def on_close(self):
        subscriptions.unsubscribe(self)

    def get_identity(self):
        return self._identifier

    def check_origin(self, origin):
        return True

