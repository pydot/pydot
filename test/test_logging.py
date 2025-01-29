# SPDX-FileCopyrightText: 2025 pydot contributors
#
# SPDX-License-Identifier: MIT

"""Unit testing of pydot logging setup."""

import importlib
import logging

import pytest

import pydot


def test_logging_init(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.DEBUG, logger="pydot"):
        importlib.reload(pydot)
        importlib.reload(pydot.core)
        importlib.reload(pydot.dot_parser)
    assert caplog.record_tuples == [
        ("pydot", logging.DEBUG, "pydot initializing"),
        ("pydot", logging.DEBUG, f"pydot {pydot.__version__}"),
        ("pydot.core", logging.DEBUG, "pydot core module initializing"),
        (
            "pydot.dot_parser",
            logging.DEBUG,
            "pydot dot_parser module initializing",
        ),
    ]
    importlib.reload(pydot)
