import argparse
import logging
import os

from regrowl.server import GNTPServer
from regrowl.config import ReloadableConfig, DEFAULTS
from regrowl.test import test_client, TEST_OPTIONS


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "-c", "--config",
        help="Config File",
        default=os.path.expanduser('~/.regrowl'),
    )

    args, _ = parser.parse_known_args()
    config = ReloadableConfig()
    config.read(args.config)

    # Redefine our parser so that -h works with the entire
    # list of options
    parser = argparse.ArgumentParser(parents=[parser])
    parser.add_argument(
        "-a",
        "--address",
        help="address to listen on",
        dest="host",
        default=config.get('regrowl.server', 'host', DEFAULTS['host'])
    )

    parser.add_argument(
        "-p",
        "--port",
        help="port to listen on",
        dest="port",
        type=int,
        default=config.getint('regrowl.server', 'port', DEFAULTS['port'])
    )

    parser.add_argument(
        "-P",
        "--password",
        help="Network password",
        dest='password',
        default=config.get('regrowl.server', 'password', DEFAULTS['password'])
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

    parser.add_argument(
        "-t",
        "--test",
        help="Simple built-in test client (Useful for development)",
        choices=TEST_OPTIONS
    )

    options = parser.parse_args()
    options.verbose = logging.WARNING - options.verbose * 10

    if options.test:
        return test_client(config, options)

    try:
        import setproctitle
        setproctitle.setproctitle('regrowl-server')
    except ImportError:
        pass

    logging.basicConfig(
        level=options.verbose,
        format="%(levelname)-7s %(name)-25s %(message)s"
    )

    server = GNTPServer(options, config)
    server.run()

if __name__ == "__main__":
    main()
