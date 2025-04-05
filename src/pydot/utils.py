# SPDX-FileCopyrightText: 2025 pydot contributors
#
# SPDX-License-Identifier: MIT

"""Utility functions for string processing."""

import re
import typing as T

from pydot.constants import DOT_KEYWORDS, ID_QUOTED_CHARS

re_numeric = re.compile(r"^-?([0-9]+\.?[0-9]*|[0-9]*\.[0-9]+)$")
re_dbl_quoted = re.compile(r'^".*"$', re.S)
re_html = re.compile(r"^<.*>$", re.S)

id_re_alpha_nums = re.compile(r"^[_a-zA-Z][a-zA-Z0-9_]*$")
id_re_alpha_nums_with_ports = re.compile(
    r'^[_a-zA-Z][a-zA-Z0-9_:"]*[a-zA-Z0-9_"]+$'
)
id_re_with_port = re.compile(r"^([^:]*):([^:]*)$")


def possibly_unquoted(identifier: str) -> str:
    """Produce the unquoted version of an identifier, if safe.

    An 'unsafe' identifier which can't be unquoted, in this context,
    means any keyword, HTML-like string in quotes, string containing
    inner quotes, or a string containing non-ASCII characters."""
    if not (identifier.startswith('"') and identifier.endswith('"')):
        return identifier
    unquoted: str = identifier[1:-1]
    if any([
        unquoted.startswith("<"),
        unquoted.endswith(">"),
        unquoted.lower() in DOT_KEYWORDS,
        any(unquoted.find(c) >= 0 for c in ID_QUOTED_CHARS),
    ]):
        return identifier
    if unquoted.isascii():
        return unquoted
    return identifier


def make_quoted(s: str) -> str:
    """Transform a string into a quoted string, escaping internal quotes."""
    out = s.replace('"', r"\"")
    return f'"{out}"'


def any_needs_quotes(s: str) -> T.Optional[bool]:
    """Determine if a string needs to be quoted.

    Returns True, False, or None if the result is indeterminate.
    """

    # Strings consisting _only_ of digits are safe unquoted
    if s.isdigit():
        return False

    # MIXED-aphanumeric values need quoting if they *start* with a digit
    if s.isalnum():
        return s[0].isdigit()

    for test_re in [re_numeric, re_dbl_quoted, re_html]:
        if test_re.match(s):
            return False

    has_high_chars = any(ord(c) > 0x7F or ord(c) == 0 for c in s)
    if has_high_chars:
        return True

    return None


def id_needs_quotes(s: str) -> bool:
    """Checks whether a string is a dot language ID.

    It will check whether the string is solely composed
    by the characters allowed in an ID or not.
    If the string is one of the reserved keywords it will
    need quotes too but the user will need to add them
    manually.
    """

    # If the name is a reserved keyword it will need quotes but pydot
    # can't tell when it's being used as a keyword or when it's simply
    # a name. Hence the user needs to supply the quotes when an element
    # would use a reserved keyword as name. This function will return
    # false indicating that a keyword string, if provided as-is, won't
    # need quotes.
    if s.lower() in DOT_KEYWORDS:
        return False

    any_result = any_needs_quotes(s)
    if any_result is not None:
        return any_result

    for test_re in [
        id_re_alpha_nums,
        id_re_alpha_nums_with_ports,
    ]:
        if test_re.match(s):
            return False

    m = id_re_with_port.match(s)
    if m:
        return id_needs_quotes(m.group(1)) or id_needs_quotes(m.group(2))

    return True


def quote_id_if_necessary(
    s: str, unquoted_keywords: T.Optional[T.Sequence[str]] = None
) -> str:
    """Enclose identifier in quotes, if needed."""
    unquoted = [
        w.lower() for w in list(unquoted_keywords if unquoted_keywords else [])
    ]

    if isinstance(s, bool):
        return str(s).lower()
    if not isinstance(s, str):
        return s
    if not s:
        return s

    if s.lower() in unquoted:
        return s
    if s.lower() in DOT_KEYWORDS:
        return make_quoted(s)

    if id_needs_quotes(s):
        return make_quoted(s)

    return s


def quote_attr_if_necessary(s: str) -> str:
    """Enclose attribute value in quotes, if needed."""
    if isinstance(s, bool):
        return str(s).lower()

    if not isinstance(s, str):
        return s

    if s.lower() in DOT_KEYWORDS:
        return make_quoted(s)

    any_result = any_needs_quotes(s)
    if any_result is not None and not any_result:
        return s

    return make_quoted(s)


def format_for_lookup(s: str) -> T.List[str]:
    """Return a list of the possible lookup forms of an identifier."""
    if re_html.match(s):
        return [s]
    if re_dbl_quoted.match(s):
        return list({possibly_unquoted(s), s})
    return [s, f'"{s}"']
