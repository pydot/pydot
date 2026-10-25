"""Graph builder helpers in pydot.core: graph_from_edges,
graph_from_adjacency_matrix, graph_from_incidence_matrix.

Node names produced from matrices are 1-based indices, optionally prefixed.
"""

from pydot.core import (
    graph_from_adjacency_matrix,
    graph_from_edges,
    graph_from_incidence_matrix,
)


def test_from_edges_undirected_by_default():
    graph = graph_from_edges([("a", "b"), ("b", "c")])
    assert graph.to_string() == "graph G {\na -- b;\nb -- c;\n}\n"


def test_from_edges_directed():
    graph = graph_from_edges([("a", "b")], directed=True)
    assert graph.to_string() == "digraph G {\na -> b;\n}\n"


def test_from_edges_node_prefix():
    graph = graph_from_edges([("a", "b")], node_prefix="n")
    assert graph.to_string() == "graph G {\nna -- nb;\n}\n"


def test_from_edges_empty():
    assert graph_from_edges([]).to_string() == "graph G {\n}\n"


def test_from_adjacency_undirected():
    graph = graph_from_adjacency_matrix([[0, 1], [0, 0]])
    assert graph.to_string() == "graph G {\n1 -- 2;\n}\n"


def test_from_adjacency_directed_both_directions():
    graph = graph_from_adjacency_matrix([[0, 1], [1, 0]], directed=True)
    assert graph.to_string() == "digraph G {\n1 -> 2;\n2 -> 1;\n}\n"


def test_from_adjacency_node_prefix():
    graph = graph_from_adjacency_matrix([[0, 1], [0, 0]], node_prefix="N")
    assert graph.to_string() == "graph G {\nN1 -- N2;\n}\n"


def test_from_adjacency_empty():
    assert graph_from_adjacency_matrix([]).to_string() == "graph G {\n}\n"


def test_from_incidence_basic():
    # Each row describes one edge; truthy entries mark its endpoints
    # (1-based column positions). Row [1, 0] has a single endpoint and
    # yields no edge; row [1, 1] links nodes 1 and 2.
    graph = graph_from_incidence_matrix([[1, 0], [1, 1]])
    assert graph.to_string() == "graph G {\n1 -- 2;\n}\n"


def test_from_incidence_empty():
    assert graph_from_incidence_matrix([]).to_string() == "graph G {\n}\n"


def test_from_incidence_directed():
    # A single row with two truthy entries is one directed edge.
    graph = graph_from_incidence_matrix([[1, 1]], directed=True)
    assert graph.to_string() == "digraph G {\n1 -> 2;\n}\n"
