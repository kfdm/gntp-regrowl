from __future__ import absolute_import

import logging

from regrowl.regrowler import ReGrowler


logger = logging.getLogger(__name__)


__all__ = ['EchoNotifier']


class EchoNotifier(ReGrowler):
    valid = ['REGISTER', 'NOTIFY']

    def instance(self, packet):
        return None

    def register(self, packet):
        logger.info('Register')
        print packet

    def notify(self, packet):
        logger.info('Notify')
        print packet
