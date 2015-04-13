Since [revision 14](https://code.google.com/p/pydot/source/detail?r=14) it's possible to run a set of tests to attempt to guarantee backwards compatibility and successful parsing of a set of graphs ranging from the trivial to the rather complex. The graphs include some collected from Graphviz's own testing sets and others I've created to test specific issues.

To run the script `pydot_unittest.py` it should suffice with going to the `./test` directory and running it from there. If _pydot_ is able to find Graphviz's executables (_and it should be able under Windows, Linux and OSX if Graphviz is in any of the standard locations_) then the tests should run without major problems.

Running the tests usually take a few minutes. Currently all test run successfully with the current revision.