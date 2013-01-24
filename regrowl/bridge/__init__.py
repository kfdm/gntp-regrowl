"""
Bridge Plugin Loader

Load all the bridge plugins in regrowl.bridge.*
"""
import logging
import imp
import os
import glob

logger = logging.getLogger(__name__)

# All bridge plugins should be in the same directory as the bridge loader
MODULE_PATH = os.path.dirname(__file__)
# We want to search for only python files
SEARCHPATH = os.path.join(MODULE_PATH, '*.py')
# And we want to make sure to blacklist the bridge loader itself
BLACKLIST = ['__init__']


def load_bridges():
    bridges = []
    for module in glob.glob(SEARCHPATH):
        # Get just the module name without the directory or .py
        module = os.path.basename(module).split('.')[0]
        if module in BLACKLIST:
            continue

        try:
            # We use the short name of the module with the search path
            _fp, _pathname, _description = imp.find_module(module, [MODULE_PATH])
            # And then add back the __package__ part so that it acts a
            # bit more like a "proper" module
            module = '{0}.{1}'.format(__package__, module)
            mod = imp.load_module(module, _fp, _pathname, _description)
        except ImportError:
            logger.error('Unable to import %s', module)
        else:
            logger.info('Loaded %s module', mod.__name__)
            bridges.append(mod)
        finally:
            if _fp:
                _fp.close()
    return bridges
