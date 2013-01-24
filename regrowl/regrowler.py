import logging
import urllib2

logger = logging.getLogger(__name__)


class ReGrowler(object):
    def __init__(self, packet, srcaddr, srcport):
        self.srcpacket = packet
        self.srcaddr = srcaddr
        self.srcport = srcport

        if packet.info['messagetype'] not in self.valid:
            logger.warning('<%s> cannot decode %s',
                self.__module__, packet.info['messagetype'])
            return

        # Registration and notification packets have Application-Name
        self.applicationName = packet.headers.get('Application-Name')
        logger.info('Application Name: %s', self.applicationName)

        # Pull out the notification type(s)
        if packet.info['messagetype'] == 'NOTIFY':
            self.notifications = [packet.headers['Notification-Name']]
        elif packet.info['messagetype'] == 'REGISTER':
            self.notifications = []
            for name in packet.notifications:
                self.notifications.append(name['Notification-Name'])
        else:
            self.notifications = []
        logger.info('Notification Name: %s', self.notifications)

        logger.debug('%s', packet.headers)

        self.growler = self.instance(packet)
        {
            'REGISTER': self.register,
            'NOTIFY': self.notify,
            'SUBSCRIBE': self.subscribe,
        }.get(packet.info['messagetype'])(packet)

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

    def instance(self, packet):
        raise NotImplementedError()

    def register(self, packet):
        raise NotImplementedError()

    def notify(self, packet):
        raise NotImplementedError()

    def subscribe(self, packet):
        raise NotImplementedError()
