from tornado import web
import json
from ..log_service import log_service

class LogHandler(web.RequestHandler):

    def post(self):
        log_dict = json.loads(self.request.body, encoding = object)
        log_service.handle_log(log_dict)