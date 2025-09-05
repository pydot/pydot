# SPDX-FileCopyrightText: 2024 pydot contributors
#
# SPDX-License-Identifier: MIT

"""Graphviz's dot language parser.

The dotparser parses GraphViz files in
dot and dot files and transforms them
into a class representation defined by `pydot`.

Author: Michael Krause <michael@krause-software.de>
Fixes by: Ero Carrera <ero.carrera@gmail.com>
"""

from __future__ import annotations

import logging
from functools import cached_property
from typing import Any

from pyparsing import (
    CaselessLiteral,
    Combine,
    DelimitedList,
    Forward,
    Group,
    Literal,
    OneOrMore,
    Optional,
    ParseException,
    ParserElement,
    ParseResults,
    QuotedString,
    Suppress,
    Token,
    Word,
    autoname_elements,
    cStyleComment,
    lineno,
    nums,
    restOfLine,
    unicode,
)

import pydot.core
from pydot.classes import FrozenDict

__author__ = ["Michael Krause", "Ero Carrera"]
__license__ = "MIT"


_logger = logging.getLogger(__name__)
_logger.debug("pydot dot_parser module initializing")


class P_AttrList:
    def __init__(self, toks: ParseResults) -> None:
        self.attrs = {}
        i = 0

        while i < len(toks):
            attrname = toks[i]
            if i + 2 < len(toks) and toks[i + 1] == "=":
                attrvalue = toks[i + 2]
                i += 3
            else:
                attrvalue = None
                i += 1

            self.attrs[attrname] = attrvalue

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"{name}({self.attrs!r})"


class DefaultStatement(P_AttrList):
    def __init__(self, default_type: str, attrs: Any) -> None:
        self.default_type = default_type
        self.attrs = attrs

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"{name}({self.default_type}, {self.attrs!r})"


class HTML(Token):
    """Parsing for HTML-like strings."""

    def __init__(self) -> None:
        super().__init__()

    def parseImpl(
        self, instring: str, loc: int, do_actions: bool = True
    ) -> tuple[int, str]:
        open_loc = loc
        if not (loc < len(instring) and instring[loc] == "<"):
            raise ParseException(instring, loc, "expected <", self)
        num_open = 1
        loc += 1
        while loc < len(instring):
            if instring[loc] == "<":
                num_open += 1
            elif instring[loc] == ">":
                num_open -= 1
            loc += 1
            if num_open == 0:
                return loc, instring[open_loc:loc]
        raise ParseException(
            instring,
            loc,
            "HTML: expected '>' to match '<' "
            + f"on line {lineno(open_loc, instring)}",
            self,
        )


