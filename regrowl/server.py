#!/usr/bin/env python
#
# ReGrowl Server
# A simple ? server for *regrowling* GNTP messages to the local OSX Growl system

import SocketServer
import logging
import platform

import gntp
from gntp.errors import BaseError as GNTPError
from regrowl.bridge import load_bridges

__all__ = ['GNTPServer', 'GNTPHandler']

logger = logging.getLogger(__name__)

SPACER = 'x' * 80

TRACE = 1


def _trace(self, msg, *args, **kwargs):
    self.log(TRACE, msg, *args, **kwargs)

logging.addLevelName(TRACE, 'TRACE')
logging.Logger.trace = _trace


def add_origin_info(packet):
    packet.add_header('Origin-Machine-Name', platform.node())
    packet.add_header('Origin-Software-Name', 'ReGrowl Server')
    packet.add_header('Origin-Software-Version', '0.1')
    packet.add_header('Origin-Platform-Name', platform.system())
    packet.add_header('Origin-Platform-Version', platform.platform())


class GNTPHandler(SocketServer.StreamRequestHandler):
    def read(self):
        bufferLength = 2048
        buffer = ''
        while(1):
            data = self.request.recv(bufferLength)
            logger.debug('Reading %s Bytes', len(data))
            buffer = buffer + data
            if len(data) < bufferLength and buffer.endswith('\r\n\r\n'):
                break
        logger.trace('Incoming Request\n%s\n%s\n%s', SPACER, buffer, SPACER)
        return buffer

    def write(self, msg):
        logger.trace('Outgoing Response\n%s\n%s\n%s', SPACER, msg, SPACER)
        self.request.sendall(msg)

    def handle(self):
        self.hostaddr, self.port = self.request.getsockname()
        logger.info('Handling request from %s:%s', self.hostaddr, self.port)

        self.data = self.read()

        try:
            message = gntp.parse_gntp(self.data, self.server.options.password)

            response = gntp.GNTPOK(action=message.info['messagetype'])
            add_origin_info(response)

            if message.info['messagetype'] == 'NOTICE':
                response.add_header('Notification-ID', '')
            elif message.info['messagetype'] == 'SUBSCRIBE':
                response.add_header('Subscription-TTL', '10')

            self.write(response.encode())
        except GNTPError:
            logger.exception('GNTP Error')
            return
        except:
            logger.exception('Unknown Error')
            return

        if self.server.options.debug:
            logger.info('Reloading bridges')
            self.server.notifiers = load_bridges(self.server.config)

        for bridge in self.server.notifiers:
            bridge(message, self.hostaddr, self.port)


class GNTPServer(SocketServer.TCPServer):
    def __init__(self, options, config):
        try:
            SocketServer.TCPServer.__init__(self, (options.host, options.port), GNTPHandler)
        except:
            logger.critical('There is already a server running on port %d', options.port)
            exit(1)

        logger.info('Loading Server')
        self.config = config
        self.options = options
        self.notifiers = load_bridges(self.config)

    def run(self):
        logger.info('Starting Server')
        try:
            sa = self.socket.getsockname()
            logger.info('Listening for GNTP on %s port %s', sa[0], sa[1])
            self.serve_forever()
        except KeyboardInterrupt:
            self.__serving = False
