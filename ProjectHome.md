This is the homepage of **pydot**, a Python interface to [Graphviz](http://www.graphviz.org/)'s Dot language.

**pydot** allows to easily create both directed and non directed graphs from Python. Currently all attributes implemented in the Dot language are supported (up to Graphviz 2.26.3).

Output can be inlined in Postscript into interactive scientific environments like [TeXmacs](http://www.texmacs.org/), or output in any of the format's supported by the Graphviz tools _dot_, _neato_, _twopi_.

## Support for Python 3 ##

James Mills has created a [branch for Python 3 compatibility](https://bitbucket.org/prologic/pydot)

## Requirements ##

  * [pyparsing](http://pyparsing.wikispaces.com/) in order to load DOT files.
  * [Graphviz](http://www.research.att.com/sw/tools/graphviz/) to render the graphs.


## Changelog ##

#### Version: **1.0.28** ####
  * Fixed [issue 52](https://code.google.com/p/pydot/issues/detail?id=52). Improved handling of BOM-less UTF-8 encoded files.
  * Fixed [issue 55](https://code.google.com/p/pydot/issues/detail?id=55) regarding unicode handling.
  * Fixed [issue 50](https://code.google.com/p/pydot/issues/detail?id=50) where an ending colon in a node name was understood as a port separator. Colons as the last character of node names will be left as-is.
  * [Issue 59](https://code.google.com/p/pydot/issues/detail?id=59) (and duplicate [issue 62](https://code.google.com/p/pydot/issues/detail?id=62)): Program arguments are mishandled in `Dot.create` - Patch merged.
  * Fixed [issue 49](https://code.google.com/p/pydot/issues/detail?id=49), handling of quotes in unicode html-labels.
  * Fixed [issue 60](https://code.google.com/p/pydot/issues/detail?id=60). Added an additional check in `__get_attribute__` to not assume the parent graph is always retrievable.
  * Fixed [issue 61](https://code.google.com/p/pydot/issues/detail?id=61). Graph names will be adequately quoted when necessary.

#### Version: **1.0.25** ####
  * Improved the message raised by `TypeErrors`.
  * If arguments need to be specified for 'dot', 'neato' and rest of graph layout engines they can now be passed to the `create()` and `create_*()` family of functions. If a string is passed it's expected to be simply the name of the program. If a list is passed it's assumed to contain strings, the name of the layout engine as the first element, followed by any optional arguments that will be later appended to the command line.
  * Improved parsing of DOT files where a subgraph was given inline as the source or destination of an edge.

#### Version: **1.0.23** ####
  * Fixed [Issue 46](https://code.google.com/p/pydot/issues/detail?id=46) and modified the version number to include the subversion revision number, hence the small jump from 1.0.4 to 1.0.23 ;-)


The release 1.0.3 of **pydot** is mainly a maintenance release. It badly needed some attention. Most of the open issues have been addressed.

The release 1.0.2 of **pydot** boasts the following:

  * The parser has been improved a lot. It passes all of GraphViz's regression tests (which I consider quite an accomplishment seeing the kind of crazy constructs on those )
  * Different charsets should now be dealt with properly.
  * The search of GraphViz's executables has been improved for all platforms. On Windows, paths and registry keys are searched. On Unix now it should exhibit the same behavior as the traditional shell path search. (Thanks Andy Gimblett and many others)
  * Double-quoted paths in Windows are nor properly handled. The os.path.exists() check fails if a valid path is enclosed within quotes.
  * 'type' keyword has been changed everywhere to 'graph\_type'
  * Better handling of Node/Edge/Graph defaults. Added methods: set\_graph\_defaults, set\_node\_defaults, set\_edge\_defaults, get\_graph\_defaults, get\_node\_defaults, get\_edge\_defaults
  * Now it's possible to use rank to lay out nodes at the same level
```
    graph = pydot.Dot('graphname', graph_type='digraph') 
    subg = pydot.Subgraph('', rank='same') 
    subg.add_node(pydot.Node('a')) 
    graph.add_subgraph(subg) 
    subg.add_node(pydot.Node('b')) 
    subg.add_node(pydot.Node('c')) 
```
  * Multiple main graphs in a file are now supported, will be returned as a list of graph instances
  * Handling of shapefiles Dot().set\_shape\_files()
  * Added method "add\_style()" to the Node class to easily append styles to a node
  * Attribute lists updated to reflect the available ones in graphviz 2.16
  * Added error reporting when rendering graphs with GraphViz executables. There was an often reported problem where the output graphs would have 0 size. In most cases this was due to Graphviz missing a library for a format that pydot assumed to be there. Now the error given by the executable will be reported instead of being silently ignored (Thanks Jarno)
  * Improved parsing of identifiers
  * Added non-GraphViz attributes needed by dot2tex
  * Jose Fonseca contributed a fix dealing with quoted strings the the dot parsing module
  * setup.py updated so that it's possible to install pydot through Setuptools' easy\_install
  * Edge()'s can be created passing two Node objects as well as, the previously supported, two strings with node names. Warning: when passing two Node instances, the attributes won't be taken into account. The edge will only read the Nodes' names to create an edge, the Nodes must be separately added to the graph so all their attributes are "remembered".
  * Substituted all str()'s for unicode()'s
  * It's possible now to manually specify the path to GraphViz's executables in the case they can't be found automatically. The method 'set\_graphviz\_executables(paths)' will take a dictionary specifying the location of the executables. Please refer to the documentation for usage detailed information.
  * And too many bugfixes to list...

**Performance:**

The new pydot stores graphs and their objects using a hierarchy of nested dictionaries and lists. Graph, Node, Edge objects are mere proxies to the data and are created on demand. So that now it's possible to have a graph with a 1 million edges and there will not be a single Edge instance (only if requested, then they will be created on demand, mapping the data and providing with all the methods to act on the data in the global dictionary).

Storing a graph with 1 million edges in pydot 1.0 has approximately the same memory requirements (~813MiB) as dealing with one with only 40.000 edges in pydot 0.9 (~851MiB), the 40.000 edges graph needs ~35MiB in pydot 1.0 . Handling graphs should be much faster, as no linear searches are performed in pydot 1.0

## Related Projects ##

  * [dot2tex](http://code.google.com/p/dot2tex/)
  * [XDot](http://code.google.com/p/jrfonseca/wiki/XDot)
