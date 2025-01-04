# SPDX-FileCopyrightText: 2024 pydot contributors
#
# SPDX-License-Identifier: MIT

"""Unit testing of `pydot`."""

# TODO:
# -test graph generation APIs (from adjacency, etc..)
# -test del_node, del_edge methods
# -test Common.set method

import functools
import importlib
import os
import pickle
import string
import sys
import textwrap
import unittest
from hashlib import sha256

import chardet
import pydot
from parameterized import parameterized
from pydot._vendor import tempfile

TEST_ERROR_DIR = os.getenv("TEST_ERROR_DIR", None)

TEST_PROGRAM = "dot"
TESTS_DIR_1 = "my_tests"
TESTS_DIR_2 = "graphs"

_test_root = os.path.dirname(os.path.abspath(__file__))


class RenderResult:
    """Results object returned by Renderer methods."""

    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        """Get the raw image data for the result."""
        return self._data

    @functools.cached_property
    def checksum(self):
        """Get the sha256 checksum for the result."""
        return sha256(self.data).hexdigest()


class Renderer:
    """Call pydot renderers for data files."""

    @classmethod
    def graphviz(cls, filename, encoding):
        with open(filename, encoding=encoding) as stdin:
            stdout_data, stderr_data, process = pydot.call_graphviz(
                program=TEST_PROGRAM,
                arguments=["-Tjpe"],
                working_dir=os.path.dirname(filename),
                stdin=stdin,
            )
        assert process.returncode == 0, stderr_data
        return RenderResult(stdout_data)

    @classmethod
    def pydot(cls, filename, encoding):
        c = pydot.graph_from_dot_file(filename, encoding=encoding)
        if not c:
            raise RuntimeError("No data returned from pydot!")
        jpe_data = bytearray()
        for g in c:
            jpe_data.extend(
                g.create(prog=TEST_PROGRAM, format="jpe", encoding=encoding)
            )
        return RenderResult(jpe_data)


def _load_test_cases(casedir):
    """Return a list of testcase files,

    Returns a list of tuples of the form:
        ("case_file_name", "case_file_name.dot", "path/to/directory")
    """
    global _test_root
    path = os.path.join(_test_root, casedir)
    dot_files = filter(lambda x: x.endswith(".dot"), os.listdir(path))

    def _case_name(fname: str) -> str:
        """No str.removesuffix() until Python 3.9."""
        if sys.version_info < (3, 9):
            return fname
        return fname.removesuffix(".dot")

    return [(_case_name(dot_file), dot_file, path) for dot_file in dot_files]


def _compare_images(fname: str, pydot: RenderResult, gv: RenderResult) -> bool:
    """Compare two RenderResult objects for the named test.

    If the images differ and a ``TEST_ERROR_DIR`` has been provided, create
    a subdir for the test and dump both images there for examination."""
    if pydot.checksum == gv.checksum:
        return True
    if TEST_ERROR_DIR is not None:
        dirname = fname.replace(".", "_")
        out_dir = os.path.join(os.path.normpath(TEST_ERROR_DIR), dirname)
        os.makedirs(out_dir)
        pydot_path = os.path.join(out_dir, "err_pydot.jpeg")
        gv_path = os.path.join(out_dir, "err_graphviz.jpeg")
        with open(pydot_path, "wb") as p, open(gv_path, "wb") as g:
            p.write(pydot.data)
            g.write(gv.data)
    return False


class PydotTestCase(unittest.TestCase):
    def setUp(self):
        self._reset_graphs()

    def _reset_graphs(self):
        self.graph_directed = pydot.Graph("testgraph", graph_type="digraph")


