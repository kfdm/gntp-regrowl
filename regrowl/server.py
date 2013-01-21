#!/usr/bin/env python
#
# ReGrowl Server
# A simple ? server for *regrowling* GNTP messages to the local OSX Growl system

import SocketServer
import logging

import regrowl.bridge.gntp as gntp


__all__ = ['GNTPServer', 'GNTPHandler']

logger = logging.getLogger('Server')


class GNTPServer(SocketServer.TCPServer):
    def __init__(self, options, RequestHandlerClass):
        try:
            SocketServer.TCPServer.__init__(self, (options.host, options.port), RequestHandlerClass)
        except:
            logger.critical('There is already a server running on port %d', options.port)
            exit(1)
        self.options = options
        logging.getLogger('Server').info('Activating server')

    def run(self):
        try:
            sa = self.socket.getsockname()
            logger.info('Listening for GNTP on %s port %s', sa[0], sa[1])
            self.serve_forever()
        except KeyboardInterrupt:
            self.__serving = False


class GNTPHandler(SocketServer.StreamRequestHandler):
    def read(self):
        bufferLength = 2048
        buffer = ''
        while(1):
            data = self.request.recv(bufferLength)
            logging.getLogger('Server').debug('Reading %s Bytes', len(data))
            buffer = buffer + data
            if len(data) < bufferLength and buffer.endswith('\r\n\r\n'):
                break
        logging.getLogger('Server').debug(buffer)
        return buffer

    def write(self, msg):
        logging.getLogger('Server').debug(msg)
        self.request.sendall(msg)

    def handle(self):
        logger = logging.getLogger('Server')
        reload(gntp)
        self.data = self.read()

        try:
            message = gntp.parse_gntp(self.data, self.server.options.password)

            response = gntp.GNTPOK(action=message.info['messagetype'])
            if message.info['messagetype'] == 'NOTICE':
                response.add_header('Notification-ID', '')
            elif message.info['messagetype'] == 'SUBSCRIBE':
                raise gntp.UnsupportedError()
                #response.add_header('Subscription-TTL','10')
            self.write(response.encode())
        except gntp.BaseError, e:
            logger.exception('GNTP Error')
            if e.gntp_error:
                self.write(e.gntp_error())
        except:
            logger.exception('Unknown Error')
            error = gntp.GNTPError(errorcode=500, errordesc='Unknown server error')
            self.write(error.encode())
            raise

        message.send()
