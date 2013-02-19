"""
Echo a growl notification to the terminal

This is just a simple regrowler to show the basic structure and provide
a simple debug output
"""

from __future__ import absolute_import

import logging

from regrowl.regrowler import ReGrowler

logger = logging.getLogger(__name__)

__all__ = ['EchoNotifier']

SPACER = '=' * 80


class EchoNotifier(ReGrowler):
    key = __name__
    valid = ['REGISTER', 'NOTIFY']

    def instance(self, packet):
        return None

    def register(self, packet):
        logger.info('Register')
        print 'Registration Packet:'
        print SPACER
        print packet
        print SPACER

    def notify(self, packet):
        logger.info('Notify')
        print 'Notification Packet:'
        print SPACER
        print packet
        print SPACER
