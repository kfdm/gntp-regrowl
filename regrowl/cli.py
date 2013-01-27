from optparse import OptionParser
from ConfigParser import SafeConfigParser
import logging
import os

from regrowl.server import GNTPServer


CONFIG_PATH = [
    os.path.expanduser('~/.regrowl'),
    '.regrowl'
    ]

DEFAULTS = {
    'host': '0.0.0.0',
    'port': 12345,
    'password': None,
}


class ParserWithConfig(OptionParser):
    def __init__(self, config):
        OptionParser.__init__(self)
        self.config = SafeConfigParser(DEFAULTS)
        self.config.read(CONFIG_PATH)

        if not self.config.has_section('regrowl.server'):
            self.config.add_section('regrowl.server')

    def add_default_option(self, *args, **kwargs):
        # Map the correct config.get* to the type of option being added
        fun = {
            'int': self.config.getint,
            None: self.config.get,
        }.get(kwargs.get('type'))

        kwargs['default'] = fun('regrowl.server', kwargs.get('dest'))

        self.add_option(*args, **kwargs)


def main():
    parser = ParserWithConfig(CONFIG_PATH)
    parser.add_default_option(
        "-a", "--address",
        help="address to listen on",
        dest="host"
        )
    parser.add_default_option("-p", "--port",
        help="port to listen on",
        dest="port",
        type="int"
        )
    parser.add_default_option("-P", "--password",
        help="Network password",
        dest='password'
        )

    # Debug Options
    parser.add_option('-v', '--verbose',
        dest='verbose',
        default=logging.INFO,
        action='store_const',
        const=logging.DEBUG
        )
    parser.add_option("-d", "--debug",
        help="Print raw growl packets",
        dest='debug',
        action="store_true",
        default=False
        )
    parser.add_option("-q", "--quiet",
        help="Quiet mode",
        dest='debug',
        action="store_false"
        )

    (options, args) = parser.parse_args()

    try:
        import setproctitle
        setproctitle.setproctitle('regrowl-server')
    except ImportError:
        pass

    logging.basicConfig(level=options.verbose,
        format="%(name)-25s %(levelname)s:%(message)s")

    server = GNTPServer(options, parser.config)
    server.run()

if __name__ == "__main__":
    main()
