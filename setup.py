#!/usr/bin/env python
"""Installation script."""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import codecs
import os

import pydot


CURRENT_DIR = os.path.dirname(__file__)


def get_long_description() -> str:
    readme_path = os.path.join(CURRENT_DIR, "README.md")
    with codecs.open(readme_path, encoding="utf8") as ld_file:
        return ld_file.read()


setup(
    name='pydot',
    version=pydot.__version__,
    description="Python interface to Graphviz's Dot",
    author='Ero Carrera',
    author_email='ero@dkbza.org',
    maintainer='Sebastian Kalinowski',
    maintainer_email='sebastian@kalinowski.eu',
    url='https://github.com/pydot/pydot',
    license='MIT',
    keywords='graphviz dot graphs visualization',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    py_modules=['pydot', 'dot_parser'],
    install_requires=['pyparsing>=2.1.4'],
    tests_require=['chardet'])
