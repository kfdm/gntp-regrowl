"""
Echo a growl notification to the terminal

This is just a simple regrowler to show the basic structure and provide
a simple debug output

Config Example:
[regrowl.bridge.echo]
verbose = True
"""

from __future__ import absolute_import

import logging

from regrowl.regrowler import ReGrowler

logger = logging.getLogger(__name__)

__all__ = ['EchoNotifier']

SPACER = '=' * 80


class EchoNotifier(ReGrowler):
    valid = ['REGISTER', 'NOTIFY', 'SUBSCRIBE']

    def format(self, packet, headers):
        logger.info(packet.info['messagetype'])
        if self.getboolean('verbose', False):
            print SPACER
            print packet
            print SPACER
        else:
            print packet.info['messagetype']
            for header in headers:
                print header, ':', packet.headers[header]

    def register(self, packet):
        self.format(packet, ['Application-Name'])

    def notify(self, packet):
        self.format(packet, [
            'Application-Name',
            'Notification-Title',
            'Notification-Text'
        ])

    def subscribe(self, packet):
        self.format(packet, ['Subscriber-ID', 'Subscriber-Name'])
