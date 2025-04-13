# SPDX-FileCopyrightText: 2025 pydot contributors
#
# SPDX-License-Identifier: MIT

"""Unit testing of individual dot_parser classes."""

import textwrap

import pyparsing as pp
import pytest

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
