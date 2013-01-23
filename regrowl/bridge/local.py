from __future__ import absolute_import

import Growl
import logging

from regrowl.regrowler import ReGrowler


logger = logging.getLogger(__name__)


__all__ = ['LocalNotifier']


class LocalNotifier(ReGrowler):
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
        logger.info('Sending notification to local machine')
        self.growler.notify(
            noteType=packet.headers['Notification-Name'],
            title=packet.headers['Notification-Title'],
            description=packet.headers['Notification-Name'],
            icon=self.icon
        )
