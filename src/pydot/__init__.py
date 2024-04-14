"""An interface to GraphViz."""
import logging

__author__ = "Ero Carrera"
__version__ = "2.0.1.dev0"
__license__ = "MIT"


_logger = logging.getLogger(__name__)
_logger.debug("pydot initializing")
_logger.debug("pydot %s", __version__)


from pydot.exceptions import *
from pydot.core import *
