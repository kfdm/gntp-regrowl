import logging
import sys

logger = logging.getLogger(__name__)


def load_bridges():
    notifiers = []
    try:
        from regrowl.bridge.local import LocalNotifier
    except ImportError:
        logger.error('Unable to import LocalNotifier')
    else:
        logger.info('Loaded %s', LocalNotifier)
        notifiers.append(sys.modules['regrowl.bridge.local'])
    return notifiers
