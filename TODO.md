# pydot contribution candidates (scanned 2026-07-17)

Scope: verified bugs, inaccurate docstrings, and security notes. Every bug and
security item below was reproduced locally, not just eyeballed. Backward
compatibility for existing users takes priority over cleanup or idealized API
behavior.

## To do

- `src/pydot/core.py:1298`, `Graph.del_edge()` — reversed endpoints are ignored
  in undirected graphs, unlike `get_edge()`. After storing `a -- b`,
  `get_edge("b", "a")` finds it but `del_edge("b", "a")` returns `False` and
  deletes nothing. **Fix:** for undirected graphs, fall back to the reversed
  key using the same matching semantics as `get_edge()`; add reversed-endpoint
  deletion cases, including indexed duplicate edges.

- `src/pydot/core.py:1205-1240,1298-1342`, `Graph.del_node()` and
  `Graph.del_edge()` — an out-of-range `index` deletes every matching object,
  despite both docstrings promising no action. Verified with two duplicate
  nodes/edges and `index=99`: both methods returned `True` and left zero
  matches. **Fix:** return `False` when a supplied index is outside the list;
  add node and edge regression cases. This is a small data-loss bug.

- `src/pydot/core.py:863`, `Edge.__eq__()` — comparing an edge with any
  non-`Edge` raises `pydot.Error`, breaking normal Python equality and
  membership operations. For example, `edge == None` and
  `edge in [pydot.Node("a"), matching_edge]` can raise. **Fix:** return
  `NotImplemented` for non-edges. This changes behavior for callers that catch
  the current error, so it needs a deliberate compatibility decision.

- `src/pydot/core.py:798-811`, `Edge.__init__()` — sequence endpoints are
  handled inconsistently. `Edge(["a"])` raises a bare tuple-unpacking
  `ValueError`, while sequences longer than two silently discard extra items;
  a separate `dst` supplied with a sequence `src` is also ignored. **Fix:**
  define and validate exactly which sequence forms are accepted, then raise
  `pydot.Error` consistently for invalid endpoint input. Tightening silently
  accepted forms is a compatibility change.

- `src/pydot/core.py:1807`, `Dot.create()` — Graphviz failure detection uses an
  `assert`, so optimized Python can silently return `b""` after Graphviz exits
  nonzero, and `Dot.write()` can then write an empty file. Repro:
  `python -O -c "import pydot; d=pydot.Dot(); d.add_node(pydot.Node('a')); print(d.create(format='bogus'))"`.
  The error report also goes to `print()` rather than an exception or logger.
  **Fix:** replace the result assertion with an unconditional exception check;
  retain `AssertionError` unless an exception-type change is documented.

- `src/pydot/core.py:1712`, `Dot.__init__()` — `self.formats` aliases the
  module-level `OUTPUT_FORMATS` set. `pydot.Dot().formats.add("bogus")`
  therefore changes all future `Dot` instances and
  `pydot.core.OUTPUT_FORMATS`. **Fix:** copy the set for each instance and add
  isolation tests for the instance and module-level values.

- `src/pydot/classes.py:69-82`, `FrozenDict.__eq__()` and `__hash__()` —
  equality compares hashes, while the hash depends on item insertion order.
  Equal dictionaries built in different orders compare unequal, and a hash
  collision would compare unequal contents as equal. This reaches
  `Edge.__eq__()` when an endpoint is a subgraph. **Fix:** use mapping equality
  and an order-independent hash while preserving hashability. Low impact, but
  existing equality and hash behavior changes.

- `src/pydot/classes.py`, `FrozenDict` immutability — the inherited dict
  in-place union operator bypasses the blocked mutation methods. For example,
  `d |= {"b": 2}` mutates the object. If `hash(d)` was already called, its
  cached hash is then stale, violating the hash-table contract. **Fix:**
  override `__ior__()` to raise the same `AttributeError` as other mutations;
  add pre-hash and post-hash regression cases.

- `src/pydot/core.py:287-317`, attribute quoting and Graphviz rendering —
  attacker-controlled attribute values can escape their intended attribute and
  inject file-reading Graphviz features. Graphviz attributes such as `image`,
  `shapefile`, `fontpath`, and HTML-like `<IMG SRC=...>` can read local files
  or fetch URLs and embed the result in rendered output. pydot widens this risk
  because values matching `re_dbl_quoted` or `re_html` are emitted verbatim:
  `pydot.Node("n", label='"x" image="/etc/passwd"').to_string()` emits
  `n [label="x" image="/etc/passwd"];`. Exposure applies to services that
  render graphs built from untrusted values or untrusted DOT. **Fix:** document
  that untrusted DOT and attribute values must not be rendered, then correct
  the quoting bypass in a deliberate, versioned change because serialized DOT
  output will change. This is the security-facing side of issues #187/#178;
  re-verified 2026-07-05.

