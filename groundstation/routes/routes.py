from .index import IndexHandler
from .by_coordinates import ImageByCoordinateHandler
import tornado.ioloop
import tornado.web
import asyncio

routes = [
    (r"/", IndexHandler),
    (r"/images/by_coordinates", ImageByCoordinateHandler)
]