class TestGraphAPI(PydotTestCase):
    def test_keep_graph_type(self):
        g = pydot.Dot(graph_name="Test", graph_type="graph")
        self.assertEqual(g.get_type(), "graph")
        g = pydot.Dot(graph_name="Test", graph_type="digraph")
        self.assertEqual(g.get_type(), "digraph")

    def test_add_style(self):
        node = pydot.Node("mynode")
        node.add_style("abc")
        self.assertEqual(node.get_style(), "abc")
        node.add_style("def")
        self.assertEqual(node.get_style(), "abc,def")
        node.add_style("ghi")
        self.assertEqual(node.get_style(), "abc,def,ghi")

    def test_create_simple_graph_with_node(self):
        g = pydot.Dot()
        g.set_type("digraph")
        node = pydot.Node("legend")
        node.set("shape", "box")
        g.add_node(node)
        node.set("label", "mine")
        s = g.to_string()
        expected = "digraph G {\nlegend [shape=box, label=mine];\n}\n"
        assert s == expected

    def test_attribute_with_implicit_value(self):
        d = 'digraph {\na -> b[label="hi", decorate];\n}'
        graphs = pydot.graph_from_dot_data(d)
        (g,) = graphs
        attrs = g.get_edges()[0].get_attributes()

        self.assertEqual("decorate" in attrs, True)

    def test_subgraphs(self):
        g = pydot.Graph()
        s = pydot.Subgraph("foo")

        self.assertEqual(g.get_subgraphs(), [])
        self.assertEqual(g.get_subgraph_list(), [])

        g.add_subgraph(s)

        self.assertEqual(g.get_subgraphs()[0].get_name(), s.get_name())
        self.assertEqual(g.get_subgraph_list()[0].get_name(), s.get_name())

    def test_graph_pickling(self):
        g = pydot.Graph()
        s = pydot.Subgraph("foo")
        g.add_subgraph(s)
        g.add_edge(pydot.Edge("A", "B"))
        g.add_edge(pydot.Edge("A", "C"))
        g.add_edge(pydot.Edge(("D", "E")))
        g.add_node(pydot.Node("node!"))
        pickle.dumps(g)

    def test_dot_pickling(self):
        g = pydot.Dot()
        g.set_prog("neato")
        g.set_shape_files("dummy.png")
        pkl = pickle.dumps(g)
        g2 = pickle.loads(pkl)
        self.assertIsInstance(g2, pydot.Dot)
        self.assertEqual(g2.prog, "neato")
        self.assertEqual(g2.shape_files[0], "dummy.png")

    def test_unicode_ids(self):
        node1 = '"aánñoöüé€"'
        node2 = '"îôø®çßΩ"'

        g = pydot.Dot()
        g.set_charset("latin1")
        g.add_node(pydot.Node(node1))
        g.add_node(pydot.Node(node2))
        g.add_edge(pydot.Edge(node1, node2))

        self.assertEqual(g.get_node(node1)[0].get_name(), node1)
        self.assertEqual(g.get_node(node2)[0].get_name(), node2)

        self.assertEqual(g.get_edges()[0].get_source(), node1)
        self.assertEqual(g.get_edges()[0].get_destination(), node2)
        graphs = pydot.graph_from_dot_data(g.to_string())
        (g2,) = graphs

        self.assertEqual(g2.get_node(node1)[0].get_name(), node1)
        self.assertEqual(g2.get_node(node2)[0].get_name(), node2)

        self.assertEqual(g2.get_edges()[0].get_source(), node1)
        self.assertEqual(g2.get_edges()[0].get_destination(), node2)

    def test_graph_simplify(self):
        # Fail example: pydot 1.0.2. GH pydot/pydot#92 OP patch 1.
        g = pydot.Graph()
        g.add_edge(pydot.Edge("a", "b"))
        g.add_edge(pydot.Edge("a", "b"))
        g.add_edge(pydot.Edge("b", "a"))
        g.add_edge(pydot.Edge("b", "a"))
        test_combinations = [
            (
                "graph",
                False,
                "graph G { a -- b; a -- b; b -- a; b -- a; }",
            ),
            (
                "graph",
                True,
                "graph G { a -- b; }",
            ),
            (
                "digraph",
                False,
                "digraph G { a -> b; a -> b; b -> a; b -> a; }",
            ),
            (
                "digraph",
                True,
                "digraph G { a -> b; b -> a; }",
            ),
        ]
        expected_concat = observed_concat = ""
        for graph_type, simplify, expected in test_combinations:
            expected_concat += (
                f"graph_type {graph_type}, simplify {simplify}: {expected}\n"
            )
            g.set_type(graph_type)
            g.set_simplify(simplify)
            try:
                observed = " ".join(g.to_string().split())
            except (NameError, TypeError) as e:
                type_name = type(e).__name__
                observed = f"{type_name}: {e}"
            observed_concat += (
                f"graph_type {graph_type}, simplify {simplify}: {observed}\n"
            )
        self.maxDiff = None
        self.assertMultiLineEqual(expected_concat, observed_concat)

    def test_multiple_graphs(self):
        graph_data = "graph A { a->b };\ngraph B {c->d}"
        graphs = pydot.graph_from_dot_data(graph_data)
        n = len(graphs)
        assert n == 2, n
        names = [g.get_name() for g in graphs]
        assert names == ["A", "B"], names

    def test_numeric_node_id(self):
        self._reset_graphs()
        self.graph_directed.add_node(pydot.Node(1))
        self.assertEqual(self.graph_directed.get_nodes()[0].get_name(), "1")

    def test_numeric_quoting(self):
        num = pydot.Node("12", label=1.4, width=".75")
        non = pydot.Node("1.2.3", label="1.4.0")
        self.assertEqual(num.to_string(), "12 [label=1.4, width=.75];")
        self.assertEqual(non.to_string(), '"1.2.3" [label="1.4.0"];')

    def test_quoted_node_id(self):
        self._reset_graphs()
        self.graph_directed.add_node(pydot.Node('"node"'))
        self.assertEqual(
            self.graph_directed.get_nodes()[0].get_name(), '"node"'
        )

    def test_quoted_node_id_to_string_no_attributes(self):
        self._reset_graphs()
        self.graph_directed.add_node(pydot.Node('"node"'))
        self.assertEqual(
            self.graph_directed.get_nodes()[0].to_string(), '"node";'
        )

    def test_keyword_node_id(self):
        self._reset_graphs()
        self.graph_directed.add_node(pydot.Node("node"))
        self.assertEqual(self.graph_directed.get_nodes()[0].get_name(), "node")

    def test_keyword_node_id_to_string_no_attributes(self):
        self._reset_graphs()
        self.graph_directed.add_node(pydot.Node("node"))
        self.assertEqual(self.graph_directed.get_nodes()[0].to_string(), "")

    def test_keyword_node_id_to_string_with_attributes(self):
        self._reset_graphs()
        self.graph_directed.add_node(pydot.Node("node", shape="box"))
        self.assertEqual(
            self.graph_directed.get_nodes()[0].to_string(), "node [shape=box];"
        )

    def test_keyword_node_id_in_label(self):
        self.graph_directed.add_node(pydot.Node("Node", label="Node"))
        self.assertEqual(
            self.graph_directed.get_nodes()[0].to_string(),
            'Node [label="Node"];',
        )

    def test_comma_separated_attribute_values_to_string(self):
        self._reset_graphs()
        self.graph_directed.add_node(
            pydot.Node("node", color="green", style="rounded,filled")
        )
        self.assertEqual(
            self.graph_directed.get_nodes()[0].to_string(),
            'node [color=green, style="rounded,filled"];',
        )

    def test_attribute_string_values_quoting(self):
        self._reset_graphs()
        self.graph_directed.add_node(
            pydot.Node("node", length=1.234, size="2.345", radius="9,876")
        )
        self.assertEqual(
            self.graph_directed.get_nodes()[0].to_string(),
            'node [length=1.234, size=2.345, radius="9,876"];',
        )

    def test_names_of_a_thousand_nodes(self):
        self._reset_graphs()
        names = {f"node_{i:05d}" for i in range(10**3)}
        for name in names:
            self.graph_directed.add_node(pydot.Node(name, label=name))

        self.assertEqual(
            {n.get_name() for n in self.graph_directed.get_nodes()}, names
        )

    def test_executable_not_found_exception(self):
        graph = pydot.Dot("graphname", graph_type="digraph")
        self.assertRaises(Exception, graph.create, prog="dothehe")

    def test_graph_add_node_argument_type(self):
        self._reset_graphs()
        self.assertRaises(TypeError, self.graph_directed.add_node, 1)
        self.assertRaises(TypeError, self.graph_directed.add_node, "a")

    def test_graph_add_edge_argument_type(self):
        self._reset_graphs()
        self.assertRaises(TypeError, self.graph_directed.add_edge, 1)
        self.assertRaises(TypeError, self.graph_directed.add_edge, "a")

    def test_graph_add_subgraph_argument_type(self):
        self._reset_graphs()
        self.assertRaises(TypeError, self.graph_directed.add_subgraph, 1)
        self.assertRaises(TypeError, self.graph_directed.add_subgraph, "a")

    def test_node_parenting(self):
        g = pydot.Dot()
        n = pydot.Node("node a")
        n2 = pydot.Node("node a")
        g.add_node(n)
        g.add_node(n2)

        nodes = g.get_node('"node a"')
        for node in nodes:
            assert node.get_parent_graph() == g

        sg = pydot.Subgraph("sub sg")
        sg_n = pydot.Node("node a")
        sg.add_node(sg_n)
        self.assertEqual(sg_n.get_parent_graph(), sg)

        g.add_node(sg_n)
        self.assertEqual(sg_n.get_parent_graph(), sg)

        g.add_subgraph(sg)
        self.assertEqual(sg_n.get_parent_graph(), g)

    def test_quoting(self):
        g = pydot.Dot()
        g.add_node(pydot.Node("test", label=string.printable))
        data = g.create(format="jpe")
        self.assertEqual(len(data) > 0, True)

    def test_keyword_quoting(self):
        g = pydot.Dot(graph_name="graph", graph_type="graph")
        g.add_node(pydot.Node("digraph", color="red"))
        g.add_node(pydot.Node("strict", shape="box"))
        g.add_node(pydot.Node("A", label="digraph"))
        g.add_node(pydot.Node("B", label="subgraph"))
        g.add_node(pydot.Node("edge", style="dashed"))
        g.add_edge(pydot.Edge("A", "B", xlabel="node"))

        formatted = g.to_string()
        self.assertEqual(
            formatted,
            textwrap.dedent("""\
                graph "graph" {
                "digraph" [color=red];
                "strict" [shape=box];
                A [label="digraph"];
                B [label="subgraph"];
                edge [style=dashed];
                A -- B [xlabel="node"];
                }
                """),
        )

    def test_alphanum_quoting(self):
        """Test the fix for issue #408."""
        g = pydot.Dot(graph_name="issue408", graph_type="graph")
        n1 = pydot.Node(
            "11herbs", label="and 11¼ spices", fontsize=12, height="1"
        )
        n2 = pydot.Node("nooks9nooks", fontsize="14pt", height="2in")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(pydot.Edge(n1, n2, minlength="4pt"))

        self.assertEqual(
            g.to_string(),
            textwrap.dedent("""\
                graph issue408 {
                "11herbs" [label="and 11¼ spices", fontsize=12, height=1];
                nooks9nooks [fontsize="14pt", height="2in"];
                "11herbs" -- nooks9nooks [minlength="4pt"];
                }
                """),
        )

    def test_alphanum_quoting2(self):
        """Test the fix for issue #418."""
        g = pydot.Dot(graph_name="issue418", graph_type="graph")
        n1 = pydot.Node("foo.bar", color="red")
        n2 = pydot.Node("baz", color="blue")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(pydot.Edge(n1, n2))

        self.assertEqual(
            g.to_string(),
            textwrap.dedent("""\
                graph issue418 {
                "foo.bar" [color=red];
                baz [color=blue];
                "foo.bar" -- baz;
                }
                """),
        )

    def test_edge_quoting(self):
        """Test the fix for issue #383 (pydot 3.0.0)."""
        g = pydot.Graph("", graph_type="digraph")
        g.add_node(pydot.Node("Node^A"))
        g.add_node(pydot.Node("Node^B"))
        g.add_edge(pydot.Edge("Node^A", "Node^B"))
        self.assertEqual(
            g.to_string(),
            textwrap.dedent("""\
            digraph {
            "Node^A";
            "Node^B";
            "Node^A" -> "Node^B";
            }
            """),
        )

    def test_id_storage_and_lookup(self):
        g = pydot.Graph()
        a = pydot.Node("my node")
        b = pydot.Node('"node B"')
        e = pydot.Edge(a, b)

        g.add_node(a)
        g.add_node(b)
        g.add_edge(e)

        a_out = g.get_node("my node")[0]
        b_out = g.get_node('"node B"')[0]
        self.assertEqual(g.get_node("node B"), [])
        self.assertEqual(id(a_out.obj_dict), id(a.obj_dict))
        self.assertEqual(id(b_out.obj_dict), id(b.obj_dict))

        e_out = g.get_edge("my node", '"node B"')[0]
        self.assertEqual(id(e_out.obj_dict), id(e.obj_dict))

        sg = pydot.Subgraph("sub graph", graph_type="graph")
        sgA = pydot.Node("sg A")
        sgB = pydot.Node('"sg B"')
        sg.add_node(sgA)
        sg.add_node(sgB)
        g.add_subgraph(sg)

        sg_out = g.get_subgraph("sub graph")[0]
        self.assertEqual(id(sg_out.obj_dict), id(sg.obj_dict))

        g_nodes_out = g.get_nodes()
        self.assertEqual(id(g_nodes_out[0].obj_dict), id(a.obj_dict))
        self.assertEqual(id(g_nodes_out[1].obj_dict), id(b.obj_dict))

        g_edges_out = g.get_edges()
        self.assertEqual(id(g_edges_out[0].obj_dict), id(e.obj_dict))

        g_sg_out = g.get_subgraphs()
        self.assertEqual(id(g_sg_out[0].obj_dict), id(sg.obj_dict))

        sg_nodes_out = sg.get_nodes()
        self.assertEqual(id(sg_nodes_out[0].obj_dict), id(sgA.obj_dict))
        self.assertEqual(id(sg_nodes_out[1].obj_dict), id(sgB.obj_dict))
        self.assertEqual(sg.get_edges(), [])

    def test_dot_args(self):
        g = pydot.Dot()
        u = pydot.Node("a")
        g.add_node(u)
        with tempfile.TemporaryDirectory(
            ignore_cleanup_errors=True
        ) as tmp_dir:
            outfile = os.path.join(tmp_dir, "test.svg")
            g.write_svg(outfile, prog=["twopi", "-Goverlap=scale"])

    def test_edge_equality_basics_3_same_points_not_not_equal(self):
        # Fail example: pydot 1.4.1 on Python 2.
        g = pydot.Graph()
        e1 = pydot.Edge("a", "b")
        e2 = pydot.Edge("a", "b")
        g.add_edge(e1)
        g.add_edge(e2)
        self.assertFalse(e1 != e2)

    def test_edge_point_namestr(self):
        self._reset_graphs()
        self.graph_directed.add_edge(pydot.Edge("a", "b"))
        self.assertEqual(
            self.graph_directed.get_edges()[0].to_string(), "a -> b;"
        )

    def test_edge_point_object_node(self):
        self._reset_graphs()
        self.graph_directed.add_edge(
            pydot.Edge(pydot.Node("a"), pydot.Node("b"))
        )
        self.assertEqual(
            self.graph_directed.get_edges()[0].to_string(), "a -> b;"
        )

    def test_edge_point_object_subgraph(self):
        self._reset_graphs()
        self.graph_directed.add_edge(
            pydot.Edge(pydot.Subgraph("a"), pydot.Subgraph("b"))
        )
        self.assertEqual(
            self.graph_directed.get_edges()[0].to_string(), "a -> b;"
        )

    def test_edge_point_object_cluster(self):
        self._reset_graphs()
        self.graph_directed.add_edge(
            pydot.Edge(pydot.Cluster("a"), pydot.Cluster("b"))
        )
        self.assertEqual(
            self.graph_directed.get_edges()[0].to_string(),
            "cluster_a -> cluster_b;",
        )

    def test_graph_from_adjacency_matrix(self):
        g = pydot.graph_from_adjacency_matrix(
            [[0, 1, 0], [1, 0, 0], [0, 1, 1]], directed=True
        )
        s = " ".join(g.to_string().split())
        self.assertEqual(s, "digraph G { 1 -> 2; 2 -> 1; 3 -> 2; 3 -> 3; }")
        g = pydot.graph_from_adjacency_matrix(
            [[0, 1, 0], [1, 0, 0], [0, 0, 1]], directed=False
        )
        s = " ".join(g.to_string().split())
        self.assertEqual(s, "graph G { 1 -- 2; 3 -- 3; }")

    def test_graph_from_incidence_matrix(self):
        g = pydot.graph_from_incidence_matrix(
            [[-1, 1, 0], [1, -1, 0], [0, 1, -1]], directed=True
        )
        s = " ".join(g.to_string().split())
        self.assertEqual(s, "digraph G { 1 -> 2; 2 -> 1; 3 -> 2; }")
        g = pydot.graph_from_incidence_matrix(
            [[1, 1, 0], [0, 1, 1]], directed=False
        )
        s = " ".join(g.to_string().split())
        self.assertEqual(s, "graph G { 1 -- 2; 2 -- 3; }")

    def test_version(self):
        self.assertIsInstance(pydot.__version__, str)

    def test_logging_init(self):
        with self.assertLogs("pydot", level="DEBUG") as cm:
            importlib.reload(pydot)
            importlib.reload(pydot.core)
            importlib.reload(pydot.dot_parser)
        self.assertEqual(
            cm.output,
            [
                "DEBUG:pydot:pydot initializing",
                f"DEBUG:pydot:pydot {pydot.__version__}",
                "DEBUG:pydot.core:pydot core module initializing",
                "DEBUG:pydot.dot_parser:pydot dot_parser module initializing",
            ],
        )
        importlib.reload(pydot)


