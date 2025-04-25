# SPDX-FileCopyrightText: 2025 pydot contributors
#
# SPDX-License-Identifier: MIT

"""Unit testing of pydot api calls."""

import os
import pickle
import string
import textwrap
import typing as T

import pytest

import pydot
from pydot._vendor import tempfile


def test_keep_graph_type() -> None:
    g = pydot.Dot(graph_name="Test", graph_type="graph")
    assert g.get_type() == "graph"
    g = pydot.Dot(graph_name="Test", graph_type="digraph")
    assert g.get_type() == "digraph"


def test_add_style() -> None:
    node = pydot.Node("mynode")
    node.add_style("abc")
    assert node.get("style") == "abc"
    node.add_style("def")
    assert node.get("style") == "abc,def"
    node.add_style("ghi")
    assert node.get("style") == "abc,def,ghi"


def test_create_simple_graph_with_node() -> None:
    g = pydot.Dot()
    g.set_type("digraph")
    node = pydot.Node("legend")
    node.set("shape", "box")
    g.add_node(node)
    node.set("label", "mine")
    s = g.to_string()
    expected = "digraph G {\nlegend [shape=box, label=mine];\n}\n"
    assert s == expected


def test_attribute_with_implicit_value() -> None:
    d = 'digraph {\na -> b[label="hi", decorate];\n}'
    graphs = pydot.graph_from_dot_data(d)
    (g,) = graphs
    attrs = g.get_edges()[0].get_attributes()

    assert "decorate" in attrs


def test_subgraphs() -> None:
    g = pydot.Graph()
    s = pydot.Subgraph("foo")

    assert g.get_subgraphs() == []
    assert g.get_subgraph_list() == []

    g.add_subgraph(s)

    assert g.get_subgraphs()[0].get_name() == s.get_name()
    assert g.get_subgraph_list()[0].get_name() == s.get_name()


def test_graph_pickling() -> None:
    g = pydot.Graph()
    s = pydot.Subgraph("foo")
    g.add_subgraph(s)
    g.add_edge(pydot.Edge("A", "B"))
    g.add_edge(pydot.Edge("A", "C"))
    g.add_edge(pydot.Edge(("D", "E")))
    g.add_node(pydot.Node("node!"))
    pkl = pickle.dumps(g)
    g2 = pickle.loads(pkl)
    assert isinstance(g2, pydot.Graph)
    s2 = g2.get_subgraph("foo")[0]
    assert s2.to_string() == s.to_string()
    assert g2.to_string() == g.to_string()


def test_dot_pickling() -> None:
    g = pydot.Dot()
    g.set_prog("neato")
    g.set_shape_files("dummy.png")
    pkl = pickle.dumps(g)
    g2 = pickle.loads(pkl)
    assert isinstance(g2, pydot.Dot)
    assert g2.prog == "neato"
    assert g2.shape_files[0] == "dummy.png"


def test_unicode_ids() -> None:
    node1 = '"aánñoöüé€"'
    node2 = '"îôø®çßΩ"'

    g = pydot.Dot()
    g.set("charset", "latin1")
    g.add_node(pydot.Node(node1))
    g.add_node(pydot.Node(node2))
    g.add_edge(pydot.Edge(node1, node2))

    assert g.get_node(node1)[0].get_name() == node1
    assert g.get_node(node2)[0].get_name() == node2

    assert g.get_edges()[0].get_source() == node1
    assert g.get_edges()[0].get_destination() == node2
    graphs = pydot.graph_from_dot_data(g.to_string())
    (g2,) = graphs

    assert g2.get_node(node1)[0].get_name() == node1
    assert g2.get_node(node2)[0].get_name() == node2

    assert g2.get_edges()[0].get_source() == node1
    assert g2.get_edges()[0].get_destination() == node2


def test_graph_simplify() -> None:
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
    for graph_type, simplify, expected in test_combinations:
        g.set_type(graph_type)
        g.set_simplify(simplify)
        result = " ".join(g.to_string().split())
        assert result == expected


def test_multiple_graphs() -> None:
    graph_data = "graph A { a->b };\ngraph B {c->d}"
    graphs = pydot.graph_from_dot_data(graph_data)
    n = len(graphs)
    assert n == 2
    names = [g.get_name() for g in graphs]
    assert names == ["A", "B"]


