[![Build Status](https://www.travis-ci.com/pydot/pydot.svg?branch=master)](https://www.travis-ci.com/pydot/pydot)
[![PyPI](https://img.shields.io/pypi/v/pydot.svg)](https://pypi.org/project/pydot/)


About
=====

`pydot`:

  - is an interface to [Graphviz][1]
  - can parse and dump into the [DOT language][2] used by GraphViz,
  - is written in pure Python,

and [`networkx`][3] can convert its graphs to `pydot`.

Development occurs at [GitHub][11], where you can report issues and
contribute code.


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

[1]: https://www.graphviz.org
[2]: https://en.wikipedia.org/wiki/DOT_%28graph_description_language%29
[3]: https://github.com/networkx/networkx
[4]: https://pypi.python.org/pypi
[5]: https://github.com/pypa/pip
[6]: https://github.com/pyparsing/pyparsing
[7]: https://en.wikipedia.org/wiki/Package_manager
[8]: https://www.macports.org
[9]: https://gitlab.com/graphviz/graphviz
[10]: https://github.com/pydot/pydot/blob/master/LICENSE
[11]: https://github.com/pydot/pydot
