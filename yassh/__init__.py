import logging
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

from .reactor import *
from .command import *
from .exceptions import *

__version__ = '0.1.dev'
__revision__ = ''
__all__ = ['Command',
           'Reactor',
           'AlreadyStartedException']

