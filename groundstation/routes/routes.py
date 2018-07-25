from .index import IndexHandler
from .by_coordinates import ImageByCoordinateHandler
import tornado.ioloop
import tornado.web
import asyncio
from .log_handler import LogHandler
from .images import ImagesHandler, ImagesByIdHandler, ImagesByIdJpgHandler, ImagesTagHandler, ImagesUntagHandler
from .telemetry_handler import TelemetryHandler
from .camera_handler import ZoomInHandler, ZoomOutHandler, CaptureStillHandler, ModeHandler, StatusHandler
from .markers import MarkerHandler

routes = [
    (r"/", IndexHandler),
    (r"/images", ImagesHandler),
    (r"/images/by_coordinates", ImageByCoordinateHandler),
    (r"/logs", LogHandler),
    (r"/images/(.*)\.jpg", ImagesByIdJpgHandler), # For returning actual image data as binary jpg
    (r"/images/(.*)/tag", ImagesTagHandler),
    (r"/images/(.*)/untag", ImagesUntagHandler),
    (r"/images/(.*)", ImagesByIdHandler),
    (r"/telemetry", TelemetryHandler),
    (r"/camera/zoomin", ZoomInHandler),
    (r"/camera/zoomout", ZoomOutHandler),
    (r"/camera/still", CaptureStillHandler),
    (r"/camera/mode", ModeHandler),
    (r"/camera/status", StatusHandler),
    (r"/markers", MarkerHandler)
]
