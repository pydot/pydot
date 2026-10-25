"""Graph / Subgraph / Cluster / Dot pure-logic behaviour (pydot.core).

Only object construction, membership handling and DOT rendering are used;
nothing here invokes a Graphviz binary. Dot.write(format="raw") is included
because it writes the DOT source without calling any external program.
"""

import pytest

import pydot
from pydot import Cluster, Dot, Edge, Graph, Node, Subgraph


def test_graph_defaults():
    graph = Graph()
    assert graph.get_name() == "G"
    assert graph.get_graph_type() == "digraph"
    assert graph.get_strict() is False
    assert graph.get_simplify() is False
    assert graph.get_suppress_disconnected() is False
    assert graph.to_string() == "digraph G {\n}\n"


def test_graph_undirected_to_string():
    graph = Graph("U", graph_type="graph")
    graph.add_edge(Edge("a", "b"))
    assert graph.to_string() == "graph U {\na -- b;\n}\n"


def test_graph_directed_to_string_with_nodes_and_edge():
    graph = Graph("G", graph_type="digraph")
    graph.add_node(Node("a"))
    graph.add_node(Node("b"))
    graph.add_edge(Edge("a", "b"))
    assert graph.to_string() == "digraph G {\na;\nb;\na -> b;\n}\n"


def test_graph_set_type_case_insensitive_and_invalid():
    graph = Graph("G")
    graph.set_type("DIGRAPH")
    assert graph.get_type() == "digraph"
    with pytest.raises(pydot.Error, match='Invalid type "bogus"'):
        graph.set_type("bogus")
    with pytest.raises(pydot.Error):
        graph.set_type(123)


def test_graph_set_name_and_strict_flag_in_first_line():
    graph = Graph("G", graph_type="digraph", strict=True)
    assert graph.get_strict() is True
    assert graph.to_string().startswith("strict digraph G {")
    graph.set_name("H")
    assert graph.get_name() == "H"


def test_graph_sequence_numbers_increment():
    graph = Graph("G", graph_type="digraph")
    assert graph.get_next_sequence_number() == 1
    assert graph.get_next_sequence_number() == 2
    node = Node("a")
    graph.add_node(node)
    assert node.get_sequence() == 3
    edge = Edge("a", "b")
    graph.add_edge(edge)
    assert edge.get_sequence() == 4


def test_graph_add_node_rejects_non_node():
    with pytest.raises(TypeError, match="non node class object"):
        Graph("G").add_node("nope")


def test_graph_add_edge_rejects_non_edge():
    with pytest.raises(TypeError, match="non edge class object"):
        Graph("G").add_edge("nope")


def test_graph_add_subgraph_rejects_non_subgraph():
    with pytest.raises(TypeError, match="non subgraph class object"):
        Graph("G").add_subgraph(Node("a"))


def test_graph_duplicate_nodes_listed_in_order():
    graph = Graph("X", graph_type="digraph")
    graph.add_node(Node("a", color="red"))
    graph.add_node(Node("a", color="blue"))
    assert [n.get("color") for n in graph.get_node("a")] == ["red", "blue"]
    assert len(graph.get_node_list()) == 2


def test_graph_get_node_missing_is_empty():
    assert Graph("G").get_node("zzz") == []


def test_graph_del_node_all_and_by_index():
    graph = Graph("X", graph_type="digraph")
    graph.add_node(Node("a", color="red"))
    graph.add_node(Node("a", color="blue"))
    assert graph.del_node("a", index=0) is True
    assert [n.get("color") for n in graph.get_node("a")] == ["blue"]
    assert graph.del_node("a") is True
    assert graph.get_node("a") == []
    assert graph.del_node("nope") is False


def test_graph_del_node_accepts_node_object():
    graph = Graph("G", graph_type="digraph")
    graph.add_node(Node("a"))
    assert graph.del_node(Node("a")) is True
    assert graph.get_node_list() == []


def test_graph_del_node_out_of_range_index_deletes_all():
    # Quirk (current behaviour): an index beyond the list length falls
    # through to the "delete the whole key" branch instead of being a no-op.
    graph = Graph("G", graph_type="digraph")
    graph.add_node(Node("a"))
    assert graph.del_node("a", index=5) is True
    assert graph.get_node_list() == []


def test_graph_get_and_del_edge_forms():
    graph = Graph("X", graph_type="digraph")
    graph.add_edge(Edge("a", "b"))
    graph.add_edge(Edge("a", "c"))
    assert len(graph.get_edge("a", "b")) == 1
    assert len(graph.get_edge(["a", "b"])) == 1
    assert graph.get_edge("a", "zzz") == []
    assert graph.del_edge(["a", "b"]) is True
    assert len(graph.get_edge_list()) == 1
    assert graph.del_edge("a", "c") is True
    assert graph.get_edge_list() == []
    assert graph.del_edge("a", "b") is False


def test_graph_get_edge_with_node_objects_returns_empty():
    # Quirk (current behaviour): del_edge() converts Node arguments to
    # names, but get_edge() does not, so Node lookups find nothing.
    graph = Graph("Y", graph_type="digraph")
    graph.add_edge(Edge("a", "b"))
    assert graph.get_edge(Node("a"), Node("b")) == []


def test_graph_del_edge_accepts_node_objects():
    graph = Graph("X", graph_type="digraph")
    graph.add_edge(Edge("a", "b"))
    assert graph.del_edge(Node("a"), Node("b")) is True
    assert graph.get_edge_list() == []


