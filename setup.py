#!/usr/bin/env python
"""Installation script."""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import pydot


long_description = '''
A Python interface to GraphViz and the DOT language.

This package includes an interface to GraphViz [1], with classes to represent
graphs and dump them in the DOT language [2], and a parser from DOT.


[1] https://www.graphviz.org
[2] https://www.graphviz.org/doc/info/lang.html
'''


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
    long_description=long_description,
    py_modules=['pydot', 'dot_parser'],
    install_requires=['pyparsing>=2.1.4'],
    tests_require=['chardet'])
