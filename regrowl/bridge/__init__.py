"""
Bridge Plugin Loader

Load all the bridge plugins in regrowl.bridge.*
"""
import logging
import inspect

import pkg_resources

from regrowl.regrowler import ReGrowler

logger = logging.getLogger(__name__)


def load_bridges(options):
    bridges = []
    for bridge in pkg_resources.iter_entry_points('regrowl.bridge'):
        if not options.has_section(bridge.module_name):
            logger.debug('Skipping %s. Not Enabled', bridge)
            continue
        try:
            obj = bridge.load()
        except ImportError, e:
            logger.error('Unable to import %s: %s', bridge, e)
        else:
            if inspect.isclass(obj) and \
                    issubclass(obj, ReGrowler) and \
                    obj is not ReGrowler:
                bridges.append(obj)
                logger.debug('Loaded %s', bridge)
    return bridges
