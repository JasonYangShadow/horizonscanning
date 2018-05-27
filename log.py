import logging
from exception import Type,TeleException
from config import Config

LOGGER = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
config = Config()
logpath = config.getValue('sys','logpath')
loglevel = config.getValue('sys','loglevel')
if logpath is not None:
    fh = logging.FileHandler(logpath)
    fh.setFormatter(formatter)
    LOGGER.addHandler(fh)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
LOGGER.addHandler(ch)

if loglevel is not None:
    if loglevel == 'debug':
        LOGGER.setLevel(logging.DEBUG)
    elif loglevel == 'info':
        LOGGER.setLevel(logging.INFO)
    elif loglevel == 'warn':
        LOGGER.setLevel(logging.WARN)
    elif loglevel == 'error':
        LOGGER.setLevel(logging.ERROR)
    elif loglevel == 'fatal':
        LOGGER.setLevel(logging.FATAL)
    else:
        raise TeleException(Type.MissMatchException,"loglevel should be one of 'debug','info','warn','error' and 'fatal'")


