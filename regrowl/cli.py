from optparse import OptionParser
from ConfigParser import RawConfigParser
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


class DefaultConfig(RawConfigParser):
    def __init__(self, *args, **kwargs):
        RawConfigParser.__init__(self, *args, **kwargs)
        if not self.has_section('regrowl.server'):
            self.add_section('regrowl.server')

        self.get = self._wrap_default(self.get)
        self.getint = self._wrap_default(self.getint)
        self.getboolean = self._wrap_default(self.getboolean)

    def _wrap_default(self, function):
        def _wrapper(section, option, default=None):
            try:
                return function(section, option)
            except:
                return default
        return _wrapper


class ParserWithConfig(OptionParser):
    def __init__(self, config):
        OptionParser.__init__(self)
        self.config = DefaultConfig(DEFAULTS)
        self.config.read(CONFIG_PATH)

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
