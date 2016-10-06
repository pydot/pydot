[![Build Status][build_img]][travis]


About
=====

`pydot`:

  - is an interface to [Graphviz][1]
  - can parse and dump into the [DOT language][2] used by GraphViz,
  - is written in pure Python,

and [`networkx`][3] can convert its graphs to `pydot`.
Development occurs at [github][11] (under branch `dev`),
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

[1]: http://www.graphviz.org
[2]: https://en.wikipedia.org/wiki/DOT_%28graph_description_language%29
[3]: https://github.com/networkx/networkx
[4]: https://pypi.python.org/pypi
[5]: https://github.com/pypa/pip
[6]: http://pyparsing.wikispaces.com/
[7]: https://en.wikipedia.org/wiki/Package_manager
[8]: https://www.macports.org
[9]: https://github.com/ellson/graphviz
[10]: https://github.com/erocarrera/pydot/blob/master/LICENSE
[11]: https://github.com/erocarrera/pydot
[build_img]: https://travis-ci.org/erocarrera/pydot.svg?branch=master
[travis]: https://travis-ci.org/erocarrera/pydot
