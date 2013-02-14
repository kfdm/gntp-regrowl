from __future__ import absolute_import
from regrowl.regrowler import ReGrowler


class SubscribelNotifier(ReGrowler):
    valid = ['SUBSCRIBE']

    def instance(self, packet):
        return None

    def subscribe(self, packet):
        print '='*80
        print self.srcaddr
        print self.srcport
        print packet.info
        print '='*80
        for key in packet.headers:
            print key, packet.headers[key]
