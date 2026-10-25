"""Quoting helpers in pydot.core: make_quoted, any_needs_quotes,
id_needs_quotes, quote_id_if_necessary, quote_attr_if_necessary.

All expectations below were measured by probing the real implementation;
several are quirks, marked as such, and pinned as current behaviour.
"""

import pytest

from pydot.core import (
    any_needs_quotes,
    id_needs_quotes,
    make_quoted,
    quote_attr_if_necessary,
    quote_id_if_necessary,
)


def test_make_quoted_plain():
    assert make_quoted("abc") == '"abc"'


def test_make_quoted_escapes_double_quote():
    assert make_quoted('a"b') == '"a\\"b"'


def test_make_quoted_escapes_newline_and_carriage_return():
    assert make_quoted("a\nb\rc") == '"a\\nb\\rc"'


def test_make_quoted_empty():
    assert make_quoted("") == '""'


@pytest.mark.parametrize(
    "s,expected",
    [
        ("123", False),  # digits only are safe unquoted
        ("abc", False),
        ("a1", False),
        ("1.5", False),  # numeric
        ('"quoted"', False),  # already double-quoted
        ("<b>hi</b>", False),  # HTML-like
        ("a b", None),  # indeterminate: needs a caller decision
        ("a:b", None),
        ("a\nb", None),
    ],
)
def test_any_needs_quotes(s, expected):
    assert any_needs_quotes(s) is expected


def test_any_needs_quotes_digit_start_alnum_is_true():
    assert any_needs_quotes("12a") is True


def test_any_needs_quotes_high_chars_short_circuited_by_isalnum():
    # Quirk (current behaviour): 'café'.isalnum() is True and its first
    # character is not a digit, so the function returns False before the
    # high-character check is ever reached.
    assert any_needs_quotes("café") is False


@pytest.mark.parametrize(
    "s,expected",
    [
        ("abc", False),
        ("a1", False),
        ("a_b", False),
        ("_x", False),
        ("123", False),
        ("1.5", False),
        ("a:b", False),  # port form
        ("a:b:c", False),  # multi-port form
        ("<b>hi</b>", False),
        ('"quoted"', False),
        ("a b", True),
        ("12a", True),
        ("hello-world", True),
        ("a.b", True),
        ("", True),
        ("a\nb", True),
    ],
)
def test_id_needs_quotes(s, expected):
    assert id_needs_quotes(s) is expected


def test_id_needs_quotes_keywords_return_false_by_design():
    # id_needs_quotes deliberately returns False for reserved keywords:
    # callers cannot tell a keyword use from a plain name, so the user is
    # expected to supply quotes. quote_id_if_necessary DOES quote them.
    for kw in ("graph", "digraph", "subgraph", "node", "edge", "strict"):
        assert id_needs_quotes(kw) is False
        assert quote_id_if_necessary(kw) == f'"{kw}"'


@pytest.mark.parametrize(
    "s,expected",
    [
        ("abc", "abc"),
        ("a1", "a1"),
        ("123", "123"),
        ("1.5", "1.5"),
        ("a:b", "a:b"),
        ("a b", '"a b"'),
        ("hello-world", '"hello-world"'),
        ("", '""'),
        ("<b>hi</b>", "<b>hi</b>"),
        ('"quoted"', '"quoted"'),
    ],
)
def test_quote_id_if_necessary(s, expected):
    assert quote_id_if_necessary(s) == expected


def test_quote_id_bool_is_lowercased():
    assert quote_id_if_necessary(True) == "true"
    assert quote_id_if_necessary(False) == "false"


def test_quote_id_non_str_passes_through():
    assert quote_id_if_necessary(5) == 5


def test_quote_id_unquoted_keywords_override():
    assert quote_id_if_necessary("graph", unquoted_keywords=("graph",)) == "graph"
    assert quote_id_if_necessary("graph") == '"graph"'


@pytest.mark.parametrize(
    "s,expected",
    [
        ("abc", "abc"),
        ("red", "red"),
        ("123", "123"),
        ("1.5", "1.5"),
        ("true", "true"),
        ("a b", '"a b"'),
        ("a:b", '"a:b"'),  # attr values, unlike ids, quote ports
        ("graph", '"graph"'),
    ],
)
def test_quote_attr_if_necessary(s, expected):
    assert quote_attr_if_necessary(s) == expected


def test_quote_attr_bool_is_lowercased():
    assert quote_attr_if_necessary(True) == "true"
    assert quote_attr_if_necessary(False) == "false"


def test_quote_attr_non_str_passes_through():
    assert quote_attr_if_necessary(5) == 5
