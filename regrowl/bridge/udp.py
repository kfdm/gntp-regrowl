"""
Simple Growl UDP Bridge

Converts a TCP GNTP notification to the old UDP Growl format
"""

from __future__ import absolute_import

import logging
from socket import AF_INET, SOCK_DGRAM, socket

from regrowl.regrowler import ReGrowler
import regrowl.extras.netgrowl as netgrowl


logger = logging.getLogger(__name__)


__all__ = ['UDPNotifier']


class UDPNotifier(ReGrowler):
    key = __name__
    valid = ['REGISTER', 'NOTIFY']

    def _send(self, payload):
        addr = ("localhost", netgrowl.GROWL_UDP_PORT)
        s = socket(AF_INET, SOCK_DGRAM)
        s.sendto(payload, addr)

    def instance(self, packet):
        return None

    def register(self, packet):
        p = netgrowl.GrowlRegistrationPacket(
            application=packet.headers.get('Application-Name')
            )

        for notification in packet.notifications:
            p.addNotification(notification.get('Notification-Name'))

        logger.info('Sending UDP register')
        self._send(p.payload())

    def notify(self, packet):
        p = netgrowl.GrowlNotificationPacket(
            application=packet.headers.get('Application-Name'),
            notification=packet.headers.get('Notification-Name'),
            title=packet.headers['Notification-Title'],
            description=packet.headers['Notification-Name'],
            )

        logger.info('Sending UDP notification')
        self._send(p.payload())
