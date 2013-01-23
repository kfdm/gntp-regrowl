from __future__ import absolute_import

import urllib2
import Growl
import logging


logger = logging.getLogger(__name__)


__all__ = ['LocalNotifier']


class LocalNotifier(object):
    def __init__(self, packet):
        logger.info('Decoding Packet %s', packet.info['messagetype'])

        if packet.info['messagetype'] not in ['NOTIFY', 'REGISTER']:
            logger.warning('LocalNotifier cannot decode %s', packet.info['messagetype'])
            return

        # Every packet has an application name
        self.applicationName = packet.headers['Application-Name']
        logger.info('Application Name: %s', self.applicationName)

        # Pull out the notification type(s)
        if packet.info['messagetype'] == 'NOTIFY':
            self.notifications = [packet.headers['Notification-Name']]
        elif packet.info['messagetype'] == 'REGISTER':
            self.notifications = []
            for name in packet.notifications:
                self.notifications.append(name['Notification-Name'])
        logger.info('Notification Name: %s', self.notifications)

        if packet.headers.get('Notification-Icon'):
            resource = packet.headers['Notification-Icon']
            self.icon = self.get_resource(packet, resource)
        else:
            self.icon = None

        logger.debug('%s', packet.headers)

        self.growl = Growl.GrowlNotifier(
            applicationName=self.applicationName,
            notifications=self.notifications,
            defaultNotifications=self.notifications
        )

        if packet.info['messagetype'] == 'REGISTER':
            self.growl.register()
        elif packet.info['messagetype'] == 'NOTIFY':
            self.growl.notify(
                noteType=packet.headers['Notification-Name'],
                title=packet.headers['Notification-Title'],
                description=packet.headers['Notification-Name'],
                icon=self.icon
            )

    def get_resource(self, packet, resource):
        try:
            if resource.startswith('x-growl-resource://'):
                logger.info('Getting inline resource')
                resource = resource.split('://')
                return packet.get(resource[1])['Data']
            elif resource.startswith('http'):
                logger.info('Getting url resource: %s', resource)
                resource = resource.replace(' ', '%20')
                icon = urllib2.urlopen(resource, None, 5)
                return icon.read()
            else:
                return None
        except Exception, e:
            print e
            return None
