import socket
import os
import errno
from tornado import ioloop

class UDPHandler:
    def __init__(self):
        self._started = False
        self._port = None # Port this handler listens on
        self._transport = None
        self._protocol = None

    class ProtocolFactory:

        def __init__(self, receive_func):
            self.receive_func = receive_func

        def connection_made(self, transport):
            self.transport = transport

        def datagram_received(self, data, addr):
            loop = ioloop.IOLoop.current(instance=True).asyncio_loop
            loop.create_task(self.receive_func(data, addr))

    def start(self):

        if self._port == None:
            print("UDP Handler has no port defined")
            os._exit(1)

        loop = ioloop.IOLoop.current(instance=True).asyncio_loop

        listener = loop.create_datagram_endpoint(
            lambda: self.ProtocolFactory(self.data_received), local_addr=('127.0.0.1', self._port))

        self._transport, self._protocol = loop.run_until_complete(listener)

        print("UDP server listening on port %s" % self._port)

    def stop(self):
        self._transport.close()

    # Dummy receiver func that can be overridden
    async def data_received(self, data, addr):
        pass