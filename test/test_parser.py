# SPDX-FileCopyrightText: 2025 pydot contributors
#
# SPDX-License-Identifier: MIT

"""Unit testing of individual dot_parser classes."""

import textwrap

import pyparsing as pp
import pytest

from pydot import dot_parser
from pydot.dot_parser import HTML, GraphParser


def test_HTML_valid() -> None:
    """Test successful HTML parses."""
    parsed = HTML().parse_string("<<b>Bold Text</b>>")
    assert isinstance(parsed, pp.ParseResults)
    assert list(parsed) == ["<<b>Bold Text</b>>"]

    parsed2 = HTML().parse_string("<Label #1>")
    assert isinstance(parsed2, pp.ParseResults)
    assert list(parsed2) == ["<Label #1>"]


def test_HTML_invalid() -> None:
    """Test HTML parsing failure."""
    with pytest.raises(pp.ParseException) as exc:
        HTML().parse_string("<<b>Unbalanced tags</b>")
    assert "HTML: expected '>' to match '<' on line 1" in str(exc.value)


def test_edge_subgraph_anon() -> None:
    """Test parsing of an edge with an anonymous subgraph endpoint."""
    parser = GraphParser.edge_stmt
    res = parser.parse_string("""a -- { b; c; }""")
    assert len(res) == 1
    edge = res[0]
    expected = textwrap.dedent("""
        a -- {
        b;
        c;
        };""").strip()
    assert edge.to_string() == expected


def test_edge_subgraph_explicit() -> None:
    """Test parsing of an edge with an explicit subgraph endpoint."""
    parser = GraphParser.edge_stmt
    res = parser.parse_string("""a -- subgraph XY { b; c; }""")
    assert len(res) == 1
    edge = res[0]
    expected = textwrap.dedent("""
        a -- subgraph XY {
        b;
        c;
        };""").strip()
    assert edge.to_string() == expected


def test_AttrList_repr() -> None:
    parser = GraphParser.attr_list("a_list")
    res = parser.parse_string("[color=red, shape=square]")
    assert isinstance(res, pp.ParseResults)
    a_list = res.a_list
    assert isinstance(a_list, pp.ParseResults)
    assert len(a_list) == 1
    repr_str = repr(a_list[0])
    assert repr_str == "P_AttrList({'color': 'red', 'shape': 'square'})"


def test_DefaultStatement_repr() -> None:
    parser = GraphParser.default_stmt("defaults")
    res = parser.parse_string("node [color=blue];")
    assert isinstance(res, pp.ParseResults)
    defaults = res.defaults
    repr_str = repr(defaults)
    assert repr_str == "DefaultStatement(node, {'color': 'blue'})"


def test_strict_graph_parsing() -> None:
    res = dot_parser.parse_dot_data("strict graph G { a; b; }")
    assert isinstance(res, list)
    assert len(res) == 1
    graph = res[0]
    assert graph.get_strict()
    assert graph.to_string() == "strict graph G {\na;\nb;\n}\n"

    res2 = dot_parser.parse_dot_data(
        """
        graph G { a; b; }
        strict digraph H { c; d; }
        """
    )
    assert isinstance(res2, list)
    assert len(res2) == 2
    assert not res2[0].get_strict()
    assert res2[1].get_strict()


def test_backslash_continuations() -> None:
    src = textwrap.dedent(r"""
        graph G {
            "my very long node \
        name" [color=red];
            "my indented and wrapped \
            node name" [shape=square];
            "my node name containing \ backslash";
        }""")
    res = dot_parser.parse_dot_data(src)
    assert isinstance(res, list)
    assert len(res) == 1
    graph = res[0]
    nodes = graph.get_nodes()
    assert len(nodes) == 3
    assert nodes[0].get_name() == '"my very long node name"'
    assert nodes[1].get_name() == '"my indented and wrapped     node name"'
    assert nodes[2].get_name() == '"my node name containing \\ backslash"'


def test_plus_concatenation() -> None:
    src = textwrap.dedent(r"""
        digraph G {
            "my" + "concatenated" + "name";
            "myconcatenated" + " with " + "ports" [color="r" + "ed"];
            "my\
        concatenated" + " with ports":p45:sw -> "my\
        concatenated\
        name":ne [penwidth=5, arrows="b" + "o" + "t" + "h"];
        "con" + "catenated" [label="this is a long\
        long label" + " that just goes on \
        and on and on"];
        }""")
    res = dot_parser.parse_dot_data(src)
    assert isinstance(res, list)
    assert len(res) == 1
    graph = res[0]
    nodes = graph.get_nodes()
    edges = graph.get_edges()

    assert len(nodes) == 3
    assert nodes[0].get_name() == '"myconcatenatedname"'
    assert nodes[1].get_name() == '"myconcatenated with ports"'
    assert nodes[1].get("color") == '"red"'
    assert nodes[2].get_name() == '"concatenated"'
    assert nodes[2].get("label") == (
        '"this is a longlong label that just goes on and on and on"'
    )

    assert len(edges) == 1
    edge = edges[0]
    assert edge.get_source() == f"{nodes[1].get_name()}:p45:sw"
    assert edge.get_destination() == '"myconcatenatedname":ne'
    assert edge.get("arrows") == '"both"'
