"""
Send notification with legacy growl library

Uses the legacy growl bindings to send a growl notification.
Useful for older versions of OSX
"""

from __future__ import absolute_import

import Growl
import logging

from regrowl.regrowler import ReGrowler


logger = logging.getLogger(__name__)


__all__ = ['LocalNotifier']


class LocalNotifier(ReGrowler):
    key = __name__
    valid = ['REGISTER', 'NOTIFY']

    def instance(self, packet):
        return Growl.GrowlNotifier(
            applicationName=self.applicationName,
            notifications=self.notifications,
            defaultNotifications=self.notifications
        )

    def register(self, packet):
        logger.info('Sending register to local machine')
        self.growler.register()

    def notify(self, packet):
        if packet.headers.get('Notification-Icon'):
            resource = packet.headers['Notification-Icon']
            icon = self.get_resource(packet, resource)
        else:
            icon = None

        logger.info('Sending notification to local machine')
        self.growler.notify(
            noteType=packet.headers['Notification-Name'],
            title=packet.headers['Notification-Title'],
            description=packet.headers['Notification-Name'],
            icon=icon
        )
