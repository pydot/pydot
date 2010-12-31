# coding=iso-8859-1

# TODO:
# -test graph generation APIs (from adjacency, etc..)
# -test del_node, del_edge methods
# -test Common.set method


import os
try:
    from hashlib import sha256
except ImportError:
    import sha
    sha256 = sha.new
import subprocess

import pydot
import dot_parser
import unittest


DOT_BINARY_PATH         = pydot.find_graphviz()['dot']
TEST_DIR                = './'
REGRESSION_TESTS_DIR    = os.path.join(TEST_DIR, 'graphs')
MY_REGRESSION_TESTS_DIR    = os.path.join(TEST_DIR, 'my_tests')



class TestGraphAPI(unittest.TestCase):
    
    def setUp(self):
        
        self._reset_graphs()
        
    
    def _reset_graphs(self):
        
        self.graph_directed = pydot.Graph('testgraph', graph_type='digraph')
        
    
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
        node.set('label','mine')
        
        self.assertEqual( g.to_string(), 'digraph G {\nlegend [shape=box, label=mine];\n}\n' ) 
        
    
    def test_attribute_with_implicit_value(self):

        d='digraph {\na -> b[label="hi", decorate];\n}'
        g = pydot.graph_from_dot_data(d)
        attrs = g.get_edges()[0].get_attributes()
        
        self.assertEqual( 'decorate' in attrs, True ) 


    def test_subgraphs(self):

        g = pydot.Graph()
        s = pydot.Subgraph("foo")
        
        self.assertEqual( g.get_subgraphs(), [] )
        self.assertEqual( g.get_subgraph_list(), [] )
        
        g.add_subgraph(s)

        self.assertEqual( g.get_subgraphs()[0].get_name(), s.get_name() )
        self.assertEqual( g.get_subgraph_list()[0].get_name(), s.get_name() )


    def test_graph_pickling(self):

        import pickle

        g = pydot.Graph()
        s = pydot.Subgraph("foo")
        g.add_subgraph(s)
        g.add_edge( pydot.Edge('A','B') )
        g.add_edge( pydot.Edge('A','C') )
        g.add_edge( pydot.Edge( ('D','E') ) )
        g.add_node( pydot.Node( 'node!' ) )

        self.assertEqual( type(pickle.dumps(g)), str )



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
        
        #g2 = dot_parser.parse_dot_data( g.to_string() )
        g2 = pydot.graph_from_dot_data( g.to_string() )
        
        self.assertEqual( g2.get_node(node1)[0].get_name(), node1 ) 
        self.assertEqual( g2.get_node(node2)[0].get_name(), node2 ) 
        
        self.assertEqual( g2.get_edges()[0].get_source(), node1 ) 
        self.assertEqual( g2.get_edges()[0].get_destination(), node2 ) 
        
    
    def test_graph_with_shapefiles(self):
        
        shapefile_dir = os.path.join(TEST_DIR, 'from-past-to-future')
        dot_file = os.path.join( shapefile_dir, 'from-past-to-future.dot' )
        
        
        pngs = dot_files = [ os.path.join(shapefile_dir, fname) for 
            fname in os.listdir(shapefile_dir) if fname.endswith('.png') ]
        
        f = file( dot_file, 'rt' )
        graph_data = f.read()
        f.close()
        
        #g = dot_parser.parse_dot_data(graph_data)
        g = pydot.graph_from_dot_data(graph_data)
        
        g.set_shape_files( pngs )
        
        jpe_data = g.create( format='jpe' )
        
        hexdigest = sha256(jpe_data).hexdigest()
        
        hexdigest_original = self._render_with_graphviz(dot_file)
        
        self.assertEqual( hexdigest, hexdigest_original ) 
        
    
    def test_multiple_graphs(self):
        
        graph_data = 'graph A { a->b };\ngraph B {c->d}'
        
        #graphs = dot_parser.parse_dot_data(graph_data)
        graphs = pydot.graph_from_dot_data(graph_data)
        
        self.assertEqual( len(graphs), 2 )
        
        self.assertEqual( [g.get_name() for g in graphs], ['A', 'B'] )
        
    
    def _render_with_graphviz(self, filename):
        
        p = subprocess.Popen(
            ( DOT_BINARY_PATH , '-Tjpe', ),
            cwd = os.path.dirname(filename),
            stdin=file(filename, 'rt'),
            stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            
        stdout = p.stdout
        
        stdout_output = list()
        while True:
            data = stdout.read()
            if not data:
                break
            stdout_output.append(data)
        stdout.close()
            
        if stdout_output:
            stdout_output = ''.join(stdout_output)
            
        #pid, status = os.waitpid(p.pid, 0)
        status = p.wait()
        
        
        return sha256(stdout_output).hexdigest()
        
    
    def _render_with_pydot(self, filename):
        
        #f = file(filename, 'rt')
        #graph_data = f.read()
        #f.close()
        
        #g = dot_parser.parse_dot_data(graph_data)
        #g = pydot.parse_from_dot_data(graph_data)
        g = pydot.graph_from_dot_file(filename)
        
        if not isinstance( g, list ):
            g = [g]
            
        jpe_data = ''.join( [ _g.create( format='jpe' ) for _g in g ] )
        
        return sha256(jpe_data).hexdigest()
        
    
    def test_my_regression_tests(self):
        
        self._render_and_compare_dot_files( MY_REGRESSION_TESTS_DIR )
        
    
    def test_graphviz_regression_tests(self):
        
        self._render_and_compare_dot_files( REGRESSION_TESTS_DIR )
        
    
    def _render_and_compare_dot_files(self, directory):
        
        dot_files = [ fname for fname in os.listdir(directory) if
            fname.endswith('.dot') ] ##and fname.startswith('')]
        
        for dot in dot_files:
            
            #print 'Processing: %s' % dot 
            
            os.sys.stdout.write('#')
            os.sys.stdout.flush()
            
            fname = os.path.join(directory, dot)
            
            try:
                parsed_data_hexdigest = self._render_with_pydot(fname)
            
                original_data_hexdigest = self._render_with_graphviz(fname)
            except Exception, excp:
                print 'Failed redering BAD(%s)' % dot
                #print 'Error:', str(excp)
                raise excp
            
            if parsed_data_hexdigest != original_data_hexdigest:
                print 'BAD(%s)' % dot
            
            self.assertEqual( parsed_data_hexdigest, original_data_hexdigest )
            
        
    
    def test_numeric_node_id(self):
        
        self._reset_graphs()
        
        self.graph_directed.add_node( pydot.Node(1) )
        
        self.assertEqual( self.graph_directed.get_nodes()[0].get_name() , '1' )
        
    
    def test_quoted_node_id(self):
        
        self._reset_graphs()
        
        self.graph_directed.add_node( pydot.Node('"node"') )
        
        self.assertEqual( self.graph_directed.get_nodes()[0].get_name() , '"node"' )
        
    
    def test_quoted_node_id_to_string_no_attributes(self):
        
        self._reset_graphs()
        
        self.graph_directed.add_node( pydot.Node('"node"') )
        
        self.assertEqual( self.graph_directed.get_nodes()[0].to_string() , '"node";' )
    
    def test_keyword_node_id(self):
        
        self._reset_graphs()
        
        self.graph_directed.add_node( pydot.Node('node') )
        
        self.assertEqual( self.graph_directed.get_nodes()[0].get_name() , 'node' )
        
    
    def test_keyword_node_id_to_string_no_attributes(self):
        
        self._reset_graphs()
        
        self.graph_directed.add_node( pydot.Node('node') )
        
        self.assertEqual( self.graph_directed.get_nodes()[0].to_string() , '' )
        
    
    def test_keyword_node_id_to_string_with_attributes(self):
        
        self._reset_graphs()
        
        self.graph_directed.add_node( pydot.Node('node', shape='box') )
        
        self.assertEqual( self.graph_directed.get_nodes()[0].to_string() , 'node [shape=box];' )
        
    
    def test_names_of_a_thousand_nodes(self):
        
        self._reset_graphs()
        
        names = set([ 'node_%05d' % i for i in xrange(10**4) ])
        
        for name in names:
        
            self.graph_directed.add_node( pydot.Node(name, label=name) )
            
        self.assertEqual( set([ n.get_name() for n in self.graph_directed.get_nodes() ]), names )
        
    
    def test_executable_not_found_exception(self):
        
        
        paths = {'dot': 'invalid_executable_path'}
        
        graph = pydot.Dot( 'graphname', graph_type='digraph' )
        
        graph.set_graphviz_executables( paths )
        
        self.assertRaises( pydot.InvocationException,  graph.create )
        
    
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
        import string
        g = pydot.Dot()
        g.add_node(pydot.Node("test", label=string.printable))
        #print g.to_string()
        data = g.create( format='jpe' )
        self.assertEqual( len(data) > 0, True )

if __name__ == '__main__':
    
    suite = unittest.TestLoader().loadTestsFromTestCase( TestGraphAPI )
    
    unittest.TextTestRunner(verbosity=2).run(suite)
