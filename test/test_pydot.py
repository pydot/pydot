# coding=utf-8
# TODO:
# -test graph generation APIs (from adjacency, etc..)
# -test del_node, del_edge methods
# -test Common.set method
from __future__ import division
from __future__ import print_function

import io
import os
import pickle
import string
import sys
import unittest
import warnings
from hashlib import sha256
from textwrap import dedent

import chardet
import mock
import pytest

import pydot


TESTS_DIR_1 = "my_tests"
TESTS_DIR_2 = "graphs"

CURRENT_DIR = os.path.dirname(__file__)
REGRESSION_TESTS_DIR = os.path.join(CURRENT_DIR, "graphs")
MY_REGRESSION_TESTS_DIR = os.path.join(CURRENT_DIR, "my_tests")
TEST_PROGRAM = "dot"


@pytest.fixture
def digraph():
    return pydot.Graph("testgraph", graph_type="digraph")


@pytest.mark.parametrize("graph_type", ("graph", "digraph"))
def test_keep_graph_type(graph_type):
    graph = pydot.Dot(graph_name="Test", graph_type=graph_type)
    assert graph.get_type() == graph_type
    assert graph.graph_type == graph_type


def test_node_style():
    node = pydot.Node("mynode")
    assert node.get_style() is None

    node.add_style("abc")
    assert node.get_style() == "abc"

    node.add_style("def")
    assert node.get_style() == "abc,def"

    node.add_style("ghi")
    assert node.get_style() == "abc,def,ghi"


# NOTE(prmtl): might fail due to problems
# with different order of attributes in resulting
# graph
def test_create_simple_graph_with_node():
    graph = pydot.Dot(graph_type="digraph")

    node = pydot.Node("legend")
    node.set("shape", "box")
    node.set("label", "mine")

    graph.add_node(node)

    assert graph.to_string() == dedent(
        """\
        digraph G {
        legend [label=mine, shape=box];
        }
        """
    )


def test_attribute_with_implicit_value():
    dot = dedent(
        """
    digraph {
    na -> b[label="hi", decorate];
    }
    """
    )
    (graph,) = pydot.graph_from_dot_data(dot)
    edge = graph.get_edges()[0]
    attrs = edge.get_attributes()
    assert attrs == {"decorate": None, "label": '"hi"'}


def test_subgraphs():
    graph = pydot.Graph()
    subgraph = pydot.Subgraph("foo")

    assert graph.get_subgraphs() == []
    assert graph.get_subgraph_list() == []

    graph.add_subgraph(subgraph)

    assert len(graph.get_subgraphs()) == 1
    assert len(graph.get_subgraph_list()) == 1

    assert graph.get_subgraphs()[0].get_name() == subgraph.get_name()
    assert graph.get_subgraph_list()[0].get_name() == subgraph.get_name()


def test_graph_is_picklabe():
    graph = pydot.Graph()
    subgraph = pydot.Subgraph("foo")
    graph.add_subgraph(subgraph)
    graph.add_edge(pydot.Edge("A", "B"))
    graph.add_edge(pydot.Edge("A", "C"))
    graph.add_edge(pydot.Edge(("D", "E")))
    graph.add_node(pydot.Node("node!"))

    assert isinstance(pickle.dumps(graph), bytes)


def test_unicode_ids():
    node1 = '"aánñoöüé€"'
    node2 = '"îôø®çßΩ"'

    graph = pydot.Dot()
    graph.set_charset("latin1")
    graph.add_node(pydot.Node(node1))
    graph.add_node(pydot.Node(node2))
    graph.add_edge(pydot.Edge(node1, node2))

    assert graph.get_node(node1)[0].get_name() == node1
    assert graph.get_node(node2)[0].get_name() == node2

    assert graph.get_edges()[0].get_source() == node1
    assert graph.get_edges()[0].get_destination() == node2

    (graph2,) = pydot.graph_from_dot_data(graph.to_string())

    assert graph2.get_node(node1)[0].get_name() == node1
    assert graph2.get_node(node2)[0].get_name() == node2

    assert graph2.get_edges()[0].get_source() == node1
    assert graph2.get_edges()[0].get_destination() == node2


def test_parse_multiple_graphs():
    graph_data = dedent(
        """\
        graph A { a->b };
        graph B {c->d}
        """
    )
    graphs = pydot.graph_from_dot_data(graph_data)
    assert len(graphs) == 2
    assert sorted(g.get_name() for g in graphs) == sorted(["A", "B"])


def test_numeric_node_id(digraph):
    digraph.add_node(pydot.Node(1))
    assert digraph.get_nodes()[0].get_name() == "1"


def test_quoted_node_id(digraph):
    digraph.add_node(pydot.Node('"node"'))
    assert digraph.get_nodes()[0].get_name() == '"node"'


def test_quoted_node_id_to_string_no_attributes(digraph):
    digraph.add_node(pydot.Node('"node"'))
    assert digraph.get_nodes()[0].to_string() == '"node";'


def test_keyword_node_id(digraph):
    digraph.add_node(pydot.Node("node"))
    assert digraph.get_nodes()[0].get_name() == "node"


def test_keyword_node_id_to_string_no_attributes(digraph):
    digraph.add_node(pydot.Node("node"))
    assert digraph.get_nodes()[0].to_string() == ""


def test_keyword_node_id_to_string_with_attributes(digraph):
    digraph.add_node(pydot.Node("node", shape="box"))
    assert digraph.get_nodes()[0].to_string() == "node [shape=box];"


