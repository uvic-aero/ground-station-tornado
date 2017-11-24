from .index import IndexHandler
from .log_handler import LogHandler

routes = [
    (r"/", IndexHandler),
    (r"/logs", LogHandler)
]