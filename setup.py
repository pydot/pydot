#!/usr/bin/env python
"""Installation script."""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import ast
import codecs
import os
import re


CURRENT_DIR = os.path.dirname(__file__)


def get_long_description():
    readme_path = os.path.join(CURRENT_DIR, "README.md")
    with codecs.open(readme_path, encoding="utf8") as ld_file:
        return ld_file.read()


def get_version():
    pydot_py = os.path.join(CURRENT_DIR, "src", "pydot", "__init__.py")
    _version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")
    with codecs.open(pydot_py, "r", encoding="utf8") as f:
        match = _version_re.search(f.read())
        version = match.group("version") if match is not None else '"unknown"'
    return str(ast.literal_eval(version))


setup(
    name="pydot",
    version=get_version(),
    package_dir={"": "src"},
    packages=["pydot"],
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
)
