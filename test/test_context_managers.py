# SPDX-FileCopyrightText: 2026 pydot contributors
#
# SPDX-License-Identifier: MIT

"""Unit testing of context manager support in pydot."""

from __future__ import annotations

import pytest

import pydot


def test_context_manager_returns_exact_instance():
    g_orig = pydot.Graph("G")
    with g_orig as g_ctx:
        assert g_orig is g_ctx

    # Subsequent calls don't change anything
    with g_orig as g_ctx:
        assert g_orig is g_ctx
    with g_orig as g_ctx:
        assert g_orig is g_ctx


def test_context_manager_empty_block():
    with pydot.Graph("G") as g:
        pass
    assert g.get_name() == "G"
    assert len(g.get_nodes()) == 0


def test_context_manager_dot():
    with pydot.Dot(graph_name="main", graph_type="digraph") as dot:
        assert isinstance(dot, pydot.Dot)

        node_a = pydot.Node("A")
        node_b = pydot.Node("B")
        edge_ab = pydot.Edge(node_a, node_b)

        dot.add_node(node_a)
        dot.add_node(node_b)
        dot.add_edge(edge_ab)

    assert dot.get_name() == "main"
    assert len(dot.get_nodes()) == 2
    assert len(dot.get_edges()) == 1
    assert dot.get_nodes()[0].get_name() == "A"
    assert dot.get_nodes()[1].get_name() == "B"


def test_context_manager_graph():
    with pydot.Graph(graph_name="G") as g:
        assert isinstance(g, pydot.Graph)
        g.add_node(pydot.Node("B"))

    assert g.get_name() == "G"
    assert len(g.get_nodes()) == 1


def test_context_manager_subgraph():
    with pydot.Subgraph(graph_name="sub") as sub:
        assert isinstance(sub, pydot.Subgraph)
        sub.add_node(pydot.Node("C"))

    assert sub.get_name() == "sub"
    assert len(sub.get_nodes()) == 1


def test_context_manager_cluster():
    with pydot.Cluster(graph_name="my_cluster") as cluster:
        assert isinstance(cluster, pydot.Cluster)
        cluster.add_node(pydot.Node("D"))

    # Cluster name is prefixed with 'cluster_'
    assert cluster.get_name() == "cluster_my_cluster"
    assert len(cluster.get_nodes()) == 1


def test_context_manager_nested_mixed():
    dot = pydot.Dot("my_graph", graph_type="digraph")

    with pydot.Cluster("my_cluster") as cluster:
        cluster.add_node(pydot.Node("A"))
        cluster.add_node(pydot.Node("B"))
        dot.add_subgraph(cluster)

        with pydot.Subgraph("nested_sub") as sub:
            sub.add_node(pydot.Node("C"))
            cluster.add_subgraph(sub)

            with pydot.Cluster("deep_cluster") as deep:
                deep.add_node(pydot.Node("D"))
                sub.add_subgraph(deep)

    assert len(dot.get_subgraphs()) == 1
    cluster_obj = dot.get_subgraphs()[0]
    assert cluster_obj.get_name() == "cluster_my_cluster"
    assert len(cluster_obj.get_nodes()) == 2

    assert len(cluster_obj.get_subgraphs()) == 1
    sub_obj = cluster_obj.get_subgraphs()[0]
    assert sub_obj.get_name() == "nested_sub"
    assert len(sub_obj.get_nodes()) == 1
    assert sub_obj.get_nodes()[0].get_name() == "C"

    assert len(sub_obj.get_subgraphs()) == 1
    deep_obj = sub_obj.get_subgraphs()[0]
    assert deep_obj.get_name() == "cluster_deep_cluster"
    assert len(deep_obj.get_nodes()) == 1
    assert deep_obj.get_nodes()[0].get_name() == "D"


def test_context_manager_exception_propagation():
    # Context manager should not swallow exceptions
    with pytest.raises(ValueError, match="test error"):
        with pydot.Dot() as dot:
            dot.add_node(pydot.Node("A"))
            raise ValueError("test error")

    # Even if exception occurred,
    # the object is still accessible and preserved up to the failure
    assert dot.get_name() == "G"  # Defaults to "G" when not specified
    assert len(dot.get_nodes()) == 1
