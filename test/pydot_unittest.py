# coding=utf-8
"""Unit testing of `pydot`."""
# TODO:
# -test graph generation APIs (from adjacency, etc..)
# -test del_node, del_edge methods
# -test Common.set method
from __future__ import division
from __future__ import print_function
import argparse
from hashlib import sha256
import io
import os
import pickle
import string
import subprocess
import sys
import warnings

import chardet
import pydot
import unittest


DOT_BINARY_PATH = 'dot'
TESTS_DIR_1 = 'my_tests'
TESTS_DIR_2 = 'graphs'


class TestGraphAPI(unittest.TestCase):

    def setUp(self):

        self._reset_graphs()


    def _reset_graphs(self):

        self.graph_directed = pydot.Graph('testgraph',
                                          graph_type='digraph')


    def test_keep_graph_type(self):

        g = pydot.Dot(graph_name='Test', graph_type='graph')

        self.assertEqual( g.get_type(), 'graph' )

        g = pydot.Dot(graph_name='Test', graph_type='digraph')

        self.assertEqual( g.get_type(), 'digraph' )


    def test_add_style(self):

        g = pydot.Dot(graph_name='Test', graph_type='graph')

        node = pydot.Node('mynode')
        node.add_style('abc')
        self.assertEqual( node.get_style(), 'abc' )
        node.add_style('def')
        self.assertEqual( node.get_style(), 'abc,def' )
        node.add_style('ghi')
        self.assertEqual( node.get_style(), 'abc,def,ghi' )


    def test_create_simple_graph_with_node(self):

        g = pydot.Dot()
        g.set_type('digraph')
        node = pydot.Node('legend')
        node.set("shape", 'box')
        g.add_node(node)
        node.set('label', 'mine')
        s = g.to_string()
        s_0 = 'digraph G {\nlegend [label=mine, shape=box];\n}\n'
        s_1 = 'digraph G {\nlegend [shape=box, label=mine];\n}\n'
        assert s == s_0 or s == s_1, (s, s_0)

    def test_attribute_with_implicit_value(self):

        d='digraph {\na -> b[label="hi", decorate];\n}'
        graphs = pydot.graph_from_dot_data(d)
        (g,) = graphs
        attrs = g.get_edges()[0].get_attributes()

        self.assertEqual( 'decorate' in attrs, True )


    def test_subgraphs(self):

        g = pydot.Graph()
        s = pydot.Subgraph("foo")

        self.assertEqual( g.get_subgraphs(), [] )
        self.assertEqual( g.get_subgraph_list(), [] )

        g.add_subgraph(s)

        self.assertEqual(g.get_subgraphs()[0].get_name(),
                         s.get_name())
        self.assertEqual(g.get_subgraph_list()[0].get_name(),
                         s.get_name())


    def test_graph_pickling(self):


        g = pydot.Graph()
        s = pydot.Subgraph("foo")
        g.add_subgraph(s)
        g.add_edge( pydot.Edge('A','B') )
        g.add_edge( pydot.Edge('A','C') )
        g.add_edge( pydot.Edge( ('D','E') ) )
        g.add_node( pydot.Node( 'node!' ) )
        pickle.dumps(g)

    def test_unicode_ids(self):

        node1 = '"aánñoöüé€"'
        node2 = '"îôø®çßΩ"'

        g = pydot.Dot()
        g.set_charset('latin1')
        g.add_node( pydot.Node( node1 ) )
        g.add_node( pydot.Node( node2 ) )
        g.add_edge( pydot.Edge( node1, node2 ) )

        self.assertEqual( g.get_node(node1)[0].get_name(), node1 )
        self.assertEqual( g.get_node(node2)[0].get_name(), node2 )

        self.assertEqual( g.get_edges()[0].get_source(), node1 )
        self.assertEqual( g.get_edges()[0].get_destination(), node2 )
        graphs = pydot.graph_from_dot_data(g.to_string())
        (g2,) = graphs

        self.assertEqual( g2.get_node(node1)[0].get_name(), node1 )
        self.assertEqual( g2.get_node(node2)[0].get_name(), node2 )

        self.assertEqual( g2.get_edges()[0].get_source(), node1 )
        self.assertEqual( g2.get_edges()[0].get_destination(), node2 )


    def test_graph_with_shapefiles(self):

        shapefile_dir = os.path.join(test_dir,
                                     'from-past-to-future')
        # image files are omitted from sdist
        if not os.path.isdir(shapefile_dir):
            warnings.warn('Skipping tests that involve images, '
                          'they can be found in the `git` repository.')
            return
        dot_file = os.path.join(shapefile_dir,
                                'from-past-to-future.dot')


        pngs = dot_files = [
            os.path.join(shapefile_dir, fname) for
            fname in os.listdir(shapefile_dir)
            if fname.endswith('.png')]

        f = open(dot_file, 'rt')
        graph_data = f.read()
        f.close()

        #g = dot_parser.parse_dot_data(graph_data)
        graphs = pydot.graph_from_dot_data(graph_data)
        (g,) = graphs
        g.set_shape_files( pngs )

        jpe_data = g.create( format='jpe' )

        hexdigest = sha256(jpe_data).hexdigest()
        hexdigest_original = self._render_with_graphviz(
            dot_file, encoding='ascii')
        self.assertEqual( hexdigest, hexdigest_original )


    def test_multiple_graphs(self):
        graph_data = 'graph A { a->b };\ngraph B {c->d}'
        graphs = pydot.graph_from_dot_data(graph_data)
        n = len(graphs)
        assert n == 2, n
        names = [g.get_name() for g in graphs]
        assert names == ['A', 'B'], names

    def _render_with_graphviz(self, filename, encoding):
        with io.open(filename, 'rt', encoding=encoding) as stdin:
            p = subprocess.Popen(
                [DOT_BINARY_PATH, '-Tjpe'],
                cwd=os.path.dirname(filename),
                stdin=stdin,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        stdout_data, stderr_data = p.communicate()
        return sha256(stdout_data).hexdigest()

    def _render_with_pydot(self, filename, encoding):
        c = pydot.graph_from_dot_file(filename, encoding=encoding)
        sha = ''
        for g in c:
            jpe_data = g.create(format='jpe', encoding=encoding)
            sha += sha256(jpe_data).hexdigest()
        return sha

    def test_my_regression_tests(self):
        path = os.path.join(test_dir, TESTS_DIR_1)
        self._render_and_compare_dot_files(path)


    def test_graphviz_regression_tests(self):
        path = os.path.join(test_dir, TESTS_DIR_2)
        self._render_and_compare_dot_files(path)


    def _render_and_compare_dot_files(self, directory):
        # files that confuse `chardet`
        encodings = {
            'Latin1.dot': 'latin-1'}
        dot_files = [
            fname for fname in os.listdir(directory)
            if fname.endswith('.dot')]
        for fname in dot_files:
            fpath = os.path.join(directory, fname)
            with open(fpath, 'rb') as f:
                s = f.read()
            estimate = chardet.detect(s)
            encoding = encodings.get(fname, estimate['encoding'])
            os.sys.stdout.write('#')
            os.sys.stdout.flush()
            pydot_sha = self._render_with_pydot(fpath, encoding)
            pydot_sha = self._render_with_graphviz(fpath, encoding)
            assert pydot_sha == pydot_sha, (pydot_sha, pydot_sha)

    def test_numeric_node_id(self):

        self._reset_graphs()

        self.graph_directed.add_node( pydot.Node(1) )

        self.assertEqual(
            self.graph_directed.get_nodes()[0].get_name(), '1')


    def test_quoted_node_id(self):

        self._reset_graphs()

        self.graph_directed.add_node( pydot.Node('"node"') )

        self.assertEqual(
            self.graph_directed.get_nodes()[0].get_name(), '"node"')


    def test_quoted_node_id_to_string_no_attributes(self):

        self._reset_graphs()

        self.graph_directed.add_node( pydot.Node('"node"') )

        self.assertEqual(
            self.graph_directed.get_nodes()[0].to_string(), '"node";')

    def test_keyword_node_id(self):

        self._reset_graphs()

        self.graph_directed.add_node( pydot.Node('node') )

        self.assertEqual(
            self.graph_directed.get_nodes()[0].get_name(), 'node')


    def test_keyword_node_id_to_string_no_attributes(self):

        self._reset_graphs()

        self.graph_directed.add_node( pydot.Node('node') )

        self.assertEqual(
            self.graph_directed.get_nodes()[0].to_string() , '' )


    def test_keyword_node_id_to_string_with_attributes(self):

        self._reset_graphs()

        self.graph_directed.add_node( pydot.Node('node', shape='box') )

        self.assertEqual(
            self.graph_directed.get_nodes()[0].to_string(),
            'node [shape=box];')


    def test_names_of_a_thousand_nodes(self):

        self._reset_graphs()

        names = { 'node_%05d' % i for i in range(10**3) }

        for name in names:

            self.graph_directed.add_node( pydot.Node(name, label=name) )

        self.assertEqual(
            {n.get_name()
                 for n in self.graph_directed.get_nodes()}, names)


    def test_executable_not_found_exception(self):
        graph = pydot.Dot('graphname', graph_type='digraph')
        self.assertRaises(Exception,  graph.create, prog='dothehe')


    def test_graph_add_node_argument_type(self):

        self._reset_graphs()

        self.assertRaises( TypeError,  self.graph_directed.add_node, 1 )
        self.assertRaises( TypeError,  self.graph_directed.add_node, 'a' )


    def test_graph_add_edge_argument_type(self):

        self._reset_graphs()

        self.assertRaises( TypeError,  self.graph_directed.add_edge, 1 )
        self.assertRaises( TypeError,  self.graph_directed.add_edge, 'a' )


    def test_graph_add_subgraph_argument_type(self):

        self._reset_graphs()

        self.assertRaises( TypeError,  self.graph_directed.add_subgraph, 1 )
        self.assertRaises( TypeError,  self.graph_directed.add_subgraph, 'a' )


    def test_quoting(self):
        g = pydot.Dot()
        g.add_node(pydot.Node("test", label=string.printable))
        #print g.to_string()
        data = g.create( format='jpe' )
        self.assertEqual( len(data) > 0, True )

    def test_dot_args(self):
        g = pydot.Dot()
        u = pydot.Node('a')
        g.add_node(u)
        g.write_svg('test.svg', prog=['twopi', '-Goverlap=scale'])


def check_path():
    not_check = parse_args()
    if not_check:
        return
    assert not os.path.isfile('setup.py'), (
        'running out of source does not '
        'test the installed `pydot`.')


def parse_args():
    """Return arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--no-check', action='store_true',
        help=('do not require that no `setup.py` be present '
              'in the current working directory.'))
    args, unknown = parser.parse_known_args()
    # avoid confusing `unittest`
    sys.argv = [sys.argv[0]] + unknown
    return args.no_check


if __name__ == '__main__':
    check_path()
    test_dir = os.path.dirname(sys.argv[0])
    print('The tests are using `pydot` from:  {pd}'.format(pd=pydot))
    unittest.main(verbosity=2)
