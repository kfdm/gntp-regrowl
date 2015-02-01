"""
Echo a growl to OSX NotificationCenter
Created by heilerich (https://github.com/heilerich)

Config Example:
[regrowl.bridge.netcent]
verbose = True
"""

from __future__ import absolute_import

import logging
import Foundation
import objc
import AppKit

from regrowl.regrowler import ReGrowler

logger = logging.getLogger(__name__)

__all__ = ['NetCenter']

SPACER = '=' * 80


class NetCenter(ReGrowler):
    valid = ['REGISTER', 'NOTIFY']

    def register(self, packet):
        logger.info('Register')
        print 'Registration Packet:'
        if self.getboolean('verbose', False):
            print SPACER
            print packet
            print SPACER
        else:
            print packet.headers['Application-Name']

    def mlnc_notify(self, title, subtitle, text, url):
        NSUserNotification = objc.lookUpClass('NSUserNotification')
        NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
        notification = NSUserNotification.alloc().init()
        notification.setTitle_(str(title))
        notification.setSubtitle_(str(subtitle))
        notification.setInformativeText_(str(text))
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
        notification.setHasActionButton_(True)
        notification.setOtherButtonTitle_("View")
        notification.setUserInfo_({"action":"open_url", "value":url})
        NSUserNotificationCenter.defaultUserNotificationCenter().setDelegate_(self)
        NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)

    def notify(self, packet):
        logger.info('Notify')
        print 'Notification Packet:'
        if self.getboolean('verbose', False):
            print SPACER
            print packet
            print SPACER
        else:
            print packet.headers['Notification-Title'],
            print packet.headers['Notification-Text']
            if 'Notification-Callback-Target' in packet.headers:
                self.mlnc_notify(packet.headers['Notification-Title'], "", packet.headers['Notification-Text'], packet.headers['Notification-Callback-Target'])
            else:
                self.mlnc_notify(packet.headers['Notification-Title'], "", packet.headers['Notification-Text'], "")