def test_graph_defaults_are_pseudo_nodes_emitted_in_sequence_order():
    graph = Graph("G", graph_type="digraph")
    graph.add_node(Node("a"))
    graph.set_node_defaults(shape="box")
    graph.set_edge_defaults(color="red")
    graph.set_graph_defaults(rankdir="LR")
    assert graph.get_node_defaults() == [{"shape": "box"}]
    assert graph.get_edge_defaults() == [{"color": "red"}]
    assert graph.get_graph_defaults() == [{"rankdir": "LR"}]
    assert graph.to_string() == (
        "digraph G {\n"
        "a;\n"
        "node [shape=box];\n"
        "edge [color=red];\n"
        "graph [rankdir=LR];\n"
        "}\n"
    )


def test_graph_suppress_disconnected_hides_lonely_nodes():
    graph = Graph("GD", graph_type="digraph")
    graph.set_suppress_disconnected(True)
    graph.add_node(Node("lonely"))
    graph.add_edge(Edge("a", "b"))
    assert graph.to_string() == "digraph GD {\na -> b;\n}\n"


def test_graph_suppress_disconnected_also_hides_default_lines():
    # Quirk (current behaviour): default pseudo-nodes have no edges, so
    # suppress_disconnected hides their lines too, while get_*_defaults()
    # still reports them.
    graph = Graph("G", graph_type="digraph")
    graph.set_suppress_disconnected(True)
    graph.set_node_defaults(shape="box")
    assert "node [shape=box]" not in graph.to_string()
    assert graph.get_node_defaults() == [{"shape": "box"}]


def test_graph_simplify_dedups_only_in_output():
    # Quirk (current behaviour): simplify affects to_string(), not the
    # stored edge list.
    graph = Graph("GS", graph_type="digraph")
    graph.set_simplify(True)
    graph.add_edge(Edge("a", "b"))
    graph.add_edge(Edge("a", "b"))
    assert len(graph.get_edge_list()) == 2
    assert graph.to_string() == "digraph GS {\na -> b;\n}\n"
    plain = Graph("GS2", graph_type="digraph")
    plain.add_edge(Edge("a", "b"))
    plain.add_edge(Edge("a", "b"))
    assert plain.to_string() == "digraph GS2 {\na -> b;\na -> b;\n}\n"


def test_graph_equality_is_obj_dict_identity():
    graph = Graph("G", graph_type="digraph")
    assert graph == graph
    assert Graph("G", graph_type="digraph") != Graph("G", graph_type="digraph")
    assert (graph == "not a graph") is False


def test_graph_context_manager():
    with Graph("CG", graph_type="digraph") as graph:
        graph.add_node(Node("a"))
        assert [n.get_name() for n in graph.get_node_list()] == ["a"]
    assert graph.to_string() == "digraph CG {\na;\n}\n"


def test_graph_generated_attribute_methods():
    graph = Graph("G")
    graph.set_rankdir("LR")
    assert graph.get_rankdir() == "LR"


def test_graph_inline_and_indent_to_string():
    graph = Graph("G", graph_type="digraph")
    graph.add_node(Node("a"))
    assert graph.to_string(inline=True) == "digraph G {\na;\n}"
    assert graph.to_string(indent="  ") == "digraph G {\n  a;\n}\n"


def test_subgraph_and_cluster_names():
    subgraph = Subgraph("cluster_0")
    assert subgraph.get_graph_type() == "subgraph"
    assert subgraph.to_string() == "subgraph cluster_0 {\n}\n"
    cluster = Cluster("mycluster")
    assert cluster.get_name() == "cluster_mycluster"
    assert cluster.to_string() == "subgraph cluster_mycluster {\n}\n"
    # Quirk (current behaviour): the prefix is prepended unconditionally.
    assert Cluster("cluster_bar").get_name() == "cluster_cluster_bar"


def test_graph_subgraph_membership_and_lookup():
    graph = Graph("G2", graph_type="digraph")
    subgraph = Subgraph("cluster_0")
    subgraph.add_node(Node("x"))
    graph.add_subgraph(subgraph)
    assert [s.get_name() for s in graph.get_subgraph_list()] == ["cluster_0"]
    assert [s.get_name() for s in graph.get_subgraph("cluster_0")] == ["cluster_0"]
    assert graph.get_subgraph("nope") == []
    assert graph.to_string() == "digraph G2 {\nsubgraph cluster_0 {\nx;\n}\n}\n"


def test_subgraph_strict_hidden_when_nested():
    # "strict" is emitted only when the graph is its own parent graph;
    # once nested, the subgraph's parent is the top graph, so it is hidden.
    subgraph = Subgraph("s")
    subgraph.set_strict(True)
    subgraph.add_node(Node("a"))
    graph = Graph("G", graph_type="digraph")
    graph.add_subgraph(subgraph)
    assert graph.to_string() == "digraph G {\nsubgraph s {\na;\n}\n}\n"


def test_dot_defaults_prog_and_shape_files():
    dot = Dot()
    assert dot.get_type() == "digraph"
    assert dot.get_name() == "G"
    assert dot.prog == "dot"
    dot.set_prog("neato")
    assert dot.prog == "neato"
    dot.set_shape_files("a.png")
    dot.set_shape_files(["b.png", "c.png"])
    assert dot.shape_files == ["a.png", "b.png", "c.png"]


def test_dot_write_raw_and_read_back(tmp_path):
    dot = Dot("D", graph_type="digraph")
    dot.add_edge(Edge("a", "b"))
    path = tmp_path / "out.dot"
    dot.write(str(path), format="raw")
    assert path.read_text() == dot.to_string()
    graphs = pydot.graph_from_dot_file(str(path))
    assert graphs is not None
    assert graphs[0].to_string() == dot.to_string()


def test_graph_from_dot_file_missing_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        pydot.graph_from_dot_file(str(tmp_path / "missing.dot"))
