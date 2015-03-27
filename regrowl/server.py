#!/usr/bin/env python
#
# ReGrowl Server
# A simple ? server for *regrowling* GNTP messages to the local OSX Growl system

import SocketServer
import logging
import platform
import threading

from gntp.core import parse_gntp, GNTPOK
from gntp.errors import BaseError as GNTPError
from regrowl.bridge import load_bridges
from regrowl.config import DEFAULTS

__all__ = ['GNTPServer', 'GNTPHandler']

SPACER = 'x' * 80

TRACE = 1


class RegrowlLogger(logging.Logger):
    def trace(self, msg, *args, **kwargs):
        if self.isEnabledFor(TRACE):
            self._log(TRACE, msg, args, **kwargs)

logging.addLevelName(TRACE, 'TRACE')
logging.setLoggerClass(RegrowlLogger)
logger = logging.getLogger(__name__)


def add_origin_info(packet):
    packet.add_header('Origin-Machine-Name', platform.node())
    packet.add_header('Origin-Software-Name', 'ReGrowl Server')
    packet.add_header('Origin-Software-Version', '0.1')
    packet.add_header('Origin-Platform-Name', platform.system())
    packet.add_header('Origin-Platform-Version', platform.platform())


class GNTPHandler(SocketServer.StreamRequestHandler):
    def read(self):
        bufferLength = self.get('bufferLength', DEFAULTS['bufferLength'])
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
            message = parse_gntp(self.data, self.server.options.password)

            response = GNTPOK(action=message.info['messagetype'])
            add_origin_info(response)

            if message.info['messagetype'] == 'NOTIFY':
                response.add_header('Notification-ID', '')
            elif message.info['messagetype'] == 'SUBSCRIBE':
                response.add_header(
                    'Subscription-TTL',
                    self.getint('timeout', DEFAULTS['timeout'])
                )

            self.write(response.encode())
        except GNTPError:
            logger.exception('GNTP Error')
            return
        except:
            logger.exception('Unknown Error')
            return

        if self.server.options.reload:
            logger.info('Reloading config')
            self.server.config = self.server.config.reload(
                [self.server.options.config]
            )

            logger.info('Reloading bridges')
            self.server.notifiers = load_bridges(self.server.config)

        for bridge in self.server.notifiers:
            try:
                threading.Thread(
                    target=bridge,
                    args=(self.server.config, message, self.hostaddr, self.port)
                ).start()
            except:
                logger.exception('Error calling %s', bridge)

    def get(self, key, default=None):
        return self.server.config.get(__name__, key, default)

    def getint(self, key, default=None):
        return self.server.config.getint(__name__, key, default)

    def getboolean(self, key, default=None):
        return self.server.config.getboolean(__name__, key, default)


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
