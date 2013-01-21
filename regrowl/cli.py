from optparse import OptionParser
import logging
import os

from regrowl.server import GNTPServer, GNTPHandler


def store_path(option, opt, value, parser):
    setattr(parser.values, option.dest, os.path.realpath(value))


class ServerParser(OptionParser):
    def __init__(self, domain='com.github.kfdm.gntp'):
        OptionParser.__init__(self)

        # Network Options
        self.add_option("-a", "--address", help="address to listen on",
                    dest="host", default='localhost')
        self.add_option("-p", "--port", help="port to listen on",
                    dest="port", type="int", default=12345)
        self.add_option("-P", "--password", help="Network password",
                    dest='password')

        # Debug Options
        self.add_option('-l', '--log', dest='log', default='server.log',
                    action='callback', callback=store_path, type=str)
        self.add_option('-v', '--verbose', dest='verbose', default=logging.INFO,
                    action='store_const', const=logging.DEBUG)
        self.add_option("-d", "--debug", help="Print raw growl packets",
                    dest='debug', action="store_true", default=False)
        self.add_option("-q", "--quiet", help="Quiet mode",
                    dest='debug', action="store_false")

    def parse_args(self, args=None, values=None):
        values, args = OptionParser.parse_args(self, args, values)
        return values, args


def main():
    (options, args) = ServerParser().parse_args()

    try:
        import setproctitle
        setproctitle.setproctitle('regrowl-server')
    except ImportError:
        pass
    logging.basicConfig(level=logging.DEBUG,
        format='%(name)-12s: %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M',
        filename=options.log)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    server = GNTPServer(options, GNTPHandler)
    server.run()

if __name__ == "__main__":
    main()
