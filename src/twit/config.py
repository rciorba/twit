import ConfigParser
import os
import os.path
import logging

import twit


_settings = None
logger = logging.getLogger(__name__)


class OnionDict(object):
    def __init__(self, *args):
        self.__dictionaries = args

    def __getitem__(self, key):
        for d in self.__dictionaries:
            if key in d:
                return d[key]
        raise KeyError(key)

    def __contains__(self, key):
        for d in self.__dictionaries:
            if key in d:
                return True
        return False

    def get(self, key, default=None):
        if key in self:
            return self[key]
        else:
            return default


def get_config():
    global _settings
    if _settings is None:
        _config = ConfigParser.ConfigParser()
        default = os.path.join(twit.__path__[0], "twit.conf")
        _config.read(default)
        local_settings = os.getenv("TWIT_SETTINGS") or os.path.join(
            twit.__path__[0], "twit_local.conf")
        if local_settings:
            _config.read(local_settings)
        _settings = OnionDict(
            dict((k, v) for k, v in _config.items("main")),
            os.environ)
    return _settings
