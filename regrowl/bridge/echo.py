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
    valid = ['REGISTER', 'NOTIFY']

    def instance(self, packet):
        return None

    def register(self, packet):
        logger.info('Register')
        print 'Registration Packet:'
        if self.getboolean('verbose', False):
            print SPACER
            print packet
            print SPACER
        else:
            print packet.headers['Application-Name']

    def notify(self, packet):
        logger.info('Notify')
        print 'Notification Packet:'
        if self.getboolean('verbose', False):
            print SPACER
            print packet
            print SPACER
        else:
            print packet.headers['Notification-Title'],
            print packet.headers['Notification-Text']
