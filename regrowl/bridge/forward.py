"""
Forward notification

This is a simple forwarder bridge

Config Example:
[regrowl.bridge.forward]
host = 127.0.0.1
pass = p@ssword
"""

from __future__ import absolute_import

import logging

from gntp.notifier import GrowlNotifier
from regrowl.regrowler import ReGrowler
from regrowl.config import DEFAULTS

logger = logging.getLogger(__name__)

# Ignore debug logging from lower level growl library
logging.getLogger('gntp.notifier').setLevel(logging.INFO)

__all__ = ['ForwardNotifier']


class ForwardNotifier(ReGrowler):
    valid = ['REGISTER', 'NOTIFY']

    def forward(self, messagetype, packet):
        self.password = self.get('pass')
        self.passwordHash = self.get('passwordHash', DEFAULTS['passwordHash'])
        self.host = self.get('host')
        self.port = self.getint('port', DEFAULTS['port'])

        packet.set_password(self.password, self.passwordHash)

        logger.info('Forwarding %s to %s:%s', messagetype, self.host, self.port)

        self.growler = GrowlNotifier(
            hostname=self.host,
            port=self.port,
        )._send(messagetype, packet)

    def register(self, packet):
        self.forward('REGISTER', packet)

    def notify(self, packet):
        self.forward('NOTIFY', packet)
