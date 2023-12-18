# coding=utf-8
"""Unit testing of `pydot`."""
# TODO:
# -test graph generation APIs (from adjacency, etc..)
# -test del_node, del_edge methods
# -test Common.set method
import argparse
import datetime
from hashlib import sha256
import io
import os
import pickle
import string
import sys
import warnings

import chardet
import pydot
import unittest


TEST_PROGRAM = "dot"
TESTS_DIR_1 = "my_tests"
TESTS_DIR_2 = "graphs"


class TestGraphAPI(unittest.TestCase):
    def setUp(self):
        self._reset_graphs()

    def _reset_graphs(self):
        self.graph_directed = pydot.Graph("testgraph", graph_type="digraph")

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
        expected = "digraph G {\nlegend [label=mine, shape=box];\n}\n"
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
            expected_concat += "graph_type %s, simplify %s: %s\n" % (
                graph_type,
                simplify,
                expected,
            )
            g.set_type(graph_type)
            g.set_simplify(simplify)
            try:
                observed = " ".join(g.to_string().split())
            except (NameError, TypeError) as e:
                observed = "%s: %s" % (type(e).__name__, e)
            observed_concat += "graph_type %s, simplify %s: %s\n" % (
                graph_type,
                simplify,
                observed,
            )
        self.maxDiff = None
        self.assertMultiLineEqual(expected_concat, observed_concat)

    def test_graph_with_shapefiles(self):
        shapefile_dir = os.path.join(test_dir, "from-past-to-future")
        # image files are omitted from sdist
        if not os.path.isdir(shapefile_dir):
            warnings.warn(
                "Skipping tests that involve images, "
                "they can be found in the `git` repository."
            )
            return
        dot_file = os.path.join(shapefile_dir, "from-past-to-future.dot")

        pngs = [
            os.path.join(shapefile_dir, fname)
            for fname in os.listdir(shapefile_dir)
            if fname.endswith(".png")
        ]

        f = open(dot_file, "rt")
        graph_data = f.read()
        f.close()

        graphs = pydot.graph_from_dot_data(graph_data)
        (g,) = graphs
        g.set_shape_files(pngs)

        jpe_data = g.create(format="jpe")

        hexdigest = sha256(jpe_data).hexdigest()
        _, hexdigest_original = self._render_with_graphviz(
            dot_file, encoding="ascii"
        )
        if hexdigest != hexdigest_original:
            raise AssertionError(
                "from-past-to-future.dot: "
                f"{hexdigest} != {hexdigest_original} "
                "(found pydot vs graphviz difference)"
            )

    def test_multiple_graphs(self):
        graph_data = "graph A { a->b };\ngraph B {c->d}"
        graphs = pydot.graph_from_dot_data(graph_data)
        n = len(graphs)
        assert n == 2, n
        names = [g.get_name() for g in graphs]
        assert names == ["A", "B"], names

    def _render_with_graphviz(self, filename, encoding):
        with io.open(filename, "rt", encoding=encoding) as stdin:
            stdout_data, stderr_data, process = pydot.call_graphviz(
                program=TEST_PROGRAM,
                arguments=["-Tjpe"],
                working_dir=os.path.dirname(filename),
                stdin=stdin,
            )

        assert process.returncode == 0, stderr_data
        return stdout_data, sha256(stdout_data).hexdigest()

    def _render_with_pydot(self, filename, encoding):
        c = pydot.graph_from_dot_file(filename, encoding=encoding)
        jpe_data = bytearray()
        for g in c:
            jpe_data.extend(
                g.create(prog=TEST_PROGRAM, format="jpe", encoding=encoding)
            )
        return jpe_data, sha256(jpe_data).hexdigest()

    def test_my_regression_tests(self):
        path = os.path.join(test_dir, TESTS_DIR_1)
        self._render_and_compare_dot_files(path)

    def test_graphviz_regression_tests(self):
        path = os.path.join(test_dir, TESTS_DIR_2)
        self._render_and_compare_dot_files(path)

    def _render_and_compare_dot_files(self, directory):
        # files that confuse `chardet`
        encodings = {"Latin1.dot": "latin-1"}
        dot_files = [
            fname for fname in os.listdir(directory) if fname.endswith(".dot")
        ]
        for fname in dot_files:
            fpath = os.path.join(directory, fname)
            with open(fpath, "rb") as f:
                s = f.read()
            estimate = chardet.detect(s)
            encoding = encodings.get(fname, estimate["encoding"])
            os.sys.stdout.write("#")
            os.sys.stdout.flush()
            pydot_bytes, pydot_sha = self._render_with_pydot(
                fpath,
                encoding,
            )
            graphviz_bytes, graphviz_sha = self._render_with_graphviz(
                fpath,
                encoding,
            )
            if pydot_sha != graphviz_sha:
                # In case of error, save both images locally for inspection
                now = datetime.datetime.now().strftime("%H_%M_%S")
                with open(f"err_{fname}_pydot_{now}.jpeg", "wb") as f:
                    f.write(pydot_bytes)
                with open(f"err_{fname}_graphviz_{now}.jpeg", "wb") as f:
                    f.write(graphviz_bytes)
                pydot_bytes
                raise AssertionError(
                    f"{fname}: {pydot_sha} != {graphviz_sha} "
                    "(found pydot vs graphviz difference)"
                )

    def test_numeric_node_id(self):
        self._reset_graphs()
        self.graph_directed.add_node(pydot.Node(1))
        self.assertEqual(self.graph_directed.get_nodes()[0].get_name(), "1")

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

    def test_names_of_a_thousand_nodes(self):
        self._reset_graphs()
        names = {"node_%05d" % i for i in range(10**3)}
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

    def test_quoting(self):
        g = pydot.Dot()
        g.add_node(pydot.Node("test", label=string.printable))
        data = g.create(format="jpe")
        self.assertEqual(len(data) > 0, True)

    def test_dot_args(self):
        g = pydot.Dot()
        u = pydot.Node("a")
        g.add_node(u)
        g.write_svg("test.svg", prog=["twopi", "-Goverlap=scale"])

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


def parse_args():
    """Parse arguments. Deprecated since pydot 2.0."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--no-check", action="store_true")
    args, unknown = parser.parse_known_args()
    if args.no_check:
        print(
            "WARNING: The --no-check option became redundant with pydot 2.0 "
            "and will be removed in a future major release of pydot.\n",
            file=sys.stderr,
        )
    # avoid confusing `unittest`
    sys.argv = [sys.argv[0]] + unknown


if __name__ == "__main__":
    parse_args()
    test_dir = os.path.dirname(os.path.abspath(__file__))
    print("The tests are using `pydot` from:  {pd}".format(pd=pydot))
    unittest.main(verbosity=2)
