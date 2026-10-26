"""DOT parser behaviour via graph_from_dot_data (pydot.dot_parser).

Parsing and re-serialising are pure logic; no Graphviz binary is used.
"""

import pytest

from pydot import Edge, Graph, Node, Subgraph
from pydot.core import graph_from_dot_data


def parse_one(src):
    graphs = graph_from_dot_data(src)
    assert graphs is not None and len(graphs) == 1
    return graphs[0]


def test_parse_simple_digraph_and_undirected():
    graph = parse_one("digraph G { a -> b; }")
    assert graph.get_graph_type() == "digraph"
    assert graph.to_string() == "digraph G {\na -> b;\n}\n"
    graph = parse_one("graph G { a -- b; }")
    assert graph.to_string() == "graph G {\na -- b;\n}\n"


def test_parse_node_and_edge_attributes():
    graph = parse_one(
        'digraph { rankdir=LR; a [label="hello world"]; b [shape=box];'
        " a -> b [color=red]; }"
    )
    assert graph.to_string() == (
        "digraph {\n"
        "rankdir=LR;\n"
        'a [label="hello world"];\n'
        "b [shape=box];\n"
        "a -> b [color=red];\n"
        "}\n"
    )


def test_parse_chain_expands_to_pairwise_edges():
    graph = parse_one("digraph G { a -> b -> c; }")
    assert [(e.get_source(), e.get_destination()) for e in graph.get_edge_list()] == [
        ("a", "b"),
        ("b", "c"),
    ]


def test_parse_quoted_identifiers_with_spaces():
    graph = parse_one('digraph G { "a b" -> "c d"; }')
    assert graph.to_string() == 'digraph G {\n"a b" -> "c d";\n}\n'


def test_parse_numeric_node_ids():
    graph = parse_one("digraph G { 123 -> 456; }")
    assert graph.to_string() == "digraph G {\n123 -> 456;\n}\n"


def test_parse_ports():
    graph = parse_one("digraph G { a:port -> b; }")
    assert graph.to_string() == "digraph G {\na:port -> b;\n}\n"


def test_parse_comments_are_dropped():
    assert parse_one("digraph G { /* comment */ a -> b; }").to_string() == (
        "digraph G {\na -> b;\n}\n"
    )
    assert parse_one("digraph G { a -> b; // comment\n }").to_string() == (
        "digraph G {\na -> b;\n}\n"
    )


def test_parse_missing_semicolons_ok():
    assert parse_one("digraph G { a -> b }").to_string() == "digraph G {\na -> b;\n}\n"
    assert parse_one("digraph G { a; b; }").to_string() == "digraph G {\na;\nb;\n}\n"


def test_parse_default_statements_land_in_defaults():
    graph = parse_one(
        "digraph G { node [shape=circle]; edge [color=blue];"
        " graph [bgcolor=white]; a; b; }"
    )
    assert graph.get_node_defaults() == [{"shape": "circle"}]
    assert graph.get_edge_defaults() == [{"color": "blue"}]
    assert graph.get_graph_defaults() == [{"bgcolor": "white"}]
    assert graph.to_string() == (
        "digraph G {\n"
        "node [shape=circle];\n"
        "edge [color=blue];\n"
        "graph [bgcolor=white];\n"
        "a;\n"
        "b;\n"
        "}\n"
    )


def test_parse_strict_flag_survives():
    graph = parse_one("strict digraph G { a -> b; a -> b; }")
    assert graph.get_strict() is True
    assert graph.to_string() == "strict digraph G {\na -> b;\na -> b;\n}\n"


def test_parse_subgraph_cluster_preserved():
    graph = parse_one("digraph G { subgraph cluster_0 { a; b; } a -> b; }")
    assert graph.to_string() == (
        "digraph G {\n"
        "subgraph cluster_0 {\na;\nb;\n}\n"
        "a -> b;\n"
        "}\n"
    )


def test_parse_subgraph_endpoint_edges_round_trip():
    left = parse_one("digraph G { subgraph cluster_0 { a; } -> b; }")
    assert left.to_string() == "digraph G {\nsubgraph cluster_0 {\na;\n} -> b;\n}\n"
    right = parse_one("digraph G { a -> subgraph cluster_0 { b; } }")
    assert right.to_string() == "digraph G {\na -> subgraph cluster_0 {\nb;\n};\n}\n"


def test_parse_float_and_int_attribute_values():
    graph = parse_one("digraph G { a [weight=1.5, color=red]; }")
    assert graph.to_string() == "digraph G {\na [weight=1.5, color=red];\n}\n"
    graph = parse_one("digraph G { a -> b [penwidth=2]; }")
    assert graph.to_string() == "digraph G {\na -> b [penwidth=2];\n}\n"


def test_parse_html_label_is_split_into_tokens():
    # Quirk (current behaviour): the parser does not keep an HTML-like
    # label intact; it splits it into separate tokens on re-serialisation.
    graph = parse_one("digraph G { a [label=<b>bold</b>]; }")
    assert graph.to_string() == "digraph G {\na [label=<b>, bold, </b>];\n}\n"


def test_parse_empty_garbage_and_truncated_return_none():
    assert graph_from_dot_data("") is None
    assert graph_from_dot_data("this is not dot {{{") is None
    assert graph_from_dot_data("digraph G { a -> }") is None


def test_parse_bytes_input_raises_type_error():
    with pytest.raises(TypeError):
        graph_from_dot_data(b"digraph G { a -> b; }")


def test_parse_multiple_graphs_returns_list():
    graphs = graph_from_dot_data("digraph A { a; } digraph B { b; }")
    assert graphs is not None and len(graphs) == 2
    assert [g.get_name() for g in graphs] == ["A", "B"]


def test_build_parse_round_trip_is_stable():
    graph = Graph("RT", graph_type="digraph")
    graph.add_node(Node("a", label="hello world", shape="box"))
    graph.add_node(Node("b"))
    graph.add_edge(Edge("a", "b", color="red"))
    graph.add_edge(Edge("b", "a"))
    subgraph = Subgraph("cluster_0")
    subgraph.add_node(Node("c"))
    graph.add_subgraph(subgraph)
    text = graph.to_string()
    reparsed = parse_one(text)
    assert reparsed.to_string() == text


def test_parse_then_mutate_and_reserialise():
    graph = parse_one("digraph G { a -> b; }")
    graph.add_node(Node("c", shape="box"))
    graph.add_edge(Edge("b", "c"))
    assert graph.to_string() == (
        "digraph G {\na -> b;\nc [shape=box];\nb -> c;\n}\n"
    )
