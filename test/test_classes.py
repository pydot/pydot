# SPDX-FileCopyrightText: 2024 pydot contributors
#
# SPDX-License-Identifier: MIT

"""Unit testing of `pydot.classes`."""

import pytest

import pydot
from pydot.classes import FrozenDict


def test_FrozenDict_create(objdict):
    fd = FrozenDict(objdict)
    assert isinstance(fd, FrozenDict)
    assert isinstance(fd["attributes"], FrozenDict)
    assert isinstance(fd["nodes"], FrozenDict)
    assert isinstance(fd["nodes"]["3"], tuple)
    assert isinstance(fd["nodes"]["16"], tuple)

    fd2 = FrozenDict((("a", 1), ("b", 2)), obj_dict={"frozen": fd})
    assert isinstance(fd2["obj_dict"], FrozenDict)
    assert len(fd2) == 3
    assert fd == fd2["obj_dict"]["frozen"]


def test_FrozenDict_modify(objdict):
    fd = FrozenDict(objdict)

    with pytest.raises(AttributeError):
        fd.clear()

    with pytest.raises(AttributeError):
        fd["nodes"] = None

    with pytest.raises(AttributeError):
        fd["nodes"].update({"12": [{"name": "12"}]})

    with pytest.raises(AttributeError):
        fd.popitem()

    with pytest.raises(AttributeError):
        fd.pop("nodes")

    with pytest.raises(AttributeError):
        fd.setdefault("edges", None)

    with pytest.raises(AttributeError):
        del fd["nodes"]


def test_FrozenDict_compare():
    dict_in = {
        "red": "first",
        "green": "second",
        "blue": "third",
    }
    fd1 = FrozenDict(dict_in)
    fd2 = FrozenDict(dict(sorted(dict_in.items())))
    assert hash(fd1) == hash(tuple(dict_in.items()))
    assert hash(fd2) != hash(tuple(dict_in.items()))
    assert fd1 != fd2

    assert fd1 == dict_in
    assert fd2 == dict_in  # Unfortunate fallback to dict.__eq__


def test_frozendict_deprecation(objdict):
    with pytest.warns(DeprecationWarning):
        fd = pydot.frozendict(objdict)

    assert isinstance(fd, FrozenDict)
