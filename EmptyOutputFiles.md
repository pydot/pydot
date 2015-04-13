# Introduction #

If the [Graphviz](http://graphviz.org/) binaries are not installed in default locations _pydot_ will not find them. _pydot_ scans for the binaries through all the directories specified in the PATH enviroment variable.

If you are obtaining empty output files when using _pydot_'s output functionality through the "write" methods, try adding the path to [Graphviz](http://graphviz.org/)'s binaries (_fdp_, _twopi_, _neato_, _dot_, _circo_) to the PATH environment variable. That should fix the issue.

In OSX the path to the binaries usually looks like one of these:

  * `/usr/local/graphviz-2.12/bin/`
  * `/Applications/Graphviz.app/Contents/MacOS/`