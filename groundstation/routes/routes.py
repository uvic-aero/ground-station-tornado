from .index import IndexHandler
from .by_coordinates import ImageByCoordinateHandler
import tornado.ioloop
import tornado.web
import asyncio
from .log_handler import LogHandler
from .images import ImagesHandler, ImagesByIdHandler
from .telemetry_handler import TelemetryHandler

routes = [
    (r"/", IndexHandler),
    (r"/images", ImagesHandler),
    (r"/images/by_coordinates", ImageByCoordinateHandler),
    (r"/logs", LogHandler),
    (r"/images/(.*)", ImagesByIdHandler),
    (r"/telemetry", TelemetryHandler)
]
