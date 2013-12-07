import ConfigParser
import twit
import os.path
import logging


_settings = None
logger = logging.getLogger(__name__)


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
        _settings = dict((k, v) for k, v in _config.items("main"))
    return _settings
