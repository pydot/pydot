# SPDX-FileCopyrightText: 2024 pydot contributors
#
# SPDX-License-Identifier: MIT

"""Unit testing of `pydot`."""

from __future__ import annotations

import functools
import os
import sys
from collections.abc import Generator
from hashlib import sha256

import chardet
import pytest

import pydot

TEST_ERROR_DIR = os.getenv("TEST_ERROR_DIR", None)

TEST_PROGRAM = "dot"
TESTS_DIR_1 = "my_tests"
TESTS_DIR_2 = "graphs"

_test_root = os.path.dirname(os.path.abspath(__file__))
_shapefile_dir = os.path.join(_test_root, "from-past-to-future")


class RenderResult:
    """Results object returned by Renderer methods."""

    def __init__(
        self,
        data: bytes,
        dot_file: str | None = None,
        dot_src: str | None = None,
    ) -> None:
        self._data = data
        self._dot_file: str | None = dot_file
        self._dot_src: str | None = dot_src

    @property
    def data(self) -> bytes:
        """Get the raw image data for the result."""
        return self._data

    @property
    def dot_file(self) -> str:
        """Get the graph data used to generate the file."""
        return self._dot_file or ""  # pragma: no cover

    @property
    def dot_src(self) -> str:  # pragma: no cover
        if self._dot_src is None and self.dot_file is not None:
            with open(self.dot_file, encoding="utf-8") as _in:
                self._dot_src = _in.read()
        return self._dot_src or ""

    @functools.cached_property
    def checksum(self) -> str:
        """Get the sha256 checksum for the result."""
        return sha256(self.data).hexdigest()


class GVRenderResult(RenderResult):
    """Results object returned by Renderer methods.

    Unlike RenderResult, GVRenderResult will always have a dot_file.
    """

    def __init__(self, data: bytes, dot_file: str) -> None:
        super().__init__(data)
        self._dot_file: str = dot_file


class PydotRenderResult(RenderResult):
    """Results object returned by Renderer methods.

    Unlike RenderResult, PydotRenderResult will always have a dot_src.
    """

    def __init__(self, data: bytes, dot_src: str) -> None:
        super().__init__(data)
        self._dot_src: str = dot_src


class Renderer:
    """Call pydot renderers for data files."""

    @classmethod
    def graphviz(cls, filename: str, encoding: str) -> GVRenderResult:
        with open(filename, encoding=encoding) as stdin:
            stdout_data, stderr_data, process = pydot.call_graphviz(
                program=TEST_PROGRAM,
                arguments=["-Tjpe"],
                working_dir=os.path.dirname(filename),
                stdin=stdin,
            )
        assert process.returncode == 0, stderr_data
        return GVRenderResult(stdout_data, filename)

    @classmethod
    def pydot(cls, filename: str, encoding: str) -> PydotRenderResult:
        c = pydot.graph_from_dot_file(filename, encoding=encoding)
        if not c:  # pragma: no cover
            raise RuntimeError("No data returned from pydot!")
        jpe_data = bytearray()
        for g in c:
            jpe_data.extend(
                g.create(prog=TEST_PROGRAM, format="jpe", encoding=encoding)
            )
        src = "\n".join(g.to_string() for g in c)
        return PydotRenderResult(jpe_data, src)


def _load_test_cases(casedir: str) -> Generator[tuple[str, str, str]]:
    """Generate testcase parameters from files in a directory.

    Yields testcase names, testfiles, and the files' parent directory.
    """
    path = os.path.join(_test_root, casedir)
    dot_files = filter(lambda x: x.endswith(".dot"), os.listdir(path))

    def _case_name(fname: str) -> str:
        """No str.removesuffix() until Python 3.9."""
        if sys.version_info < (3, 9):  # pragma: no cover
            return fname
        return fname.removesuffix(".dot")

    for dot_file in dot_files:
        yield (_case_name(dot_file), dot_file, path)


