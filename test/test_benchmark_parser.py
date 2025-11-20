# SPDX-FileCopyrightText: 2025 pydot contributors
#
# SPDX-License-Identifier: MIT

from pathlib import Path

import pytest

import pydot.core
from pydot.dot_parser import parse_dot_data

_test_root = Path(__file__).parent


def read_dot_src(dot_file: Path) -> str:
    with dot_file.open(encoding="utf-8") as infile:
        return infile.read()


@pytest.mark.benchmark(
    group="small",
    min_rounds=5,
)
@pytest.mark.parametrize(
    "dot_file",
    [
        "b57.dot",
        "b71.dot",
        "b94.dot",
    ],
)
def test_parsing_small(dot_file: str, benchmark) -> None:
    dot = _test_root / "graphs" / dot_file
    dot_src = read_dot_src(dot)
    res = benchmark(parse_dot_data, dot_src)
    assert isinstance(res, list)
    assert isinstance(res[0], pydot.core.Dot)


@pytest.mark.benchmark(
    group="big",
    min_rounds=2,
)
@pytest.mark.parametrize(
    "dot_file",
    [
        "b29.dot",
        "b69.dot",
        "b102.dot",
    ],
)
def test_parsing_big(dot_file: str, benchmark) -> None:
    dot = _test_root / "graphs" / dot_file
    dot_src = read_dot_src(dot)
    res = benchmark(parse_dot_data, dot_src)
    assert isinstance(res, list)
    assert isinstance(res[0], pydot.core.Dot)


@pytest.mark.benchmark(
    group="multiple",
    min_rounds=2,
)
def test_multiple_parsing(benchmark, latin1_graph_files) -> None:
    dotfile_dir = _test_root / "graphs"
    assert dotfile_dir.is_dir()

    def parse_multiple(_dir) -> int:
        for i, dotfile in enumerate(_dir.iterdir()):
            if (
                not dotfile.name.endswith(".dot")
                or dotfile.name in latin1_graph_files
            ):
                continue
            dot_src = read_dot_src(dotfile)
            res = parse_dot_data(dot_src)
            assert isinstance(res, list)
            assert isinstance(res[0], pydot.core.Dot)
        return i + 1

    count = benchmark(parse_multiple, dotfile_dir)
    assert count == len(set(dotfile_dir.iterdir()))
