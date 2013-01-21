from __future__ import absolute_import

import urllib2
import Growl
import logging

from gntp.notifier import GrowlNotifier

logger = logging.getLogger(__name__)


class LocalNotifier(GrowlNotifier):
    def register(self):
        '''
        Resend a GNTP Register message to Growl running on a local OSX Machine
        '''
        logger.info('Sending local registration')
        logger.debug('    Application: %s', self.headers['Application-Name'])

        #Local growls only need a list of strings
        notifications = []
        defaultNotifications = []
        for notice in self.notifications:
            notifications.append(notice['Notification-Name'])
            if notice.get('Notification-Enabled', True):
                defaultNotifications.append(notice['Notification-Name'])

        appIcon = get_resource(self, 'Application-Icon')

        growl = Growl.GrowlNotifier(
            applicationName=self.headers['Application-Name'],
            notifications=notifications,
            defaultNotifications=defaultNotifications,
            applicationIcon=appIcon,
        )
        growl.register()
        return self.encode()

    def notify(self):
        '''
        Resend a GNTP Notify message to Growl running on a local OSX Machine
        '''
        logger = logging.getLogger('ReGrowl')
        logger.info('Sending local notification')
        logger.debug('    Application: %s', self.headers['Application-Name'])
        logger.debug('    Notification: %s', self.headers['Notification-Name'])
        logger.debug('    Title: %s', self.headers['Notification-Title'])
        logger.debug('    Text: %s', self.headers['Notification-Text'])

        growl = Growl.GrowlNotifier(
            applicationName=self.headers['Application-Name'],
            notifications=[self.headers['Notification-Name']]
        )

        noticeIcon = get_resource(self, 'Notification-Icon')

        growl.notify(
            noteType=self.headers['Notification-Name'],
            title=self.headers['Notification-Title'],
            description=self.headers.get('Notification-Text', ''),
            icon=noticeIcon
        )
        return self.encode()


def get_resource(self, key):
    logger = logging.getLogger('ReGrowl')
    try:
        resource = self.headers.get(key, '')
        if resource.startswith('x-growl-resource://'):
            logger.info('Getting inline resource')
            resource = resource.split('://')
            return self.resources.get(resource[1])['Data']
        elif resource.startswith('http'):
            logger.info('Getting url resource')
            logger.debug('    %s', resource)
            resource = resource.replace(' ', '%20')
            icon = urllib2.urlopen(resource, None, 5)
            return icon.read()
        else:
            return None
    except Exception, e:
        print e
        return None
