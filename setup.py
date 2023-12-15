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
    description="Python interface to Graphviz's Dot",
    author="Ero Carrera",
    author_email="ero.carrera@gmail.com",
    maintainer="Peter Nowee",
    maintainer_email="peter@peternowee.com",
    url="https://github.com/pydot/pydot",
    project_urls={
        "Changelog": "https://github.com/pydot/pydot/blob/master/ChangeLog",
        "Bug Tracker": "https://github.com/pydot/pydot/issues",
    },
    license="MIT",
    keywords="graphviz dot graphs visualization",
    platforms=["any"],
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    install_requires=["pyparsing>=2.1.4"],
    extras_require={
        "dev": [
            "chardet",
            "black==21.5b2; python_version > '3.5'",
        ],
    },
)
