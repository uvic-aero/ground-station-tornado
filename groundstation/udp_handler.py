import socket
import os
import errno
from tornado.ioloop import IOLoop
from tornado.platform.auto import set_close_exec


class UDPHandler:
    def __init__(self):
        self._socket = None
        self._started = False

    def _bind_socket(self):
        for res in set(socket.getaddrinfo(None, self._port, socket.AF_UNSPEC, socket.SOCK_DGRAM,
                                          0, socket.AI_PASSIVE)):

            af, socktype, proto, canonname, sockaddr = res

            if sockaddr[0] == '0.0.0.0':

                self._socket = socket.socket(af, socktype, proto)
                set_close_exec(self._socket.fileno())

                if os.name != 'nt':
                    self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                self._socket.setblocking(0)
                self._socket.bind(sockaddr)
                break

    def _add_handler(self):

        def handler(fd, events):

            while True:
                try:
                    data, address = self._socket.recvfrom(2500)
                except socket.error as e:
                    if e.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN):
                        return
                    raise
                self._handle_receive(data, address)

        IOLoop.instance().add_handler(self._socket.fileno(), handler, IOLoop.READ)

    def _handle_receive(self, data, address):
        pass

    def start(self, port):

        self._port = port

        self._bind_socket()

        if self._socket is None:
            print("Failed to start UDP server and bind socket")
            os._exit(1)

        print("UDP server listening on port %s" % port)