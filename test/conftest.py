# SPDX-FileCopyrightText: 2024 pydot contributors
#
# SPDX-License-Identifier: MIT

import pytest


@pytest.fixture
def objdict():
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
    }