def test_names_of_a_thousand_nodes(digraph):
    names = set(["node_%05d" % i for i in range(10 ** 4)])

    for name in names:
        digraph.add_node(pydot.Node(name, label=name))

    assert set([n.get_name() for n in digraph.get_nodes()]) == names


@pytest.mark.parametrize("node", (1, "a", None))
def test_graph_add_node_argument_type(digraph, node):
    with pytest.raises(TypeError) as exc_info:
        digraph.add_node(node)

    assert "add_node() received a non node class object" in str(exc_info.value)


@pytest.mark.parametrize("edge", (1, "a", None))
def test_graph_add_edge_argument_type(digraph, edge):
    with pytest.raises(TypeError) as exc_info:
        digraph.add_edge(edge)

    assert "add_edge() received a non edge class object" in str(exc_info.value)


@pytest.mark.parametrize("subgraph", (1, "a", None))
def test_graph_add_subgraph_argument_type(digraph, subgraph):
    with pytest.raises(TypeError) as exc_info:
        digraph.add_subgraph(subgraph)
    assert "add_subgraph() received a non subgraph class object" in str(
        exc_info.value
    )


def test_quoting():
    g = pydot.Dot()
    g.add_node(pydot.Node("test", label=string.printable))
    data = g.create(format="jpe")
    assert len(data) > 0


# @pytest.mark.xfail(
#     (3, 7) > sys.version_info >= (3, 6),
#     reason="python 3.6 on Travis is failing this and no way to debug it now",
# )
def test_dotparser_import_warning():
    with mock.patch.dict(sys.modules, {"dot_parser": None}):
        with pytest.warns(
            UserWarning,
            match="Couldn't import dot_parser, loading"
            " of dot files will not be possible.",
        ):
            del sys.modules["pydot"]
            warnings.simplefilter("always")
            import pydot  # noqa: F401


# class TestGraphAPI(unittest.TestCase):
#     def test_graph_with_shapefiles(self):
#         shapefile_dir = os.path.join(CURRENT_DIR, "from-past-to-future")
#         # image files are omitted from sdist
#         if not os.path.isdir(shapefile_dir):
#             warnings.warn(
#                 "Skipping tests that involve images, "
#                 "they can be found in the `git` repository."
#             )
#             return
#         dot_file = os.path.join(shapefile_dir, "from-past-to-future.dot")
#
#         pngs = [
#             os.path.join(shapefile_dir, fname)
#             for fname in os.listdir(shapefile_dir)
#             if fname.endswith(".png")
#         ]
#
#         f = open(dot_file, "rt")
#         graph_data = f.read()
#         f.close()
#
#         # g = dot_parser.parse_dot_data(graph_data)
#         graphs = pydot.graph_from_dot_data(graph_data)
#         (g,) = graphs
#         g.set_shape_files(pngs)
#
#         jpe_data = g.create(format="jpe")
#
#         hexdigest = sha256(jpe_data).hexdigest()
#         hexdigest_original = self._render_with_graphviz(
#             dot_file, encoding="ascii"
#         )
#         self.assertEqual(hexdigest, hexdigest_original)
#
#     def _render_with_graphviz(self, filename, encoding):
#         with io.open(filename, "rt", encoding=encoding) as stdin:
#             stdout_data, stderr_data, process = pydot.call_graphviz(
#                 program=TEST_PROGRAM,
#                 arguments=["-Tjpe"],
#                 working_dir=os.path.dirname(filename),
#                 stdin=stdin,
#             )
#
#         assert process.returncode == 0, stderr_data
#
#         return sha256(stdout_data).hexdigest()
#
#     def _render_with_pydot(self, filename, encoding):
#         c = pydot.graph_from_dot_file(filename, encoding=encoding)
#         sha = ""
#         for g in c:
#             jpe_data = g.create(
#                 prog=TEST_PROGRAM, format="jpe", encoding=encoding
#             )
#             sha += sha256(jpe_data).hexdigest()
#         return sha
#
#     def test_my_regression_tests(self):
#         self._render_and_compare_dot_files(MY_REGRESSION_TESTS_DIR)
#
#     def test_graphviz_regression_tests(self):
#         self._render_and_compare_dot_files(REGRESSION_TESTS_DIR)
#
#     def _render_and_compare_dot_files(self, directory):
#         # files that confuse `chardet`
#         encodings = {"Latin1.dot": "latin-1"}
#         dot_files = [
#             fname for fname in os.listdir(directory) if fname.endswith(".dot")
#         ]
#         for fname in dot_files:
#             fpath = os.path.join(directory, fname)
#             with open(fpath, "rb") as f:
#                 s = f.read()
#             estimate = chardet.detect(s)
#             encoding = encodings.get(fname, estimate["encoding"])
#             os.sys.stdout.write("#")
#             os.sys.stdout.flush()
#             pydot_sha = self._render_with_pydot(fpath, encoding)
#             graphviz_sha = self._render_with_graphviz(fpath, encoding)
#             assert pydot_sha == graphviz_sha, (pydot_sha, graphviz_sha)
#
#     def test_executable_not_found_exception(self):
#         graph = pydot.Dot("graphname", graph_type="digraph")
#         self.assertRaises(Exception, graph.create, prog="dothehe")
#
#
# def test_dot_args(self):
#     g = pydot.Dot()
#     u = pydot.Node("a")
#     g.add_node(u)
#     g.write_svg("test.svg", prog=["twopi", "-Goverlap=scale"])


if __name__ == "__main__":
    pytest.main(sys.argv[0])
    print("The tests are using `pydot` from: {pd}".format(pd=pydot))
