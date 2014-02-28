import ConfigParser

DEFAULTS = {
    'host': '0.0.0.0',
    'port': 23053,
    'password': None,
    'timeout': 600,
    'bufferLength': 2048,
    'passwordHash': 'SHA1',
}


class ReloadableConfig(ConfigParser.RawConfigParser):
    def __init__(self, *args, **kwargs):
        ConfigParser.RawConfigParser.__init__(self, *args, **kwargs)
        self.get = self._wrap_default(self.get)
        self.getint = self._wrap_default(self.getint)
        self.getboolean = self._wrap_default(self.getboolean)

        # Ensuring this section always exists, makes our later
        # logic easier. Since we're not saving over the config
        # file this should be reasonably safe
        if not self.has_section('regrowl.server'):
            self.add_section('regrowl.server')

    def reload(self, path):
        config = ReloadableConfig(self.defaults())
        config.read(path)
        return config

    def _wrap_default(self, function):
        def _wrapper(section, option, default=None):
            try:
                return function(section, option)
            except:
                return default
        return _wrapper
