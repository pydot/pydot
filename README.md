[![Build Status](https://www.travis-ci.com/pydot/pydot.svg?branch=master)](https://www.travis-ci.com/pydot/pydot)
[![PyPI](https://img.shields.io/pypi/v/pydot.svg)](https://pypi.org/project/pydot/)


About
=====

`pydot`:

  - is an interface to [Graphviz][1]
  - can parse and dump into the [DOT language][2] used by GraphViz,
  - is written in pure Python,

and [`networkx`][3] can convert its graphs to `pydot`.
Development occurs at [GitHub][11] (under branch `dev`),
where you can report issues and contribute code.


Installation
============

From [PyPI][4] using [`pip`][5]:

`pip install pydot`

From source:

`python setup.py install`


Dependencies
============

- [`pyparsing`][6]: used only for *loading* DOT files,
  installed automatically during `pydot` installation.

- GraphViz: used to render graphs as PDF, PNG, SVG, etc.
  Should be installed separately, using your system's
  [package manager][7], something similar (e.g., [MacPorts][8]),
  or from [its source][9].


License
=======

Distributed under an [MIT license][10].


Troubleshooting
===============

How to enable logging
---------------------

`pydot` uses Python's standard `logging` module and registers the
following loggers:

- `pydot.dot_parser`: Messages related to the parsing of DOT strings.
- `pydot.core`: All other messages.

Being a library, `pydot` does not add any handlers to its loggers, nor
does it touch the root logger. The loggers are created with the default
level `NOTSET`. Their implied parent logger `pydot` can be used to
control their levels.

To see the logs, assuming logging has not been configured already:

    >>> import logging
    >>> logging.basicConfig(level=logging.DEBUG)
    >>> import pydot
    DEBUG:pydot.dot_parser:pydot dot_parser module initializing
    DEBUG:pydot.core:pydot core module initializing
    DEBUG:pydot.core:pydot <version>

**Warning**: When `DEBUG` level logging is enabled, `pydot` may log the
data that it processes, such as graph contents or DOT strings. This can
cause the log to become very large or contain sensitive information.

For more options, check out the [Python logging documentation][12] and
the [`logging_tree`][13] visualizer.


[1]: https://www.graphviz.org
[2]: https://en.wikipedia.org/wiki/DOT_%28graph_description_language%29
[3]: https://github.com/networkx/networkx
[4]: https://pypi.python.org/pypi
[5]: https://github.com/pypa/pip
[6]: https://github.com/pyparsing/pyparsing
[7]: https://en.wikipedia.org/wiki/Package_manager
[8]: https://www.macports.org
[9]: https://github.com/ellson/graphviz
[10]: https://github.com/pydot/pydot/blob/master/LICENSE
[11]: https://github.com/pydot/pydot
[12]: https://docs.python.org/3/library/logging.html
[13]: https://pypi.org/project/logging_tree/
