"""Node and Edge pure-logic behaviour (pydot.core).

No Graphviz binary is involved anywhere here: only object construction,
attribute handling and DOT string rendering are exercised.
"""

import pytest

import pydot
from pydot import Edge, Graph, Node


def test_node_default_name_and_string():
    node = Node()
    assert node.get_name() == ""
    assert str(node) == '"";'


def test_node_attributes_round_trip():
    node = Node("a", color="red", shape="box")
    assert node.get("color") == "red"
    assert node.get("shape") == "box"
    assert node.get("missing") is None
    assert node.get_attributes() == {"color": "red", "shape": "box"}
    assert str(node) == "a [color=red, shape=box];"


def test_node_set_overwrites_and_get_missing_is_none():
    node = Node("a")
    node.set("label", "hi")
    assert node.get("label") == "hi"
    node.set("label", "bye")
    assert node.get("label") == "bye"


def test_node_add_style_accumulates_comma_separated():
    node = Node("b")
    node.add_style("filled")
    assert node.get("style") == "filled"
    node.add_style("dashed")
    assert node.get("style") == "filled,dashed"


def test_node_int_name_is_stringified():
    node = Node(5)
    assert node.get_name() == "5"
    assert node.to_string() == "5;"


def test_node_port_split_and_port_not_emitted():
    # Quirk (current behaviour): the port is stored and readable via
    # get_port(), but Node.to_string() never emits it.
    node = Node("a:port1")
    assert node.get_name() == "a"
    assert node.get_port() == ":port1"
    assert node.to_string() == "a;"
    assert Node("a:port1", color="red").to_string() == "a [color=red];"


def test_node_port_is_none_without_colon():
    assert Node("a").get_port() is None


def test_node_quoted_name_is_not_split_on_colon():
    node = Node('"a:b"')
    assert node.get_name() == '"a:b"'
    assert node.get_port() is None
    assert node.to_string() == '"a:b";'


def test_node_colon_at_edge_is_not_a_port():
    assert Node("a:").get_name() == "a:"
    assert Node("a:").get_port() is None
    assert Node(":a").get_name() == ":a"
    assert Node(":a").get_port() is None


def test_node_set_name_keeps_old_port():
    # Quirk (current behaviour): set_name() replaces the name but leaves
    # the previously parsed port in place.
    node = Node("a:port")
    node.set_name("z")
    assert node.get_name() == "z"
    assert node.get_port() == ":port"


def test_node_keyword_name_is_quoted_in_output():
    # Node names graph/node/edge are the defaults mechanism: they are
    # emitted unquoted when they carry attributes, and as "" when bare.
    assert Node("graph", color="red").to_string() == "graph [color=red];"
    assert Node("graph").to_string() == ""


def test_node_named_node_edge_or_graph_with_attrs_is_emitted():
    # A bare default pseudo-node (name node/edge/graph, no attributes)
    # renders as "" so it contributes no line; with attributes it does.
    assert Node("node", shape="box").to_string() == "node [shape=box];"
    assert Node("node").to_string() == ""


def test_node_indent_and_attrs_string():
    node = Node("a", color="red")
    assert node.to_string(indent="  ", indent_level=2) == "    a [color=red];"
    assert node.attrs_string() == "[color=red]"
    assert node.attrs_string(prefix=" ") == " [color=red]"
    assert node.formatted_attr_list() == ["color=red"]


def test_node_sequence_default_and_set():
    node = Node("n")
    assert node.get_sequence() is None
    node.set_sequence(7)
    assert node.get_sequence() == 7


def test_node_parent_and_top_type_defaults():
    node = Node("n")
    assert node.get_parent_graph() is None
    assert node.get_top_graph_type() == "graph"


def test_node_equality_is_identity():
    assert Node("a") != Node("a")
    node = Node("a")
    assert node == node


def test_node_generated_attribute_methods():
    node = Node("a")
    node.set_shape("box")
    node.set_color("red")
    assert node.get_shape() == "box"
    assert node.get_color() == "red"
    assert node.get_label() is None
    with pytest.raises(AttributeError):
        node.set_nonexistent_attr("x")


def test_edge_endpoints_and_string_undirected_by_default():
    edge = Edge("a", "b", color="blue")
    assert edge.get_source() == "a"
    assert edge.get_destination() == "b"
    # Without a parent graph the top type defaults to "graph", hence "--".
    assert str(edge) == "a -- b [color=blue];"


def test_edge_int_endpoints():
    edge = Edge(1, 2)
    assert edge.get_source() == 1
    assert edge.get_destination() == 2
    assert str(edge) == "1 -- 2;"


def test_edge_node_object_endpoints():
    edge = Edge(Node("x"), Node("y"))
    assert edge.get_source() == "x"
    assert edge.get_destination() == "y"


def test_edge_src_dst_kwargs():
    edge = Edge(src="s", dst="d")
    assert edge.get_source() == "s"
    assert edge.get_destination() == "d"


def test_edge_ports_preserved_verbatim():
    edge = Edge("a:p1", "b:p2")
    assert edge.get_source() == "a:p1"
    assert edge.get_destination() == "b:p2"
    assert edge.to_string() == "a:p1 -- b:p2;"
    assert Edge("a:port:compass", "b").get_source() == "a:port:compass"


def test_edge_arrow_follows_parent_graph_type():
    graph = Graph("G", graph_type="digraph")
    edge = Edge("a", "b")
    graph.add_edge(edge)
    assert str(edge) == "a -> b;"
    assert edge.get_top_graph_type() == "digraph"


def test_edge_equality_ignores_attributes():
    assert Edge("a", "b") == Edge("a", "b", color="red")
    assert Edge("a", "b") != Edge("a", "c")


def test_edge_equality_reversed_depends_on_directedness():
    # Standalone edges default to undirected: reversed endpoints are equal.
    assert Edge("a", "b") == Edge("b", "a")
    graph = Graph("G", graph_type="digraph")
    graph.add_edge(Edge("a", "b"))
    graph.add_edge(Edge("b", "a"))
    first, second = graph.get_edge_list()
    assert first != second
    assert first == Edge("a", "b")


def test_edge_equality_with_non_edge_raises():
    with pytest.raises(pydot.Error, match="Can not compare"):
        Edge("a", "b") == "nope"


def test_edge_hash_is_endpoint_symmetric():
    assert hash(Edge("a", "b")) == hash(Edge("b", "a"))


def test_edge_parse_node_ref():
    edge = Edge("a", "b")
    assert edge.parse_node_ref("a:b") == "a:b"
    assert edge.parse_node_ref('"a b"') == '"a b"'
    assert edge.parse_node_ref("a b") == '"a b"'
    assert edge.parse_node_ref("a") == "a"
    assert edge.parse_node_ref("a:port:compass") == "a:port:compass"


def test_edge_generated_attribute_methods():
    edge = Edge("a", "b")
    edge.set_style("dashed")
    assert edge.get_style() == "dashed"
