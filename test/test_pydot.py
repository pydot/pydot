# SPDX-FileCopyrightText: 2024 pydot contributors
#
# SPDX-License-Identifier: MIT

"""Unit testing of `pydot`."""

# TODO:
# -test graph generation APIs (from adjacency, etc..)
# -test del_node, del_edge methods
# -test Common.set method

import functools
import os
import sys
import typing as T
import unittest
from hashlib import sha256

import chardet
from parameterized import parameterized

import pydot

TEST_ERROR_DIR = os.getenv("TEST_ERROR_DIR", None)

TEST_PROGRAM = "dot"
TESTS_DIR_1 = "my_tests"
TESTS_DIR_2 = "graphs"

_test_root = os.path.dirname(os.path.abspath(__file__))


class RenderResult:
    """Results object returned by Renderer methods."""

    def __init__(self, data, dot_file=None, dot_src=None) -> None:
        self._data = data
        self._dot_file: T.Optional[str] = dot_file
        self._dot_src: T.Optional[str] = dot_src

    @property
    def data(self):
        """Get the raw image data for the result."""
        return self._data

    @property
    def dot_file(self):
        """Get the graph data used to generate the file."""
        return self._dot_file

    @property
    def dot_src(self):
        if self._dot_src is None and self._dot_file is not None:
            with open(self._dot_file, encoding="utf-8") as _in:
                self._dot_src = _in.read()
        return self._dot_src

    @functools.cached_property
    def checksum(self):
        """Get the sha256 checksum for the result."""
        return sha256(self.data).hexdigest()


class GVRenderResult(RenderResult):
    """Results object returned by Renderer methods.

    Unlike RenderResult, GVRenderResult will always have a dot_file.
    """

    def __init__(self, data, dot_file: str) -> None:
        super().__init__(data)
        self._dot_file: str = dot_file

    @property
    def dot_file(self):
        return self._dot_file

    @property
    def dot_src(self):
        if self._dot_src is None:
            with open(self._dot_file, encoding="utf-8") as _in:
                self._dot_src = _in.read()
        return self._dot_src


class PydotRenderResult(RenderResult):
    """Results object returned by Renderer methods.

    Unlike RenderResult, PydotRenderResult will always have a dot_src.
    """

    def __init__(self, data, dot_src: str) -> None:
        super().__init__(data)
        self._dot_src: str = dot_src

    @property
    def dot_src(self):
        return self._dot_src


class Renderer:
    """Call pydot renderers for data files."""

    @classmethod
    def graphviz(cls, filename, encoding):
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
    def pydot(cls, filename, encoding):
        c = pydot.graph_from_dot_file(filename, encoding=encoding)
        if not c:
            raise RuntimeError("No data returned from pydot!")
        jpe_data = bytearray()
        for g in c:
            jpe_data.extend(
                g.create(prog=TEST_PROGRAM, format="jpe", encoding=encoding)
            )
        src = "\n".join(g.to_string() for g in c)
        return PydotRenderResult(jpe_data, src)


def _load_test_cases(casedir):
    """Return a list of testcase files,

    Returns a list of tuples of the form:
        ("case_file_name", "case_file_name.dot", "path/to/directory")
    """
    global _test_root
    path = os.path.join(_test_root, casedir)
    dot_files = filter(lambda x: x.endswith(".dot"), os.listdir(path))

    def _case_name(fname: str) -> str:
        """No str.removesuffix() until Python 3.9."""
        if sys.version_info < (3, 9):
            return fname
        return fname.removesuffix(".dot")

    return [(_case_name(dot_file), dot_file, path) for dot_file in dot_files]


def _compare_images(
    fname: str, pydot: PydotRenderResult, gv: GVRenderResult
) -> bool:
    """Compare two RenderResult objects for the named test.

    If the images differ and a ``TEST_ERROR_DIR`` has been provided, create
    a subdir for the test and dump both images there for examination."""
    if pydot.checksum == gv.checksum:
        return True
    if TEST_ERROR_DIR is not None:
        dirname = fname.replace(".", "_")
        out_dir = os.path.join(os.path.normpath(TEST_ERROR_DIR), dirname)
        os.makedirs(out_dir)
        pydot_path = os.path.join(out_dir, "err_pydot.jpeg")
        gv_path = os.path.join(out_dir, "err_graphviz.jpeg")
        with open(pydot_path, "wb") as p, open(gv_path, "wb") as g:
            p.write(pydot.data)
            g.write(gv.data)
        src_filename = os.path.basename(gv.dot_file)
        gv_src = os.path.join(out_dir, src_filename)
        pd_src = os.path.join(out_dir, f"pydot_{src_filename}")
        with open(gv_src, "w") as gs, open(pd_src, "w") as ps:
            ps.write(pydot.dot_src)
            gs.write(gv.dot_src)
    return False


class PydotTestCase(unittest.TestCase):
    def setUp(self):
        self._reset_graphs()

    def _reset_graphs(self):
        self.graph_directed = pydot.Graph("testgraph", graph_type="digraph")


class TestShapeFiles(PydotTestCase):
    shapefile_dir = os.path.join(_test_root, "from-past-to-future")

    # image files are omitted from sdist
    @unittest.skipUnless(
        os.path.isdir(shapefile_dir),
        "Skipping tests that involve images,"
        + " they can be found in the git repository",
    )
    def test_graph_with_shapefiles(self):
        dot_file = os.path.join(self.shapefile_dir, "from-past-to-future.dot")

        pngs = [
            os.path.join(self.shapefile_dir, fname)
            for fname in os.listdir(self.shapefile_dir)
            if fname.endswith(".png")
        ]

        with open(dot_file) as f:
            graph_data = f.read()

        graphs = pydot.graph_from_dot_data(graph_data)
        self.assertIsNotNone(graphs)

        if not isinstance(graphs, list):
            return
        g = graphs.pop()
        g.set_shape_files(pngs)

        rendered = PydotRenderResult(g.create(format="jpe"), g.to_string())
        graphviz = Renderer.graphviz(dot_file, encoding="ascii")
        if not _compare_images("from-past-to-future", rendered, graphviz):
            raise AssertionError(
                "from-past-to-future.dot: "
                f"{rendered.checksum} != {graphviz.checksum} "
                "(found pydot vs graphviz difference)"
            )


class RenderedTestCase(PydotTestCase):
    def _render_and_compare_dot_file(self, fdir, fname):
        # files that confuse `chardet`
        encodings = {"Latin1.dot": "latin-1"}
        fpath = os.path.join(fdir, fname)
        with open(fpath, "rb") as f:
            s = f.read()
        estimate = chardet.detect(s)
        encoding = encodings.get(fname, estimate["encoding"])
        rendered = Renderer.pydot(
            fpath,
            encoding,
        )
        graphviz = Renderer.graphviz(
            fpath,
            encoding,
        )
        if not _compare_images(fname, rendered, graphviz):
            raise AssertionError(
                f"{fname}: {rendered.checksum} != {graphviz.checksum} "
                "(found pydot vs graphviz difference)"
            )


class TestMyRegressions(RenderedTestCase):
    """Perform regression tests in my_tests dir."""

    @parameterized.expand(functools.partial(_load_test_cases, TESTS_DIR_1))
    def test_regression(self, _, fname, path):
        self._render_and_compare_dot_file(path, fname)


class TestGraphvizRegressions(RenderedTestCase):
    """Perform regression tests in graphs dir."""

    @parameterized.expand(functools.partial(_load_test_cases, TESTS_DIR_2))
    def test_regression(self, _, fname, path):
        self._render_and_compare_dot_file(path, fname)
