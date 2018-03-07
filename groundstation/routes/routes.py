from .index import IndexHandler
from .by_coordinates import ImageByCoordinateHandler
import tornado.ioloop
import tornado.web
import asyncio
from .log_handler import LogHandler

routes = [
    (r"/", IndexHandler),
    (r"/images/by_coordinates", ImageByCoordinateHandler),
    (r"/logs", LogHandler)
]
