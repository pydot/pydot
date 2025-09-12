# SPDX-FileCopyrightText: 2024 pydot contributors
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import copy
import typing as T

import pytest


@pytest.fixture
def objdict() -> dict[str, T.Any]:
    obj = {
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
    return copy.deepcopy(obj)


@pytest.fixture
def latin1_graph_files() -> set[str]:
    return {
        "b34.dot",
        "b56.dot",
        "b60.dot",
        "Latin1.dot",
    }
