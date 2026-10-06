# SPDX-FileCopyrightText: 2026 pydot contributors
#
# SPDX-License-Identifier: MIT
"""Comma-separated node lists are unrolled into discoverable objects."""

from __future__ import annotations

import subprocess

import pytest

import pydot


@pytest.mark.parametrize("graph_type", ["graph", "digraph"])
def test_comma_nodes_are_individually_discoverable(graph_type: str) -> None:
    (graph,) = pydot.graph_from_dot_data(
        f"{graph_type} G {{ a, b, c [color=red]; }}"
    )
    assert {node.get_name() for node in graph.get_nodes()} == {"a", "b", "c"}
    for name in ("a", "b", "c"):
        assert graph.get_node(name)[0].get_attributes() == {"color": "red"}


@pytest.mark.parametrize(
    "graph_type,operator", [("graph", "--"), ("digraph", "->")]
)
def test_comma_edge_chain_is_unrolled(graph_type: str, operator: str) -> None:
    (graph,) = pydot.graph_from_dot_data(
        f"{graph_type} G {{ a {operator} b, c {operator} d [penwidth=5]; }}"
    )
    edges = graph.get_edges()
    assert {(e.get_source(), e.get_destination()) for e in edges} == {
        ("a", "b"),
        ("a", "c"),
        ("b", "d"),
        ("c", "d"),
    }
    assert all(e.get_attributes() == {"penwidth": "5"} for e in edges)
    assert len(graph.get_edge("a", "c")) == 1


@pytest.mark.parametrize(
    "graph_type,operator", [("graph", "--"), ("digraph", "->")]
)
def test_lists_on_each_side_of_edge_chain(
    graph_type: str, operator: str
) -> None:
    (graph,) = pydot.graph_from_dot_data(
        f"{graph_type} G {{ a, b {operator} c, d {operator} e, f "
        "[color=red][penwidth=5]; }"
    )
    expected = [
        (source, destination)
        for sources, destinations in [("ab", "cd"), ("cd", "ef")]
        for source in sources
        for destination in destinations
    ]
    actual = [(e.get_source(), e.get_destination()) for e in graph.get_edges()]
    assert actual == expected
    assert all(
        edge.get_attributes() == {"color": "red", "penwidth": "5"}
        for edge in graph.get_edges()
    )
    assert graph.get_subgraphs() == []
    (roundtrip,) = pydot.graph_from_dot_data(graph.to_string())
    assert roundtrip.to_string() == graph.to_string()


def test_list_node_names_and_attributes_preserve_commas() -> None:
    (graph,) = pydot.graph_from_dot_data(
        'digraph { "a,b", <c,d>, plain [label="x,y"][color=red]; }'
    )
    assert [node.get_name() for node in graph.get_nodes()] == [
        '"a,b"',
        "<c,d>",
        "plain",
    ]
    assert all(
        node.get_attributes() == {"label": '"x,y"', "color": "red"}
        for node in graph.get_nodes()
    )


def test_edge_lists_preserve_quoted_ids_and_ports() -> None:
    (graph,) = pydot.graph_from_dot_data(
        'digraph { "a,b":out:sw, c:in -> d:n, "e,f":port; }'
    )
    actual = [(e.get_source(), e.get_destination()) for e in graph.get_edges()]
    assert actual == [
        ('"a,b":out:sw', "d:n"),
        ('"a,b":out:sw', '"e,f":port'),
        ("c:in", "d:n"),
        ("c:in", '"e,f":port'),
    ]


def test_lists_allow_comments_and_statements_without_semicolons() -> None:
    (graph,) = pydot.graph_from_dot_data(
        "digraph { a, /* separated */ b [color=red]\n"
        "c, d -> e, // list continues\n f [style=dashed] }"
    )
    assert [n.get_name() for n in graph.get_nodes()] == ["a", "b"]
    assert len(graph.get_edges()) == 4
    assert all(e.get("style") == "dashed" for e in graph.get_edges())


@pytest.mark.parametrize("subgraph", ["{c; d;}", "subgraph S {c; d;}"])
def test_lists_do_not_flatten_subgraph_endpoints(subgraph: str) -> None:
    (graph,) = pydot.graph_from_dot_data(
        f"digraph {{ a, b -> {subgraph} -> e, f [color=red]; }}"
    )
    edges = graph.get_edges()
    assert len(edges) == 4
    assert [e.get_source() for e in edges[:2]] == ["a", "b"]
    assert all(isinstance(e.get_destination(), dict) for e in edges[:2])
    assert all(isinstance(e.get_source(), dict) for e in edges[2:])
    assert [e.get_destination() for e in edges[2:]] == ["e", "f"]
    assert all(e.get_attributes() == {"color": "red"} for e in edges)


def test_repeated_list_endpoints_preserve_parallel_edges() -> None:
    (graph,) = pydot.graph_from_dot_data(
        "digraph { a, a -> b, b [color=red]; }"
    )
    assert len(graph.get_edge("a", "b")) == 4


def test_list_nodes_have_independent_attributes() -> None:
    (graph,) = pydot.graph_from_dot_data("graph { a, b [color=red]; }")
    graph.get_node("a")[0].set("color", "blue")
    assert graph.get_node("b")[0].get("color") == "red"


@pytest.mark.parametrize(
    "graph_type,operator", [("graph", "--"), ("digraph", "->")]
)
def test_existing_unrolled_and_quoted_comma_control(
    graph_type: str, operator: str
) -> None:
    (graph,) = pydot.graph_from_dot_data(
        f"{graph_type} G {{ a [color=red]; b [color=red]; "
        f"c [color=red]; a {operator} b; b {operator} c; "
        '"comma,node" [color=blue]; }'
    )
    assert len(graph.get_edges()) == 2
    assert graph.get_node('"comma,node"')[0].get_attributes() == {
        "color": "blue"
    }


@pytest.mark.parametrize(
    "source,expected_edges",
    [
        ("graph G { a, b, c [color=red]; }", 0),
        ("graph G { a -- b, c -- d [penwidth=5]; }", 4),
    ],
)
def test_installed_graphviz_accepts_comma_syntax(
    source: str, expected_edges: int
) -> None:
    result = subprocess.run(
        ["dot", "-Tcanon"],
        input=source,
        text=True,
        capture_output=True,
        check=True,
        timeout=10,
    )
    (graph,) = pydot.graph_from_dot_data(result.stdout)
    assert len(graph.get_edges()) == expected_edges
    if expected_edges == 0:
        for name in ("a", "b", "c"):
            assert graph.get_node(name)[0].get_attributes() == {"color": "red"}