def _compare_images(
    fname: str, pd: PydotRenderResult, gv: GVRenderResult
) -> bool:
    """Compare two RenderResult objects for the named test.

    If the images differ and a ``TEST_ERROR_DIR`` has been provided, create
    a subdir for the test and dump both images there for examination."""
    if pd.checksum == gv.checksum:
        return True
    if TEST_ERROR_DIR is not None:  # pragma: no cover
        dirname = fname.replace(".", "_")
        out_dir = os.path.join(os.path.normpath(TEST_ERROR_DIR), dirname)
        os.makedirs(out_dir)
        pd_path = os.path.join(out_dir, "err_pydot.jpeg")
        gv_path = os.path.join(out_dir, "err_graphviz.jpeg")
        with open(pd_path, "wb") as p, open(gv_path, "wb") as g:
            p.write(pd.data)
            g.write(gv.data)
        src_filename = os.path.basename(gv.dot_file)
        gv_src = os.path.join(out_dir, src_filename)
        pd_src = os.path.join(out_dir, f"pydot_{src_filename}")
        with open(gv_src, "w") as gs, open(pd_src, "w") as ps:
            ps.write(pd.dot_src)
            gs.write(gv.dot_src)
    return False  # pragma: no cover


# image files are omitted from sdist
@pytest.mark.skipif(  # pragma: no cover
    not os.path.isdir(_shapefile_dir), reason="shape files not present"
)
def test_graph_with_shapefiles() -> None:
    dot_file = os.path.join(_shapefile_dir, "from-past-to-future.dot")

    pngs = [
        os.path.join(_shapefile_dir, fname)
        for fname in os.listdir(_shapefile_dir)
        if fname.endswith(".png")
    ]

    with open(dot_file, encoding="utf-8") as f:
        graph_data = f.read()

    graphs = pydot.graph_from_dot_data(graph_data)
    assert isinstance(graphs, list)
    assert len(graphs) == 1

    g = graphs.pop()
    g.set_shape_files(pngs)

    rendered = PydotRenderResult(g.create(format="jpe"), g.to_string())
    graphviz = Renderer.graphviz(dot_file, encoding="ascii")
    assert _compare_images("from-past-to-future", rendered, graphviz)


class RenderedTestCase:
    def _render_and_compare_dot_file(self, fdir: str, fname: str) -> None:
        # files that confuse `chardet`
        encodings = {"Latin1.dot": "latin-1"}
        fpath = os.path.join(fdir, fname)
        with open(fpath, "rb") as f:
            s = f.read()
        estimate: str = chardet.detect(s).get("encoding") or "utf-8"
        encoding: str = encodings.get(fname, estimate)
        rendered = Renderer.pydot(
            fpath,
            encoding,
        )
        graphviz = Renderer.graphviz(
            fpath,
            encoding,
        )
        output_matches = _compare_images(fname, rendered, graphviz)
        if not output_matches:  # pragma: no cover
            raise AssertionError(
                f"{fname}: {rendered.checksum} != {graphviz.checksum} "
                "(found pydot vs graphviz difference)"
            )


class TestMyRegressions(RenderedTestCase):
    """Perform regression tests in my_tests dir."""

    @pytest.mark.parametrize(
        "fname,path",
        [
            pytest.param(fname, path, id=_name)
            for (_name, fname, path) in _load_test_cases(TESTS_DIR_1)
        ],
    )
    def test_regression(self, fname: str, path: str) -> None:
        self._render_and_compare_dot_file(path, fname)


class TestGraphvizRegressions(RenderedTestCase):
    """Perform regression tests in graphs dir."""

    @pytest.mark.parametrize(
        "fname,path",
        [
            pytest.param(fname, path, id=_name)
            for (_name, fname, path) in _load_test_cases(TESTS_DIR_2)
        ],
    )
    def test_regression(self, fname: str, path: str) -> None:
        self._render_and_compare_dot_file(path, fname)