class TestShapeFiles(PydotTestCase):
    shapefile_dir = os.path.join(_test_root, "from-past-to-future")

    # image files are omitted from sdist
    @unittest.skipUnless(
        os.path.isdir(shapefile_dir),
        "Skipping tests that involve images,"
        + " they can be found in the git repository",
    )
    def test_graph_with_shapefiles(self):
        dot_file = os.path.join(self.shapefile_dir, "from-past-to-future.dot")

        pngs = [
            os.path.join(self.shapefile_dir, fname)
            for fname in os.listdir(self.shapefile_dir)
            if fname.endswith(".png")
        ]

        with open(dot_file) as f:
            graph_data = f.read()

        graphs = pydot.graph_from_dot_data(graph_data)
        self.assertIsNotNone(graphs)

        if not isinstance(graphs, list):
            return
        g = graphs.pop()
        g.set_shape_files(pngs)

        rendered = RenderResult(g.create(format="jpe"))
        graphviz = Renderer.graphviz(dot_file, encoding="ascii")
        if not _compare_images("from-past-to-future", rendered, graphviz):
            raise AssertionError(
                "from-past-to-future.dot: "
                f"{rendered.checksum} != {graphviz.checksum} "
                "(found pydot vs graphviz difference)"
            )


class RenderedTestCase(PydotTestCase):
    def _render_and_compare_dot_file(self, fdir, fname):
        # files that confuse `chardet`
        encodings = {"Latin1.dot": "latin-1"}
        fpath = os.path.join(fdir, fname)
        with open(fpath, "rb") as f:
            s = f.read()
        estimate = chardet.detect(s)
        encoding = encodings.get(fname, estimate["encoding"])
        rendered = Renderer.pydot(
            fpath,
            encoding,
        )
        graphviz = Renderer.graphviz(
            fpath,
            encoding,
        )
        if not _compare_images(fname, rendered, graphviz):
            raise AssertionError(
                f"{fname}: {rendered.checksum} != {graphviz.checksum} "
                "(found pydot vs graphviz difference)"
            )


class TestMyRegressions(RenderedTestCase):
    """Perform regression tests in my_tests dir."""

    @parameterized.expand(functools.partial(_load_test_cases, TESTS_DIR_1))
    def test_regression(self, _, fname, path):
        self._render_and_compare_dot_file(path, fname)


class TestGraphvizRegressions(RenderedTestCase):
    """Perform regression tests in graphs dir."""

    @parameterized.expand(functools.partial(_load_test_cases, TESTS_DIR_2))
    def test_regression(self, _, fname, path):
        self._render_and_compare_dot_file(path, fname)
