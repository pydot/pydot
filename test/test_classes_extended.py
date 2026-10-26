"""FrozenDict (pydot.classes) and the exceptions module."""

import pickle

import pytest

from pydot.classes import FrozenDict
from pydot import exceptions


def test_frozendict_reads_like_a_dict():
    frozen = FrozenDict({"a": 1, "b": 2})
    assert frozen["a"] == 1
    assert frozen.get("b") == 2
    assert frozen.get("missing") is None
    assert set(frozen.keys()) == {"a", "b"}
    assert len(frozen) == 2
    assert "a" in frozen


def test_frozendict_kwargs_construction():
    assert FrozenDict(x=1)["x"] == 1


def test_frozendict_nested_dicts_are_frozen():
    frozen = FrozenDict({"outer": {"inner": 3}})
    assert isinstance(frozen["outer"], FrozenDict)
    assert frozen["outer"]["inner"] == 3


def test_frozendict_list_of_dicts_becomes_tuple_of_frozen():
    frozen = FrozenDict({"items": [{"e": 3}, 5]})
    assert frozen["items"] == (FrozenDict({"e": 3}), 5)
    assert isinstance(frozen["items"][0], FrozenDict)


def test_frozendict_non_dict_values_untouched():
    frozen = FrozenDict({"n": 5, "s": "x", "lst": [1, 2]})
    assert frozen["n"] == 5
    assert frozen["s"] == "x"
    # Plain lists are frozen to tuples (only dict elements stay dicts).
    assert frozen["lst"] == (1, 2)


def test_frozendict_equality_and_hash():
    left = FrozenDict({"a": 1, "b": {"c": 2}})
    right = FrozenDict({"a": 1, "b": {"c": 2}})
    assert left == right
    assert hash(left) == hash(right)
    assert left != FrozenDict({"a": 9})


def test_frozendict_pickle_round_trip():
    frozen = FrozenDict({"a": 1, "b": {"c": 2}, "d": [{"e": 3}]})
    restored = pickle.loads(pickle.dumps(frozen))
    assert restored == frozen
    assert isinstance(restored["b"], FrozenDict)
    with pytest.raises(AttributeError):
        restored["a"] = 9


def test_exceptions_hierarchy():
    assert issubclass(exceptions.Error, exceptions.PydotException)
    assert issubclass(exceptions.PydotException, Exception)
    error = exceptions.Error("boom")
    assert isinstance(error, Exception)
    assert str(error) == "boom"
