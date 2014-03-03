"""
Send push notifications

Uses pushnotify to send notifications to iOS and Android devices

Requires https://pypi.python.org/pypi/pushnotify

Sample config

[regrowl.bridge.push]
label = prowl,<apikey>
other = nma,<apikey>
example = pushover,<apikey>
"""

from __future__ import absolute_import

try:
    import pushnotify
except ImportError:
    raise ImportError('Requires https://pypi.python.org/pypi/pushnotify Please install from PyPi')

import logging

from regrowl.regrowler import ReGrowler


logger = logging.getLogger(__name__)
logging.getLogger('requests').setLevel(logging.WARNING)


__all__ = ['PushNotifier']


class PushNotifier(ReGrowler):
    valid = ['NOTIFY']

    _kwargs = {
        'Notification-Callback-Target': 'url',
        'Notification-Priority': 'pritory',
    }

    def notify(self, packet):
        for label, settings in self.config.items(__name__):
            notifier, apikey = settings.split(',')

            client = pushnotify.get_client(
                notifier, packet.headers['Application-Name'])

            if not client:
                logger.error('Error loading push provider %s', notifier)
                return

            logger.info('Sending push to %s with %s', label, notifier)
            kwargs = {}
            for key, target in self._kwargs.items():
                if key in packet.headers:
                    kwargs[target] = packet.headers[key]

            client.add_key(apikey)
            client.notify(
                packet.headers['Notification-Text'],
                packet.headers['Notification-Title'],
                kwargs=kwargs
            )