def test_numeric_node_id(graph_directed: pydot.Graph) -> None:
    graph_directed.add_node(pydot.Node(1))
    assert graph_directed.get_nodes()[0].get_name() == "1"


def test_numeric_quoting() -> None:
    num = pydot.Node("12", label=1.4, width=".75")
    non = pydot.Node("1.2.3", label="1.4.0")
    assert num.to_string() == "12 [label=1.4, width=.75];"
    assert non.to_string() == '"1.2.3" [label="1.4.0"];'


def test_quoted_node_id(graph_directed: pydot.Graph) -> None:
    graph_directed.add_node(pydot.Node('"node"'))
    assert graph_directed.get_nodes()[0].get_name() == '"node"'


def test_quoted_node_id_to_string_no_attributes(
    graph_directed: pydot.Graph,
) -> None:
    graph_directed.add_node(pydot.Node('"node"'))
    assert graph_directed.get_nodes()[0].to_string() == '"node";'


def test_keyword_node_id(graph_directed: pydot.Graph) -> None:
    graph_directed.add_node(pydot.Node("node"))
    assert graph_directed.get_nodes()[0].get_name() == "node"


def test_keyword_node_id_to_string_no_attributes(
    graph_directed: pydot.Graph,
) -> None:
    graph_directed.add_node(pydot.Node("node"))
    assert graph_directed.get_nodes()[0].to_string() == ""


def test_keyword_node_id_to_string_with_attributes(
    graph_directed: pydot.Graph,
) -> None:
    graph_directed.add_node(pydot.Node("node", shape="box"))
    assert graph_directed.get_nodes()[0].to_string() == "node [shape=box];"


def test_keyword_node_id_in_label(graph_directed: pydot.Graph) -> None:
    graph_directed.add_node(pydot.Node("Node", label="Node"))
    assert graph_directed.get_nodes()[0].to_string() == 'Node [label="Node"];'


def test_comma_separated_attribute_values_to_string(
    graph_directed: pydot.Graph,
) -> None:
    graph_directed.add_node(
        pydot.Node("node", color="green", style="rounded,filled")
    )
    assert (
        graph_directed.get_nodes()[0].to_string()
        == 'node [color=green, style="rounded,filled"];'
    )


def test_attribute_string_values_quoting(graph_directed: pydot.Graph) -> None:
    graph_directed.add_node(
        pydot.Node("node", length=1.234, size="2.345", radius="9,876")
    )
    assert (
        graph_directed.get_nodes()[0].to_string()
        == 'node [length=1.234, size=2.345, radius="9,876"];'
    )


def test_names_of_a_thousand_nodes(graph_directed: pydot.Graph) -> None:
    names = {f"node_{i:05d}" for i in range(10**3)}
    for name in names:
        graph_directed.add_node(pydot.Node(name, label=name))
    assert {n.get_name() for n in graph_directed.get_nodes()} == names


def test_executable_not_found_exception() -> None:
    graph = pydot.Dot("graphname", graph_type="digraph")
    with pytest.raises(FileNotFoundError):
        graph.create(prog="dothehe")


def test_graph_add_node_argument_type(graph_directed: pydot.Graph) -> None:
    with pytest.raises(TypeError):
        graph_directed.add_node(1)
    with pytest.raises(TypeError):
        graph_directed.add_node("a")


def test_graph_add_edge_argument_type(graph_directed: pydot.Graph) -> None:
    with pytest.raises(TypeError):
        graph_directed.add_edge(1)
    with pytest.raises(TypeError):
        graph_directed.add_edge("a")


def test_graph_add_subgraph_argument_type(graph_directed: pydot.Graph) -> None:
    with pytest.raises(TypeError):
        graph_directed.add_subgraph(1)
    with pytest.raises(TypeError):
        graph_directed.add_subgraph("a")


def test_node_parenting() -> None:
    g = pydot.Dot()
    n = pydot.Node("node a")
    n2 = pydot.Node("node a")
    g.add_node(n)
    g.add_node(n2)

    nodes = g.get_node("node a")
    for node in nodes:
        assert node.get_parent_graph() == g

    sg = pydot.Subgraph("sub sg")
    sg_n = pydot.Node("node a")
    sg.add_node(sg_n)
    assert sg_n.get_parent_graph() == sg

    g.add_node(sg_n)
    assert sg_n.get_parent_graph() == sg

    g.add_subgraph(sg)
    assert sg_n.get_parent_graph() == g


