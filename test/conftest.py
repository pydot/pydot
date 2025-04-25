# SPDX-FileCopyrightText: 2024 pydot contributors
#
# SPDX-License-Identifier: MIT

import typing as T

import pytest

import pydot.core


@pytest.fixture
def objdict() -> T.Dict[str, T.Any]:
    return {
        "attributes": {},
        "name": "G",
        "type": "graph",
        "strict": False,
        "suppress_disconnected": False,
        "simplify": False,
        "current_child_sequence": 3,
        "nodes": {
            "3": [
                {
                    "attributes": {},
                    "type": "node",
                    "parent_graph": None,
                    "sequence": 1,
                    "name": "3",
                    "port": None,
                }
            ],
            "16": [
                {
                    "attributes": {},
                    "type": "node",
                    "parent_graph": None,
                    "sequence": 2,
                    "name": "16",
                    "port": None,
                }
            ],
        },
        "edges": {},
        "subgraphs": {},
    }


@pytest.fixture
def graph_directed() -> pydot.core.Graph:
    return pydot.core.Graph("testgraph", graph_type="digraph")
