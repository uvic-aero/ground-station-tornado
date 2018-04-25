from .index import IndexHandler
from .by_coordinates import ImageByCoordinateHandler
import tornado.ioloop
import tornado.web
import asyncio
from .log_handler import LogHandler
from .images import ImagesHandler, ImagesByIdHandler
from .telemetry_handler import TelemetryHandler
from .camera_handler import ZoomInHandler, ZoomOutHandler, CaptureStillHandler, ModeHandler, StatusHandler

routes = [
    (r"/", IndexHandler),
    (r"/images", ImagesHandler),
    (r"/images/by_coordinates", ImageByCoordinateHandler),
    (r"/logs", LogHandler),
    (r"/images/(.*)", ImagesByIdHandler),
    (r"/telemetry", TelemetryHandler),
    (r"/camera/zoomin", ZoomInHandler),
    (r"/camera/zoomout", ZoomOutHandler),
    (r"/camera/still", CaptureStillHandler),
    (r"/camera/mode", ModeHandler),
    (r"/camera/status", StatusHandler)
]
