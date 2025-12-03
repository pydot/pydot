# SPDX-FileCopyrightText: 2025 pydot contributors
#
# SPDX-License-Identifier: MIT

"""Functions to run Graphviz tools in a subprocess and process results."""

from __future__ import annotations

import os
import subprocess
import sys
import typing as T

from pydot.constants import DEFAULT_PROGRAMS


def is_windows() -> bool:
    return os.name == "nt"


def is_anaconda() -> bool:
    import glob

    conda_pattern = os.path.join(sys.prefix, "conda-meta\\graphviz*.json")
    return glob.glob(conda_pattern) != []


def get_executable_extension() -> str:
    if is_windows():
        return ".bat" if is_anaconda() else ".exe"
    else:
        return ""


def call_graphviz(
    program: str,
    arguments: list[str],
    working_dir: str | bytes,
    **kwargs: T.Any,
) -> tuple[bytes, bytes, subprocess.Popen[bytes]]:
    if program in DEFAULT_PROGRAMS:
        extension = get_executable_extension()
        program += extension

    if arguments is None:
        arguments = []

    if "creationflags" not in kwargs and hasattr(
        subprocess, "CREATE_NO_WINDOW"
    ):
        # Only on Windows OS:
        # specify that the new process shall not create a new window
        kwargs.update(creationflags=subprocess.CREATE_NO_WINDOW)

    # explicitly inherit `$PATH`, on Windows too,
    # with `shell=False`
    env = {
        "PATH": os.environ.get("PATH", ""),
        "LD_LIBRARY_PATH": os.environ.get("LD_LIBRARY_PATH", ""),
        "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
    }

    program_with_args = [program] + arguments

    if sys.version_info < (3, 9):
        my_popen = subprocess.Popen  # pragma: no cover
    else:
        my_popen = subprocess.Popen[bytes]

    process = my_popen(
        program_with_args,
        env=env,
        cwd=working_dir,
        shell=False,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        **kwargs,
    )
    stdout_data, stderr_data = process.communicate()

    return stdout_data, stderr_data, process
