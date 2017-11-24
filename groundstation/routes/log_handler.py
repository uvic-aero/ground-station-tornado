from tornado import web

class LogHandler(web.RequestHandler):

    def post(self):
        print(self.request.body)