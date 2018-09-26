from .handler import WebSocketHandler
from tornado import web


class WebSocket:
    def __init__(self):
        self._application = web.Application([
            (r"/", WebSocketHandler),
        ])

    def start(self, port):
        self._port = port

        self._application.listen(self._port)

        print("WebSocket server listening on port %s" % self._port)