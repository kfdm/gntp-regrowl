import argparse
import ConfigParser
import logging
import os

from regrowl.server import GNTPServer


DEFAULTS = {
    'host': '0.0.0.0',
    'port': 23053,
    'password': None,
    'timeout': 600,
    'bufferLength': 2048,
}


class ReloadableConfig(ConfigParser.RawConfigParser):
    def reload(self, path):
        config = ReloadableConfig(self.defaults())
        config.read(path)
        return config

config = ReloadableConfig(DEFAULTS)
# Ensuring this section always exists, makes our later
# logic easier. Since we're not saving over the config
# file this should be reasonably safe
if not config.has_section('regrowl.server'):
    config.add_section('regrowl.server')


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "-c", "--config",
        help="Config File",
        default=os.path.expanduser('~/.regrowl'),
    )

    args, _ = parser.parse_known_args()
    config.read(args.config)

    # Redefine our parser so that -h works with the entire
    # list of options
    parser = argparse.ArgumentParser(parents=[parser])
    parser.add_argument(
        "-a",
        "--address",
        help="address to listen on",
        dest="host",
        default=config.get('regrowl.server', 'host')
    )

    parser.add_argument(
        "-p",
        "--port",
        help="port to listen on",
        dest="port",
        type=int,
        default=config.getint('regrowl.server', 'port')
    )

    parser.add_argument(
        "-P",
        "--password",
        help="Network password",
        dest='password',
        default=config.get('regrowl.server', 'password')
    )

    # Debug Options
    parser.add_argument(
        '-v',
        '--verbose',
        dest='verbose',
        default=0,
        action='count',
    )

    parser.add_argument(
        "-r",
        "--reload",
        help="Auto reload config and bridges (Useful for development)",
        dest='reload',
        action="store_true",
        default=False,
    )

    options = parser.parse_args()
    options.verbose = logging.WARNING - options.verbose * 10

    try:
        import setproctitle
        setproctitle.setproctitle('regrowl-server')
    except ImportError:
        pass

    logging.basicConfig(
        level=options.verbose,
        format="%(name)-25s %(levelname)s:%(message)s"
    )

    server = GNTPServer(options, config)
    server.run()

if __name__ == "__main__":
    main()
