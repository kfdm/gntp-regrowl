"""
Forward notification

This is a simple forwarder bridge

Config Example:
[regrowl.bridge.forward]
label = host,password
other = host:port,password
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

    def forward(self, packet):
        messagetype = packet.info['messagetype']
        for label, settings in self.config.items(__name__):
            dest, password = settings.split(',')
            try:
                host, port = dest.split(':')
            except ValueError:
                host, port = dest, DEFAULTS['port']

            passwordHash = self.get('passwordHash', DEFAULTS['passwordHash'])

            packet.set_password(password, passwordHash)

            logger.info('Forwarding %s to %s:%s', messagetype, host, port)

            GrowlNotifier(
                hostname=host,
                port=port,
            )._send(messagetype, packet)

    def register(self, packet):
        self.forward(packet)

    def notify(self, packet):
        self.forward(packet)