def test_quoting() -> None:
    g = pydot.Dot()
    g.add_node(pydot.Node("test", label=string.printable))
    data = g.create(format="jpe")
    assert len(data) > 0


def test_keyword_quoting() -> None:
    g = pydot.Dot(graph_name="graph", graph_type="graph")
    g.add_node(pydot.Node("digraph", color="red"))
    g.add_node(pydot.Node("strict", shape="box"))
    g.add_node(pydot.Node("A", label="digraph"))
    g.add_node(pydot.Node("B", label="subgraph"))
    g.add_node(pydot.Node("edge", style="dashed"))
    g.add_edge(pydot.Edge("A", "B", xlabel="node"))

    formatted = g.to_string()
    assert formatted == textwrap.dedent("""\
            graph "graph" {
            "digraph" [color=red];
            "strict" [shape=box];
            A [label="digraph"];
            B [label="subgraph"];
            edge [style=dashed];
            A -- B [xlabel="node"];
            }
            """)


def test_alphanum_quoting() -> None:
    """Test the fix for issue #408."""
    g = pydot.Dot(graph_name="issue408", graph_type="graph")
    n1 = pydot.Node("11herbs", label="and 11¼ spices", fontsize=12, height="1")
    n2 = pydot.Node("nooks9nooks", fontsize="14pt", height="2in")
    g.add_node(n1)
    g.add_node(n2)
    g.add_edge(pydot.Edge(n1, n2, minlength="4pt"))

    assert g.to_string() == textwrap.dedent("""\
            graph issue408 {
            "11herbs" [label="and 11¼ spices", fontsize=12, height=1];
            nooks9nooks [fontsize="14pt", height="2in"];
            "11herbs" -- nooks9nooks [minlength="4pt"];
            }
            """)


def test_alphanum_quoting2() -> None:
    """Test the fix for issue #418."""
    g = pydot.Dot(graph_name="issue418", graph_type="graph")
    n1 = pydot.Node("foo.bar", color="red")
    n2 = pydot.Node("baz", color="blue")
    g.add_node(n1)
    g.add_node(n2)
    g.add_edge(pydot.Edge(n1, n2))

    assert g.to_string() == textwrap.dedent("""\
            graph issue418 {
            "foo.bar" [color=red];
            baz [color=blue];
            "foo.bar" -- baz;
            }
            """)


def test_edge_quoting() -> None:
    """Test the fix for issue #383 (pydot 3.0.0)."""
    g = pydot.Graph("", graph_type="digraph")
    g.add_node(pydot.Node("Node^A"))
    g.add_node(pydot.Node("Node^B"))
    g.add_edge(pydot.Edge("Node^A", "Node^B"))
    assert g.to_string() == textwrap.dedent("""\
        digraph {
        "Node^A";
        "Node^B";
        "Node^A" -> "Node^B";
        }
        """)


def test_id_storage_and_lookup() -> None:
    g = pydot.Graph()
    a = pydot.Node("my node")
    b = pydot.Node('"node B"')
    e = pydot.Edge(a, b)

    g.add_node(a)
    g.add_node(b)
    g.add_edge(e)

    a_out = g.get_node("my node")[0]
    b_out = g.get_node('"node B"')[0]
    assert g.get_node("node B") == []
    assert id(a_out.obj_dict) == id(a.obj_dict)
    assert id(b_out.obj_dict) == id(b.obj_dict)

    e_out = g.get_edge("my node", '"node B"')[0]
    assert id(e_out.obj_dict) == id(e.obj_dict)

    sg = pydot.Subgraph("sub graph", graph_type="graph")
    sgA = pydot.Node("sg A")
    sgB = pydot.Node('"sg B"')
    sg.add_node(sgA)
    sg.add_node(sgB)
    g.add_subgraph(sg)

    sg_out = g.get_subgraph("sub graph")[0]
    assert id(sg_out.obj_dict) == id(sg.obj_dict)

    g_nodes_out = g.get_nodes()
    assert id(g_nodes_out[0].obj_dict) == id(a.obj_dict)
    assert id(g_nodes_out[1].obj_dict) == id(b.obj_dict)

    g_edges_out = g.get_edges()
    assert id(g_edges_out[0].obj_dict) == id(e.obj_dict)

    g_sg_out = g.get_subgraphs()
    assert id(g_sg_out[0].obj_dict) == id(sg.obj_dict)

    sg_nodes_out = sg.get_nodes()
    assert id(sg_nodes_out[0].obj_dict) == id(sgA.obj_dict)
    assert id(sg_nodes_out[1].obj_dict) == id(sgB.obj_dict)
    assert sg.get_edges() == []