- `src/pydot/dot_parser.py:387-404`, `parse_dot_data()` — deeply nested
  subgraphs can raise an uncaught `RecursionError` at a nesting depth of only
  about 50 with Python's default recursion limit. Repro:
  `graph_from_dot_data("digraph G {" + "subgraph{"*50 + "a" + "}"*50 + "}")`.
  **Fix:** decide whether parser failures should consistently return `None` or
  raise a pydot exception, then handle recursion accordingly and add a bounded
  nesting regression test. Low severity because the exception is catchable,
  but the denial-of-service trigger is tiny; re-verified 2026-07-05.

- `src/pydot/dot_parser.py:397`, `parse_dot_data()` — parsing does not require
  complete input, so a valid graph followed by arbitrary invalid text is
  silently accepted. Verified with `graph G {} THIS IS NOT DOT`, which returns
  a graph instead of `None`. **Fix:** enable pyparsing's full-input check and
  add trailing-garbage and valid-multiple-graph cases. This is a one-line fix,
  but may expose callers that accidentally rely on prefix parsing.

- `src/pydot/core.py:1764`, `Dot.write()` docstring — it claims to return
  `True` or `False` according to success, but it always returns `True` and
  failures raise. **Fix:** document the actual return and failure behavior.

- `src/pydot/core.py:1807`, `Dot.create()` docstring — it says `prog` defaults
  to `twopi`, but the default is `self.prog`, initially `dot`. **Fix:** document
  the actual default.

- `src/pydot/core.py:964,1585,1639`, `Graph`, `Subgraph`, and `Cluster`
  docstrings — they say `suppress_disconnected=False` removes disconnected
  nodes. The default keeps them; `True` removes them. **Fix:** correct all three
  descriptions together.

- `src/pydot/core.py:1639`, `Cluster` docstring — it says the prefix is
  `cluster`, but the constructor uses `cluster_`. **Fix:** include the
  underscore in the documented prefix.

- `src/pydot/core.py:405-433`, `graph_from_dot_data()` and
  `graph_from_dot_file()` docstrings — their return descriptions omit that
  parsing can return `None`, although the annotations admit it. **Fix:**
  document the parse-failure result and current printed diagnostic behavior.

- `src/pydot/core.py:863`, `Edge.__eq__()` docstring — the directed-case text
  says arcs from A to B are equal and then says A->B differs from B->A, making
  the description garbled. **Fix:** state that directed edges compare equal
  only when their ordered `(source, destination)` pairs match.

## Already tracked via expected failures

- Port logic — `test_broken_port_handling` in `test/test_api.py`.
- Numeric and negative parsing regexes — `test_broken_negatives` and
  `test_broken_negatives_2` in `test/test_api.py`.
- Quoting after `set_name()` — `test_set_name_breakage` in
  `test/test_api.py`.

## Considered and dismissed

- Injecting cosmetic nodes or attributes through a crafted attribute value or
  key only changes pydot's output graph. It is not itself a security boundary;
  the meaningful risk is reaching Graphviz's file-reading features, tracked
  above.
- Arbitrary program execution through `prog` requires an application to pass an
  attacker-controlled executable path. `shell=False` and the minimal
  environment already prevent shell injection; at most this merits a one-line
  docstring warning not to pass untrusted `prog` values.
- `shape_files` output uses `os.path.basename()`, so it does not provide a
  write-path traversal. Temporary-file handling was also reviewed and found
  acceptable.
- `Node.add_style()` with an empty initial style —
  `Node("a").add_style("")` calls `None.split()` and raises `AttributeError`.
  The one-condition fix is straightforward, but this falsy-input edge case is
  not worth changing now. Appending an empty string to an existing non-empty
  style also remains unchanged and produces a trailing comma.

## DONE

- `src/pydot/core.py:443`, `graph_from_edges()` bad docstring — removed.
- `src/pydot/core.py:1914-1915`, `Dot.create()` failure reporting — decode
  non-UTF-8 bytes from Graphviz stdout and stderr with replacement error
  handling, preserving the subprocess failure and valid diagnostic text.
- `graph_from_adjacency_matrix()` duplicate-row handling — replaced
  `matrix.index(row)` with the enumerated row index, removing mirrored duplicate
  edges in undirected graphs and the unnecessary O(n²) lookup. Regression cases
  cover `[[1, 1], [1, 1]]` and later duplicate rows.
- Typos and language errors — reviewed; no remaining candidates currently
  recorded.
