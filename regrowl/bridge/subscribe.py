from __future__ import absolute_import
from regrowl.regrowler import ReGrowler


__all__ = ['SubscribelNotifier']

SPACER = '=' * 80


class SubscribelNotifier(ReGrowler):
    valid = ['SUBSCRIBE']

    def subscribe(self, packet):
        print SPACER
        print self.srcaddr
        print self.srcport
        print packet.info
        print SPACER
        for key in packet.headers:
            print key, packet.headers[key]