def test_dot_args() -> None:
    g = pydot.Dot()
    u = pydot.Node("a")
    g.add_node(u)
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
        outfile = os.path.join(tmp_dir, "test.svg")
        g.write_svg(outfile, prog=["twopi", "-Goverlap=scale"])
        assert os.path.exists(outfile)


def test_suppress_disconnected() -> None:
    g1 = pydot.graph_from_dot_data(
        "graph G { a; b; a -- b; c; d; a -- c; b -- c; e; }"
    )
    assert g1 is not None
    gr1 = g1[0]
    g2 = pydot.graph_from_dot_data(
        "graph G { a; b; a -- b; c; a -- c; b -- c; }"
    )
    assert g2 is not None
    gr2 = g2[0]
    gr1.set_suppress_disconnected(True)
    assert gr1.to_string() == gr2.to_string()


def test_strict(objdict: T.Dict[str, T.Any]) -> None:
    g = pydot.Dot(obj_dict=objdict)
    g.set_parent_graph(g)
    g.set_strict(True)
    s = g.to_string()
    assert s == "strict graph G {\n3;\n16;\n}\n"


def test_edge_equality_basics_3_same_points_not_not_equal() -> None:
    # Fail example: pydot 1.4.1 on Python 2.
    g = pydot.Graph()
    e1 = pydot.Edge("a", "b")
    e2 = pydot.Edge("a", "b")
    g.add_edge(e1)
    g.add_edge(e2)
    assert (e1 != e2) is False


def test_edge_point_namestr(graph_directed: pydot.Graph) -> None:
    graph_directed.add_edge(pydot.Edge("a", "b"))
    assert graph_directed.get_edges()[0].to_string() == "a -> b;"


def test_edge_point_object_node(graph_directed: pydot.Graph) -> None:
    graph_directed.add_edge(pydot.Edge(pydot.Node("a"), pydot.Node("b")))
    assert graph_directed.get_edges()[0].to_string() == "a -> b;"


def test_edge_point_object_subgraph(graph_directed: pydot.Graph) -> None:
    graph_directed.add_edge(
        pydot.Edge(pydot.Subgraph("a"), pydot.Subgraph("b"))
    )
    assert graph_directed.get_edges()[0].to_string() == "a -> b;"


def test_edge_point_object_cluster(graph_directed: pydot.Graph) -> None:
    graph_directed.add_edge(pydot.Edge(pydot.Cluster("a"), pydot.Cluster("b")))
    assert (
        graph_directed.get_edges()[0].to_string() == "cluster_a -> cluster_b;"
    )


def test_graph_from_adjacency_matrix() -> None:
    g = pydot.graph_from_adjacency_matrix(
        [[0, 1, 0], [1, 0, 0], [0, 1, 1]], directed=True
    )
    s = " ".join(g.to_string().split())
    assert s == "digraph G { 1 -> 2; 2 -> 1; 3 -> 2; 3 -> 3; }"

    g = pydot.graph_from_adjacency_matrix(
        [[0, 1, 0], [1, 0, 0], [0, 0, 1]], directed=False
    )
    s = " ".join(g.to_string().split())
    assert s == "graph G { 1 -- 2; 3 -- 3; }"


def test_graph_from_incidence_matrix() -> None:
    g = pydot.graph_from_incidence_matrix(
        [[-1, 1, 0], [1, -1, 0], [0, 1, -1]], directed=True
    )
    s = " ".join(g.to_string().split())
    assert s == "digraph G { 1 -> 2; 2 -> 1; 3 -> 2; }"

    g = pydot.graph_from_incidence_matrix(
        [[1, 1, 0], [0, 1, 1]], directed=False
    )
    s = " ".join(g.to_string().split())
    assert s == "graph G { 1 -- 2; 2 -- 3; }"


def test_version() -> None:
    assert isinstance(pydot.__version__, str)
