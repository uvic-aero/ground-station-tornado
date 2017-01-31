from .routes import routes
from tornado import httpserver
from tornado import web

class API:
    def __init__(self):
        self._application = web.Application(routes.routes)
        self._server = httpserver.HTTPServer(self._application)

    def start(self, port):
        self._server.listen(port)

        print("API server is listening on port %s" % port)
