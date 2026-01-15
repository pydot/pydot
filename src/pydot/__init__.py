# SPDX-FileCopyrightText: 2024 pydot contributors
#
# SPDX-License-Identifier: MIT

"""An interface to GraphViz."""

import logging

__author__ = "Ero Carrera"
__version__ = "4.0.2.dev0"
__license__ = "MIT"


_logger = logging.getLogger(__name__)
_logger.debug("pydot initializing")
_logger.debug("pydot %s", __version__)


from pydot.classes import FrozenDict  # noqa: F401, E402
from pydot.constants import (  # noqa: F401, E402
    CLUSTER_ATTRIBUTES,
    DEFAULT_PROGRAMS,
    EDGE_ATTRIBUTES,
    GRAPH_ATTRIBUTES,
    NODE_ATTRIBUTES,
    OUTPUT_FORMATS,
)
from pydot.core import *  # noqa: F401, F403, E402
from pydot.exceptions import *  # noqa: F401, E402, F403
from pydot.launcher import (  # noqa: F401, E402
    call_graphviz,
    get_executable_extension,
    is_anaconda,
    is_windows,
)