class GraphParser:
    """Pyparsing grammar for graphviz 'dot' syntax."""

    def push_top_graph_stmt(self, toks: ParseResults) -> list[pydot.core.Dot]:
        top_graphs = []

        for result in toks.graphs:
            assert isinstance(result, ParseResults)
            gtype = result.gtype
            strict = "strict" in result
            id_ = str(result.id)

            g = pydot.core.Dot(id_, graph_type=gtype, strict=strict)
            g.set_parent_graph(g)
            if isinstance(result.contents, ParseResults):
                self.add_elements(g, result.contents)
            self.update_parent_graph_hierarchy(g)
            top_graphs.append(g)

        return top_graphs

    def update_parent_graph_hierarchy(self, g: pydot.core.Dot) -> None:
        for edge_groups in g.obj_dict.get("edges", {}).values():
            for edge in edge_groups:
                assert isinstance(edge, dict)
                endpoints = edge.get("points", [])
                for ep in endpoints:
                    if isinstance(ep, FrozenDict):
                        ep["parent_graph"].set_parent_graph(g)

    def add_elements(self, g: Any, toks: ParseResults) -> None:
        for element in toks:
            if isinstance(element, (pydot.core.Subgraph, pydot.core.Cluster)):
                g.add_subgraph(element)
            elif isinstance(element, pydot.core.Node):
                g.add_node(element)
            elif isinstance(element, pydot.core.Edge):
                g.add_edge(element)
            elif isinstance(element, ParseResults):
                self.add_elements(g, element)
            elif isinstance(element, DefaultStatement):
                default_node = pydot.core.Node(
                    element.default_type, **element.attrs
                )
                g.add_node(default_node)
            else:
                assert isinstance(element, P_AttrList)
                g.obj_dict["attributes"].update(element.attrs)

    def expand_attr_lists(self, attr_l: Any) -> dict[str, Any]:
        if not isinstance(attr_l, ParseResults):
            return {}
        attrs = {}
        for alist in attr_l:
            attrs.update(alist.attrs)
        return attrs

    def push_dbl_quoted(self, toks: ParseResults) -> str:
        assert "dbl_quoted" in toks and isinstance(toks.dbl_quoted, str)
        s = toks.dbl_quoted
        # Remove backslash line-continuations
        if "\\" in s:
            s = s.replace("\\\r\n", "").replace("\\\n", "")
        return s

    def push_ID(self, toks: ParseResults) -> str:
        """Join multiple string pieces into a single ID string."""
        if "concat" in toks:
            out = "".join(s[1:-1] for s in toks.concat)
            return f'"{out}"'
        if "dbl_quoted" in toks:
            return str(toks.dbl_quoted)
        if "ident" in toks:
            return str(toks.ident)
        # (by process of elimination, HTML)
        assert "html" in toks and isinstance(toks.html, str)
        return toks.html

    def push_node_id(self, toks: ParseResults) -> str:
        out = []
        for group in toks:
            assert "id_part" in group
            out.append(str(group.id_part))
        return ":".join(out)

    def push_graph_stmt(self, toks: ParseResults) -> pydot.core.Subgraph:
        g = pydot.core.Subgraph("")
        g.obj_dict["show_keyword"] = False
        self.add_elements(g, toks)
        return g

    def push_subgraph_stmt(self, toks: ParseResults) -> pydot.core.Subgraph:
        assert "keyword" in toks
        id_ = str(toks.id)
        show_kw = "keyword" in toks
        g = pydot.core.Subgraph(id_)
        g.obj_dict["show_keyword"] = show_kw
        if isinstance(toks.contents, ParseResults):
            self.add_elements(g, toks.contents)
        return g

    def push_default_stmt(self, toks: ParseResults) -> DefaultStatement:
        default_type = toks.dtype
        attrs = self.expand_attr_lists(toks.attr_l)
        return DefaultStatement(str(default_type), attrs)

    def push_attr_list(self, toks: ParseResults) -> P_AttrList:
        p = P_AttrList(toks)
        return p

    def push_edge_stmt(self, toks: ParseResults) -> list[pydot.core.Edge]:
        endpoints = list(toks.endpoints)
        attrs = self.expand_attr_lists(toks.attr_l)

        def make_endpoint(
            ep: pydot.core.Common | list[Any] | str,
        ) -> FrozenDict | str:
            if isinstance(ep, pydot.core.Subgraph):
                return FrozenDict(ep.obj_dict)
            return str(ep)

        edges = []
        n_prev = make_endpoint(endpoints[0])
        for endpoint in endpoints[1:]:
            n_next = make_endpoint(endpoint)
            edges.append(pydot.core.Edge(n_prev, n_next, **attrs))
            n_prev = n_next
        return edges

    def push_node_stmt(self, toks: ParseResults) -> pydot.core.Node:
        node_name = toks.name
        attrs = self.expand_attr_lists(toks.attr_l)
        return pydot.core.Node(str(node_name), **attrs)

    def __init__(self) -> None:
        # keywords
        self.strict_ = CaselessLiteral("strict")
        self.graph_ = CaselessLiteral("graph")
        self.digraph_ = CaselessLiteral("digraph")
        self.subgraph_ = CaselessLiteral("subgraph")
        self.node_ = CaselessLiteral("node")
        self.edge_ = CaselessLiteral("edge")

        # token definitions
        self.identifier = Word(unicode.BasicMultilingualPlane.alphanums + "_.")

        self.double_quoted = (
            QuotedString(
                '"', multiline=True, unquote_results=False, esc_char="\\"
            )
            .set_results_name("dbl_quoted")
            .set_parse_action(self.push_dbl_quoted)
        )

        self.concat_string = DelimitedList(
            self.double_quoted, delim="+", min=2, combine=False
        )

        self.ID = (
            self.concat_string("concat")
            | self.double_quoted
            | self.identifier("ident")
            | HTML().set_results_name("html")
        ).set_parse_action(self.push_ID)

        self.float_number = Combine(
            Optional("-") + OneOrMore(Word(nums + "."))
        )

        self.righthand_id = self.float_number | self.ID

        self.node_id = DelimitedList(
            Group(self.ID("id_part")), delim=":", min=1, max=3, combine=False
        ).set_parse_action(self.push_node_id)

        self.a_list = OneOrMore(
            self.ID
            + Optional("=" + self.righthand_id)
            + Optional(",").suppress()
        )
        self.attr_list = OneOrMore(
            Suppress("[") + Optional(self.a_list) + Suppress("]")
        )
        self.node_stmt = (
            self.node_id("name")
            + Optional(self.attr_list("attr_l"))
            + Optional(";").suppress()
        )

        self.default_type = self.graph_ | self.node_ | self.edge_
        self.default_stmt = self.default_type("dtype") + self.attr_list(
            "attr_l"
        )

        self.stmt_list = Forward()
        self.graph_stmt = Group(
            Suppress("{")
            + Optional(self.stmt_list)
            + Suppress("}")
            + Optional(";").suppress()
        )

        self.subgraph = (
            self.subgraph_("keyword")
            + Optional(self.ID("id"))
            + self.graph_stmt("contents")
        )

        self.edgeop = Literal("--") | Literal("->")
        self.edge_point = self.subgraph | self.graph_stmt | self.node_id
        self.edge_stmt = DelimitedList(
            self.edge_point, delim=self.edgeop, min=2
        )("endpoints") + Optional(self.attr_list("attr_l"))

        self.assignment = self.ID + "=" + self.righthand_id

        self.stmt = (
            self.assignment
            | self.edge_stmt
            | self.default_stmt
            | self.subgraph
            | self.graph_stmt
            | self.node_stmt
        )
        self.stmt_list <<= OneOrMore(self.stmt + Optional(";").suppress())

        self.graph_type = self.digraph_ | self.graph_
        self.parser = OneOrMore(
            Group(
                Optional(self.strict_("strict"))
                + self.graph_type("gtype")
                + Optional(self.ID("id"))
                + self.graph_stmt("contents")
            )
        ).set_results_name("graphs")

        self.singleLineComment = Group("//" + restOfLine) | Group(
            "#" + restOfLine
        )

        # actions

        self.parser.ignore(self.singleLineComment)
        self.parser.ignore(cStyleComment)
        self.parser.parse_with_tabs()

        self.assignment.setParseAction(self.push_attr_list)
        self.a_list.setParseAction(self.push_attr_list)
        self.edge_stmt.setParseAction(self.push_edge_stmt)
        self.node_stmt.setParseAction(self.push_node_stmt)
        self.default_stmt.setParseAction(self.push_default_stmt)

        self.subgraph.setParseAction(self.push_subgraph_stmt)
        self.graph_stmt.setParseAction(self.push_graph_stmt)
        self.parser.setParseAction(self.push_top_graph_stmt)

        autoname_elements()


def parse_dot_data(s: str) -> list[pydot.core.Dot] | None:
    """Parse DOT description in (unicode) string `s`.

    This function is NOT thread-safe due to the internal use of `pyparsing`.
    Use a lock if needed.

    @return: Graphs that result from parsing.
    @rtype: `list` of `pydot.core.Dot`
    """
    try:
        tokens = GraphParser().parser.parse_string(s)
        return list(tokens)
    except ParseException as err:
        print(err.line)
        print(" " * (err.column - 1) + "^")
        print(err)
        return None


class Legacy:
    """Backwards-compatible holder for legacy module-wide parser handle."""

    @cached_property
    def graphparser(self) -> ParserElement:
        """Create module-global parser instance."""
        return GraphParser().parser


_legacy = Legacy()
graphparser = _legacy.graphparser
