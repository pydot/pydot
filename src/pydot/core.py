# SPDX-FileCopyrightText: 2024 pydot contributors
#
# SPDX-License-Identifier: MIT

"""An interface to GraphViz."""

import copy
import errno
import logging
import os
import re
import subprocess
import sys

import pydot
import pydot.dot_parser
from pydot._vendor import tempfile

_logger = logging.getLogger(__name__)
_logger.debug("pydot core module initializing")

# fmt: off
GRAPH_ATTRIBUTES = {
    "Damping", "K", "URL", "aspect", "bb", "bgcolor",
    "center", "charset", "clusterrank", "colorscheme", "comment", "compound",
    "concentrate", "defaultdist", "dim", "dimen", "diredgeconstraints",
    "dpi", "epsilon", "esep", "fontcolor", "fontname", "fontnames",
    "fontpath", "fontsize", "id", "label", "labeljust", "labelloc",
    "landscape", "layers", "layersep", "layout", "levels", "levelsgap",
    "lheight", "lp", "lwidth", "margin", "maxiter", "mclimit", "mindist",
    "mode", "model", "mosek", "nodesep", "nojustify", "normalize", "nslimit",
    "nslimit1", "ordering", "orientation", "outputorder", "overlap",
    "overlap_scaling", "pack", "packmode", "pad", "page", "pagedir",
    "quadtree", "quantum", "rankdir", "ranksep", "ratio", "remincross",
    "repulsiveforce", "resolution", "root", "rotate", "searchsize", "sep",
    "showboxes", "size", "smoothing", "sortv", "splines", "start",
    "stylesheet", "target", "truecolor", "viewport", "voro_margin",
    # for subgraphs
    "rank"
}


EDGE_ATTRIBUTES = {
    "URL", "arrowhead", "arrowsize", "arrowtail",
    "color", "colorscheme", "comment", "constraint", "decorate", "dir",
    "edgeURL", "edgehref", "edgetarget", "edgetooltip", "fontcolor",
    "fontname", "fontsize", "headURL", "headclip", "headhref", "headlabel",
    "headport", "headtarget", "headtooltip", "href", "id", "label",
    "labelURL", "labelangle", "labeldistance", "labelfloat", "labelfontcolor",
    "labelfontname", "labelfontsize", "labelhref", "labeltarget",
    "labeltooltip", "layer", "len", "lhead", "lp", "ltail", "minlen",
    "nojustify", "penwidth", "pos", "samehead", "sametail", "showboxes",
    "style", "tailURL", "tailclip", "tailhref", "taillabel", "tailport",
    "tailtarget", "tailtooltip", "target", "tooltip", "weight",
    "rank"
}


NODE_ATTRIBUTES = {
    "URL", "color", "colorscheme", "comment",
    "distortion", "fillcolor", "fixedsize", "fontcolor", "fontname",
    "fontsize", "group", "height", "id", "image", "imagescale", "label",
    "labelloc", "layer", "margin", "nojustify", "orientation", "penwidth",
    "peripheries", "pin", "pos", "rects", "regular", "root", "samplepoints",
    "shape", "shapefile", "showboxes", "sides", "skew", "sortv", "style",
    "target", "tooltip", "vertices", "width", "z",
    # The following are attributes dot2tex
    "texlbl",  "texmode"
}


CLUSTER_ATTRIBUTES = {
    "K", "URL", "bgcolor", "color", "colorscheme",
    "fillcolor", "fontcolor", "fontname", "fontsize", "label", "labeljust",
    "labelloc", "lheight", "lp", "lwidth", "nojustify", "pencolor",
    "penwidth", "peripheries", "sortv", "style", "target", "tooltip"
}
# fmt: on


OUTPUT_FORMATS = {
    "canon",
    "cmap",
    "cmapx",
    "cmapx_np",
    "dia",
    "dot",
    "fig",
    "gd",
    "gd2",
    "gif",
    "hpgl",
    "imap",
    "imap_np",
    "ismap",
    "jpe",
    "jpeg",
    "jpg",
    "mif",
    "mp",
    "pcl",
    "pdf",
    "pic",
    "plain",
    "plain-ext",
    "png",
    "ps",
    "ps2",
    "svg",
    "svgz",
    "vml",
    "vmlz",
    "vrml",
    "vtx",
    "wbmp",
    "xdot",
    "xlib",
}


DEFAULT_PROGRAMS = {
    "dot",
    "twopi",
    "neato",
    "circo",
    "fdp",
    "sfdp",
}


def __generate_attribute_methods(Klass, attrs):
    """Generate setter and getter methods for attributes."""
    for attr in attrs:
        # Generate all the Getter methods.
        #
        def __getter(self, _attr=attr):
            return self.get(_attr)

        setattr(Klass, f"get_{attr}", __getter)

        # Generate all the Setter methods.
        #
        def __setter(self, *args, _attr=attr):
            return self.set(_attr, *args)

        setattr(Klass, f"set_{attr}", __setter)


def __generate_format_methods(Klass):
    """Generate create_ and write_ methods for formats."""
    # Automatically creates all
    # the methods enabling the creation
    # of output in any of the supported formats.
    for frmt in OUTPUT_FORMATS:

        def __create_method(self, f=frmt, prog=None, encoding=None):
            """Refer to docstring of method `create`."""
            return self.create(format=f, prog=prog, encoding=encoding)

        setattr(Klass, f"create_{frmt}", __create_method)

    for frmt in OUTPUT_FORMATS ^ {"raw"}:

        def __write_method(self, path, f=frmt, prog=None, encoding=None):
            """Refer to docstring of method `write`."""
            self.write(path, format=f, prog=prog, encoding=encoding)

        setattr(Klass, f"write_{frmt}", __write_method)


def is_windows():
    # type: () -> bool
    return os.name == "nt"


def is_anaconda():
    # type: () -> bool
    import glob

    conda_pattern = os.path.join(sys.prefix, "conda-meta\\graphviz*.json")
    return glob.glob(conda_pattern) != []


def get_executable_extension():
    # type: () -> str
    if is_windows():
        return ".bat" if is_anaconda() else ".exe"
    else:
        return ""


def call_graphviz(program, arguments, working_dir, **kwargs):
    # explicitly inherit `$PATH`, on Windows too,
    # with `shell=False`

    if program in DEFAULT_PROGRAMS:
        extension = get_executable_extension()
        program += extension

    if arguments is None:
        arguments = []

    env = {
        "PATH": os.environ.get("PATH", ""),
        "LD_LIBRARY_PATH": os.environ.get("LD_LIBRARY_PATH", ""),
        "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
    }

    program_with_args = [program] + arguments

    process = subprocess.Popen(
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


#
# Extended version of ASPN's Python Cookbook Recipe:
# Frozen dictionaries.
# https://code.activestate.com/recipes/414283/
#
# This version freezes dictionaries used as values within dictionaries.
#
class frozendict(dict):
    def _blocked_attribute(obj):
        raise AttributeError("A frozendict cannot be modified.")

    _blocked_attribute = property(_blocked_attribute)

    __delitem__ = __setitem__ = clear = _blocked_attribute
    pop = popitem = setdefault = update = _blocked_attribute

    def __new__(cls, *args, **kw):
        new = dict.__new__(cls)

        args_ = []
        for arg in args:
            if isinstance(arg, dict):
                arg = copy.copy(arg)
                for k in arg:
                    v = arg[k]
                    if isinstance(v, frozendict):
                        arg[k] = v
                    elif isinstance(v, dict):
                        arg[k] = frozendict(v)
                    elif isinstance(v, list):
                        v_ = []
                        for elm in v:
                            if isinstance(elm, dict):
                                v_.append(frozendict(elm))
                            else:
                                v_.append(elm)
                        arg[k] = tuple(v_)
                args_.append(arg)
            else:
                args_.append(arg)

        dict.__init__(new, *args_, **kw)
        return new

    def __init__(self, *args, **kw):
        pass

    def __hash__(self):
        try:
            return self._cached_hash
        except AttributeError:
            h = self._cached_hash = hash(tuple(sorted(self.items())))
            return h

    def __repr__(self):
        dict_repr = dict.__repr__(self)
        return f"frozendict({dict_repr})"


def make_quoted(s):
    """Transform a string into a quoted string, escaping specials."""
    replace = {
        ord('"'): r"\"",
        ord("\n"): r"\n",
        ord("\r"): r"\r",
    }
    return rf'"{s.translate(replace)}"'


dot_keywords = ["graph", "subgraph", "digraph", "node", "edge", "strict"]

re_all_numeric = re.compile(r"^[0-9\.]+$")
re_dbl_quoted = re.compile(r'^".*"$', re.S)
re_html = re.compile(r"^<.*>$", re.S)

id_re_alpha_nums = re.compile(r"^[_a-zA-Z][a-zA-Z0-9_]*$")
id_re_alpha_nums_with_ports = re.compile(
    r'^[_a-zA-Z][a-zA-Z0-9_:"]*[a-zA-Z0-9_"]+$'
)
id_re_with_port = re.compile(r"^([^:]*):([^:]*)$")


def any_needs_quotes(s):
    """Determine if a string needs to be quoted.

    Returns True, False, or None if the result is indeterminate.
    """

    # Strings consisting _only_ of digits are safe unquoted
    if s.isdigit():
        return False

    # MIXED-aphanumeric values need quoting if they *start* with a digit
    if s.isalnum():
        return s[0].isdigit()

    has_high_chars = any(ord(c) > 0x7F or ord(c) == 0 for c in s)
    if has_high_chars and not re_dbl_quoted.match(s) and not re_html.match(s):
        return True

    for test_re in [re_all_numeric, re_dbl_quoted, re_html]:
        if test_re.match(s):
            return False

    return None


def id_needs_quotes(s):
    """Checks whether a string is a dot language ID.

    It will check whether the string is solely composed
    by the characters allowed in an ID or not.
    If the string is one of the reserved keywords it will
    need quotes too but the user will need to add them
    manually.
    """

    # If the name is a reserved keyword it will need quotes but pydot
    # can't tell when it's being used as a keyword or when it's simply
    # a name. Hence the user needs to supply the quotes when an element
    # would use a reserved keyword as name. This function will return
    # false indicating that a keyword string, if provided as-is, won't
    # need quotes.
    if s in dot_keywords:
        return False

    any_result = any_needs_quotes(s)
    if any_result is not None:
        return any_result

    for test_re in [
        id_re_alpha_nums,
        id_re_alpha_nums_with_ports,
    ]:
        if test_re.match(s):
            return False

    m = id_re_with_port.match(s)
    if m:
        return id_needs_quotes(m.group(1)) or id_needs_quotes(m.group(2))

    return True


def quote_id_if_necessary(s, unquoted_keywords=None):
    """Enclose identifier in quotes, if needed."""
    unquoted = [
        w.lower() for w in list(unquoted_keywords if unquoted_keywords else [])
    ]

    if isinstance(s, bool):
        return str(s).lower()
    if not isinstance(s, str):
        return s
    if not s:
        return s

    if s.lower() in unquoted:
        return s
    if s.lower() in dot_keywords:
        return make_quoted(s)

    if id_needs_quotes(s):
        return make_quoted(s)

    return s


def quote_attr_if_necessary(s):
    """Enclose attribute value in quotes, if needed."""
    if isinstance(s, bool):
        return str(s).lower()

    if not isinstance(s, str):
        return s

    if s in dot_keywords:
        return make_quoted(s)

    any_result = any_needs_quotes(s)
    if any_result is not None and not any_result:
        return s

    return make_quoted(s)


def graph_from_dot_data(s):
    """Load graphs from DOT description in string `s`.

    This function is NOT thread-safe due to the internal use of `pyparsing`.
    Use a lock if needed.

    @param s: string in [DOT language](
        https://en.wikipedia.org/wiki/DOT_(graph_description_language))

    @return: Graphs that result from parsing.
    @rtype: `list` of `pydot.Dot`
    """
    return pydot.dot_parser.parse_dot_data(s)


def graph_from_dot_file(path, encoding=None):
    """Load graphs from DOT file at `path`.

    This function is NOT thread-safe due to the internal use of `pyparsing`.
    Use a lock if needed.

    @param path: to DOT file
    @param encoding: as passed to `io.open`.
        For example, `'utf-8'`.

    @return: Graphs that result from parsing.
    @rtype: `list` of `pydot.Dot`
    """
    with open(path, encoding=encoding) as f:
        s = f.read()
    graphs = graph_from_dot_data(s)
    return graphs


def graph_from_edges(edge_list, node_prefix="", directed=False):
    """Creates a basic graph out of an edge list.

    The edge list has to be a list of tuples representing
    the nodes connected by the edge.
    The values can be anything: bool, int, float, str.

    If the graph is undirected by default, it is only
    calculated from one of the symmetric halves of the matrix.
    """

    if directed:
        graph = Dot(graph_type="digraph")

    else:
        graph = Dot(graph_type="graph")

    for edge in edge_list:
        if isinstance(edge[0], str):
            src = node_prefix + edge[0]
        else:
            src = node_prefix + str(edge[0])

        if isinstance(edge[1], str):
            dst = node_prefix + edge[1]
        else:
            dst = node_prefix + str(edge[1])

        e = Edge(src, dst)
        graph.add_edge(e)

    return graph


def graph_from_adjacency_matrix(matrix, node_prefix="", directed=False):
    """Creates a basic graph out of an adjacency matrix.

    The matrix has to be a list of rows of values
    representing an adjacency matrix.
    The values can be anything: bool, int, float, as long
    as they can evaluate to True or False.
    """

    node_orig = 1

    if directed:
        graph = Dot(graph_type="digraph")
    else:
        graph = Dot(graph_type="graph")

    for row in matrix:
        if not directed:
            skip = matrix.index(row)
            r = row[skip:]
        else:
            skip = 0
            r = row
        node_dest = skip + 1

        for e in r:
            if e:
                graph.add_edge(
                    Edge(
                        f"{node_prefix}{node_orig}",
                        f"{node_prefix}{node_dest}",
                    )
                )
            node_dest += 1
        node_orig += 1

    return graph


def graph_from_incidence_matrix(matrix, node_prefix="", directed=False):
    """Creates a basic graph out of an incidence matrix.

    The matrix has to be a list of rows of values
    representing an incidence matrix.
    The values can be anything: bool, int, float, as long
    as they can evaluate to True or False.
    """

    if directed:
        graph = Dot(graph_type="digraph")
    else:
        graph = Dot(graph_type="graph")

    for row in matrix:
        nodes = []
        c = 1

        for node in row:
            if node:
                nodes.append(c * node)
            c += 1
            nodes.sort()

        if len(nodes) == 2:
            graph.add_edge(
                Edge(
                    f"{node_prefix}{abs(nodes[0])}",
                    f"{node_prefix}{nodes[1]}",
                )
            )

    if not directed:
        graph.set_simplify(True)

    return graph


class Common:
    """Common information to several classes.

    Should not be directly used, several classes are derived from
    this one.
    """

    def __getstate__(self):
        dict = copy.copy(self.obj_dict)
        return dict

    def __setstate__(self, state):
        self.obj_dict = state

    def __get_attribute__(self, attr):
        """Look for default attributes for this node"""

        attr_val = self.obj_dict["attributes"].get(attr, None)
        if attr_val is None:
            # get the defaults for nodes/edges

            default_node_name = self.obj_dict["type"]

            # The defaults for graphs are set on a node named 'graph'
            if default_node_name in ("subgraph", "digraph", "cluster"):
                default_node_name = "graph"

            g = self.get_parent_graph()
            if g is not None:
                defaults = g.get_node(default_node_name)
            else:
                return None

            # Multiple defaults could be set by having repeated 'graph [...]'
            # 'node [...]', 'edge [...]' statements. In such case, if the
            # same attribute is set in different statements, only the first
            # will be returned. In order to get all, one would call the
            # get_*_defaults() methods and handle those. Or go node by node
            # (of the ones specifying defaults) and modify the attributes
            # individually.
            #
            if not isinstance(defaults, (list, tuple)):
                defaults = [defaults]

            for default in defaults:
                attr_val = default.obj_dict["attributes"].get(attr, None)
                if attr_val:
                    return attr_val
        else:
            return attr_val

        return None

    def set_parent_graph(self, parent_graph):
        self.obj_dict["parent_graph"] = parent_graph

    def get_parent_graph(self):
        return self.obj_dict.get("parent_graph", None)

    def get_top_graph_type(self):
        """Find the topmost parent graph type for the current object."""
        parent = self.get_parent_graph()
        if parent is None:
            return None
        while True:
            parent_ = parent.get_parent_graph()
            if parent_ == parent:
                break
            parent = parent_

        return parent.obj_dict["type"]

    def set(self, name, value):
        """Set an attribute value by name.

        Given an attribute 'name' it will set its value to 'value'.
        There's always the possibility of using the methods:

            set_'name'(value)

        which are defined for all the existing attributes.
        """
        self.obj_dict["attributes"][name] = value

    def get(self, name):
        """Get an attribute value by name.

        Given an attribute 'name' it will get its value.
        There's always the possibility of using the methods:

            get_'name'()

        which are defined for all the existing attributes.
        """
        return self.obj_dict["attributes"].get(name, None)

    def get_attributes(self):
        """Get attributes of the object"""
        return self.obj_dict["attributes"]

    def set_sequence(self, seq):
        """Set sequence"""
        self.obj_dict["sequence"] = seq

    def get_sequence(self):
        """Get sequence"""
        return self.obj_dict["sequence"]

    @staticmethod
    def get_indent(indent, indent_level):
        if isinstance(indent, (int, float)):
            indent_str = " " * int(indent)
        else:
            indent_str = str(indent)
        return indent_str * indent_level

    @staticmethod
    def _format_attr(key: str, value):
        """Turn a key-value pair into an attribute, properly quoted."""
        if value == "":
            value = '""'
        if value is not None:
            return f"{key}={quote_attr_if_necessary(value)}"
        return key

    def formatted_attr_list(self):
        """Return a list of the class's attributes as formatted strings."""
        return [
            self._format_attr(k, v)
            for k, v in self.obj_dict["attributes"].items()
        ]

    def attrs_string(self, prefix=""):
        """Format the current attributes list for output.

        The `prefix` string will be prepended if and only if some
        output is generated."""
        attrs = self.formatted_attr_list()
        if not attrs:
            return ""
        return f"{prefix}[{', '.join(attrs)}]"


class Node(Common):
    """A graph node.

    This class represents a graph's node with all its attributes.

    node(name, attribute=value, ...)

    name: node's name

    All the attributes defined in the Graphviz dot language should
    be supported.
    """

    def __init__(self, name="", obj_dict=None, **attrs):
        #
        # Nodes will take attributes of
        # all other types because the defaults
        # for any GraphViz object are dealt with
        # as if they were Node definitions
        #
        if obj_dict is not None:
            self.obj_dict = obj_dict

        else:
            self.obj_dict = {}

            # Copy the attributes
            #
            self.obj_dict["attributes"] = dict(attrs)
            self.obj_dict["type"] = "node"
            self.obj_dict["parent_graph"] = None
            self.obj_dict["sequence"] = None

            # Remove the compass point
            #
            port = None
            if isinstance(name, str) and not name.startswith('"'):
                idx = name.find(":")
                if idx > 0 and idx + 1 < len(name):
                    name, port = name[:idx], name[idx:]

            if isinstance(name, int):
                name = str(name)

            self.obj_dict["name"] = name
            self.obj_dict["port"] = port

    def __str__(self):
        return self.to_string()

    def set_name(self, node_name):
        """Set the node's name."""
        self.obj_dict["name"] = node_name

    def get_name(self):
        """Get the node's name."""
        return self.obj_dict["name"]

    def get_port(self):
        """Get the node's port."""
        return self.obj_dict["port"]

    def add_style(self, style):
        styles = self.obj_dict["attributes"].get("style", None)
        if not styles and style:
            styles = [style]
        else:
            styles = styles.split(",")
            styles.append(style)

        self.obj_dict["attributes"]["style"] = ",".join(styles)

    def to_string(self, indent="", indent_level=1):
        """Return string representation of node in DOT language."""
        indent_str = self.get_indent(indent, indent_level)

        node = quote_id_if_necessary(
            self.obj_dict["name"], unquoted_keywords=("graph", "node", "edge")
        )

        # No point in having default nodes that don't set any attributes...
        if (
            node in ("graph", "node", "edge")
            and len(self.obj_dict.get("attributes", {})) == 0
        ):
            return ""

        return f"{indent_str}{node}{self.attrs_string(prefix=' ')};"


__generate_attribute_methods(Node, NODE_ATTRIBUTES)


class Edge(Common):
    """A graph edge.

    This class represents a graph's edge with all its attributes.

    edge(src, dst, attribute=value, ...)

    src: source node, subgraph or cluster
    dst: destination node, subgraph or cluster

    `src` and `dst` can be specified as a `Node`, `Subgraph` or
    `Cluster` object, or as the name string of such a component.

    All the attributes defined in the Graphviz dot language should
    be supported.

    Attributes can be set through the dynamically generated methods:

     set_[attribute name], i.e. set_label, set_fontname

    or directly by using the instance's special dictionary:

     Edge.obj_dict['attributes'][attribute name], i.e.

        edge_instance.obj_dict['attributes']['label']
        edge_instance.obj_dict['attributes']['fontname']

    """

    def __init__(self, src="", dst="", obj_dict=None, **attrs):
        self.obj_dict = {}
        if isinstance(src, (Node, Subgraph, Cluster)):
            src = src.get_name()
        if isinstance(dst, (Node, Subgraph, Cluster)):
            dst = dst.get_name()
        points = (src, dst)
        self.obj_dict["points"] = points
        if obj_dict is None:
            # Copy the attributes
            self.obj_dict["attributes"] = dict(attrs)
            self.obj_dict["type"] = "edge"
            self.obj_dict["parent_graph"] = None
            self.obj_dict["sequence"] = None
        else:
            self.obj_dict = obj_dict

    def __str__(self):
        return self.to_string()

    def get_source(self):
        """Get the edges source node name."""
        return self.obj_dict["points"][0]

    def get_destination(self):
        """Get the edge's destination node name."""
        return self.obj_dict["points"][1]

    def __hash__(self):
        return hash(hash(self.get_source()) + hash(self.get_destination()))

    def __eq__(self, edge):
        """Compare two edges.

        If the parent graph is directed, arcs linking
        node A to B are considered equal and A->B != B->A

        If the parent graph is undirected, any edge
        connecting two nodes is equal to any other
        edge connecting the same nodes, A->B == B->A
        """

        if not isinstance(edge, Edge):
            raise pydot.Error("Can not compare an edge to a non-edge object.")

        if self.get_top_graph_type() == "graph":
            # If the graph is undirected, the edge has neither
            # source nor destination.
            #
            if (
                self.get_source() == edge.get_source()
                and self.get_destination() == edge.get_destination()
            ) or (
                edge.get_source() == self.get_destination()
                and edge.get_destination() == self.get_source()
            ):
                return True

        else:
            if (
                self.get_source() == edge.get_source()
                and self.get_destination() == edge.get_destination()
            ):
                return True

        return False

    def parse_node_ref(self, node_str):
        if not isinstance(node_str, str):
            return node_str

        if node_str.startswith('"') and node_str.endswith('"'):
            return node_str

        node_port_idx = node_str.rfind(":")

        if (
            node_port_idx > 0
            and node_str[0] == '"'
            and node_str[node_port_idx - 1] == '"'
        ):
            return node_str

        if node_port_idx > 0:
            a = node_str[:node_port_idx]
            b = node_str[node_port_idx + 1 :]

            node = quote_id_if_necessary(a)
            node += ":" + quote_id_if_necessary(b)

            return node

        return quote_id_if_necessary(node_str)

    def to_string(self, indent="", indent_level=1):
        """Return string representation of edge in DOT language."""
        src = self.parse_node_ref(self.get_source())
        dst = self.parse_node_ref(self.get_destination())

        indent_str = self.get_indent(indent, indent_level)

        if isinstance(src, frozendict):
            sgraph = Subgraph(obj_dict=src)
            edge = [
                sgraph.to_string(
                    indent=indent, indent_level=indent_level, inline=True
                )
            ]
        elif isinstance(src, int):
            edge = [str(src)]
        else:
            edge = [src]

        if self.get_top_graph_type() == "digraph":
            edge.append("->")
        else:
            edge.append("--")

        if isinstance(dst, frozendict):
            sgraph = Subgraph(obj_dict=dst)
            edge.append(
                sgraph.to_string(
                    indent=indent, indent_level=indent_level, inline=True
                )
            )
        elif isinstance(dst, int):
            edge.append(str(dst))
        else:
            edge.append(dst)

        return f"{indent_str}{' '.join(edge)}{self.attrs_string(prefix=' ')};"


__generate_attribute_methods(Edge, EDGE_ATTRIBUTES)


class Graph(Common):
    """Class representing a graph in Graphviz's dot language.

    This class implements the methods to work on a representation
    of a graph in Graphviz's dot language.

    graph(  graph_name='G', graph_type='digraph',
        strict=False, suppress_disconnected=False, attribute=value, ...)

    graph_name:
        the graph's name
    graph_type:
        can be 'graph' or 'digraph'
    suppress_disconnected:
        defaults to False, which will remove from the
        graph any disconnected nodes.
    simplify:
        if True it will avoid displaying equal edges, i.e.
        only one edge between two nodes. removing the
        duplicated ones.

    All the attributes defined in the Graphviz dot language should
    be supported.

    Attributes can be set through the dynamically generated methods:

     set_[attribute name], i.e. set_size, set_fontname

    or using the instance's attributes:

     Graph.obj_dict['attributes'][attribute name], i.e.

        graph_instance.obj_dict['attributes']['label']
        graph_instance.obj_dict['attributes']['fontname']
    """

    def __init__(
        self,
        graph_name="G",
        obj_dict=None,
        graph_type="digraph",
        strict=False,
        suppress_disconnected=False,
        simplify=False,
        **attrs,
    ):
        if obj_dict is not None:
            self.obj_dict = obj_dict

        else:
            self.obj_dict = {}

            self.obj_dict["attributes"] = dict(attrs)

            if graph_type not in ["graph", "digraph"]:
                raise pydot.Error(
                    f'Invalid type "{graph_type}". '
                    "Accepted graph types are: graph, digraph"
                )

            self.obj_dict["name"] = graph_name
            self.obj_dict["type"] = graph_type

            self.obj_dict["strict"] = strict
            self.obj_dict["suppress_disconnected"] = suppress_disconnected
            self.obj_dict["simplify"] = simplify

            self.obj_dict["current_child_sequence"] = 1
            self.obj_dict["nodes"] = {}
            self.obj_dict["edges"] = {}
            self.obj_dict["subgraphs"] = {}

            self.set_parent_graph(self)

    def __str__(self):
        return self.to_string()

    def get_graph_type(self):
        return self.obj_dict["type"]

    def set_graph_defaults(self, **attrs):
        self.add_node(Node("graph", **attrs))

    def get_graph_defaults(self, **attrs):
        graph_nodes = self.get_node("graph")

        if isinstance(graph_nodes, (list, tuple)):
            return [node.get_attributes() for node in graph_nodes]

        return graph_nodes.get_attributes()

    def set_node_defaults(self, **attrs):
        """Define default node attributes.

        These attributes only apply to nodes added to the graph after
        calling this method.
        """
        self.add_node(Node("node", **attrs))

    def get_node_defaults(self, **attrs):
        graph_nodes = self.get_node("node")

        if isinstance(graph_nodes, (list, tuple)):
            return [node.get_attributes() for node in graph_nodes]

        return graph_nodes.get_attributes()

    def set_edge_defaults(self, **attrs):
        self.add_node(Node("edge", **attrs))

    def get_edge_defaults(self, **attrs):
        graph_nodes = self.get_node("edge")

        if isinstance(graph_nodes, (list, tuple)):
            return [node.get_attributes() for node in graph_nodes]

        return graph_nodes.get_attributes()

    def set_simplify(self, simplify):
        """Set whether to simplify or not.

        If True it will avoid displaying equal edges, i.e.
        only one edge between two nodes. removing the
        duplicated ones.
        """
        self.obj_dict["simplify"] = simplify

    def get_simplify(self):
        """Get whether to simplify or not.

        Refer to set_simplify for more information.
        """
        return self.obj_dict["simplify"]

    def set_type(self, graph_type):
        """Set the graph's type, 'graph' or 'digraph'."""
        self.obj_dict["type"] = graph_type

    def get_type(self):
        """Get the graph's type, 'graph' or 'digraph'."""
        return self.obj_dict["type"]

    def set_name(self, graph_name):
        """Set the graph's name."""
        self.obj_dict["name"] = graph_name

    def get_name(self):
        """Get the graph's name."""
        return self.obj_dict["name"]

    def set_strict(self, val):
        """Set graph to 'strict' mode.

        This option is only valid for top level graphs.
        """
        self.obj_dict["strict"] = val

    def get_strict(self, val):
        """Get graph's 'strict' mode (True, False).

        This option is only valid for top level graphs.
        """
        return self.obj_dict["strict"]

    def set_suppress_disconnected(self, val):
        """Suppress disconnected nodes in the output graph.

        This option will skip nodes in
        the graph with no incoming or outgoing
        edges. This option works also
        for subgraphs and has effect only in the
        current graph/subgraph.
        """
        self.obj_dict["suppress_disconnected"] = val

    def get_suppress_disconnected(self, val):
        """Get if suppress disconnected is set.

        Refer to set_suppress_disconnected for more information.
        """
        return self.obj_dict["suppress_disconnected"]

    def get_next_sequence_number(self):
        seq = self.obj_dict["current_child_sequence"]
        self.obj_dict["current_child_sequence"] += 1
        return seq

    def add_node(self, graph_node):
        """Adds a node object to the graph.

        It takes a node object as its only argument and returns
        None.
        """
        if not isinstance(graph_node, Node):
            raise TypeError(
                "add_node() received "
                + "a non node class object: "
                + str(graph_node)
            )

        node = self.get_node(graph_node.get_name())

        if not node:
            self.obj_dict["nodes"][graph_node.get_name()] = [
                graph_node.obj_dict
            ]
        else:
            self.obj_dict["nodes"][graph_node.get_name()].append(
                graph_node.obj_dict
            )

        if not node or graph_node.get_parent_graph() is None:
            graph_node.set_parent_graph(self.get_parent_graph())

        graph_node.set_sequence(self.get_next_sequence_number())

    def del_node(self, name, index=None):
        """Delete a node from the graph.

        Given a node's name all node(s) with that same name
        will be deleted if 'index' is not specified or set
        to None.
        If there are several nodes with that same name and
        'index' is given, only the node in that position
        will be deleted.

        'index' should be an integer specifying the position
        of the node to delete. If index is larger than the
        number of nodes with that name, no action is taken.

        If nodes are deleted it returns True. If no action
        is taken it returns False.
        """
        if isinstance(name, Node):
            name = name.get_name()

        if name in self.obj_dict["nodes"]:
            if index is not None and index < len(self.obj_dict["nodes"][name]):
                del self.obj_dict["nodes"][name][index]
                return True
            else:
                del self.obj_dict["nodes"][name]
                return True

        return False

    def get_node(self, name):
        """Retrieve a node from the graph.

        Given a node's name the corresponding Node
        instance will be returned.

        If one or more nodes exist with that name a list of
        Node instances is returned.
        An empty list is returned otherwise.
        """
        match = []

        if name in self.obj_dict["nodes"]:
            match.extend(
                [
                    Node(obj_dict=obj_dict)
                    for obj_dict in self.obj_dict["nodes"][name]
                ]
            )

        return match

    def get_nodes(self):
        """Get the list of Node instances."""
        return self.get_node_list()

    def get_node_list(self):
        """Get the list of Node instances.

        This method returns the list of Node instances
        composing the graph.
        """
        node_objs = []

        for node in self.obj_dict["nodes"]:
            obj_dict_list = self.obj_dict["nodes"][node]
            node_objs.extend([Node(obj_dict=obj_d) for obj_d in obj_dict_list])

        return node_objs

    def add_edge(self, graph_edge):
        """Adds an edge object to the graph.

        It takes a edge object as its only argument and returns
        None.
        """
        if not isinstance(graph_edge, Edge):
            raise TypeError(
                "add_edge() received a non edge class object: "
                + str(graph_edge)
            )

        edge_points = (graph_edge.get_source(), graph_edge.get_destination())

        if edge_points in self.obj_dict["edges"]:
            edge_list = self.obj_dict["edges"][edge_points]
            edge_list.append(graph_edge.obj_dict)
        else:
            self.obj_dict["edges"][edge_points] = [graph_edge.obj_dict]

        graph_edge.set_sequence(self.get_next_sequence_number())
        graph_edge.set_parent_graph(self.get_parent_graph())

    def del_edge(self, src_or_list, dst=None, index=None):
        """Delete an edge from the graph.

        Given an edge's (source, destination) node names all
        matching edges(s) will be deleted if 'index' is not
        specified or set to None.
        If there are several matching edges and 'index' is
        given, only the edge in that position will be deleted.

        'index' should be an integer specifying the position
        of the edge to delete. If index is larger than the
        number of matching edges, no action is taken.

        If edges are deleted it returns True. If no action
        is taken it returns False.
        """
        if isinstance(src_or_list, (list, tuple)):
            if dst is not None and isinstance(dst, int):
                index = dst
            src, dst = src_or_list
        else:
            src, dst = src_or_list, dst

        if isinstance(src, Node):
            src = src.get_name()

        if isinstance(dst, Node):
            dst = dst.get_name()

        if (src, dst) in self.obj_dict["edges"]:
            if index is not None and index < len(
                self.obj_dict["edges"][(src, dst)]
            ):
                del self.obj_dict["edges"][(src, dst)][index]
                return True
            else:
                del self.obj_dict["edges"][(src, dst)]
                return True

        return False

    def get_edge(self, src_or_list, dst=None):
        """Retrieved an edge from the graph.

        Given an edge's source and destination the corresponding
        Edge instance(s) will be returned.

        If one or more edges exist with that source and destination
        a list of Edge instances is returned.
        An empty list is returned otherwise.
        """
        if isinstance(src_or_list, (list, tuple)) and dst is None:
            edge_points = tuple(src_or_list)
            edge_points_reverse = (edge_points[1], edge_points[0])
        else:
            edge_points = (src_or_list, dst)
            edge_points_reverse = (dst, src_or_list)

        match = []

        if edge_points in self.obj_dict["edges"] or (
            self.get_top_graph_type() == "graph"
            and edge_points_reverse in self.obj_dict["edges"]
        ):
            edges_obj_dict = self.obj_dict["edges"].get(
                edge_points,
                self.obj_dict["edges"].get(edge_points_reverse, None),
            )

            for edge_obj_dict in edges_obj_dict:
                match.append(
                    Edge(
                        edge_points[0], edge_points[1], obj_dict=edge_obj_dict
                    )
                )

        return match

    def get_edges(self):
        return self.get_edge_list()

    def get_edge_list(self):
        """Get the list of Edge instances.

        This method returns the list of Edge instances
        composing the graph.
        """
        edge_objs = []

        for edge in self.obj_dict["edges"]:
            obj_dict_list = self.obj_dict["edges"][edge]
            edge_objs.extend([Edge(obj_dict=obj_d) for obj_d in obj_dict_list])

        return edge_objs

    def add_subgraph(self, sgraph):
        """Adds an subgraph object to the graph.

        It takes a subgraph object as its only argument and returns
        None.
        """
        if not isinstance(sgraph, Subgraph) and not isinstance(
            sgraph, Cluster
        ):
            raise TypeError(
                "add_subgraph() received a non subgraph class object:"
                + str(sgraph)
            )

        if sgraph.get_name() in self.obj_dict["subgraphs"]:
            sgraph_list = self.obj_dict["subgraphs"][sgraph.get_name()]
            sgraph_list.append(sgraph.obj_dict)

        else:
            self.obj_dict["subgraphs"][sgraph.get_name()] = [sgraph.obj_dict]

        sgraph.set_sequence(self.get_next_sequence_number())
        sgraph.set_parent_graph(self.get_parent_graph())

    def get_subgraph(self, name):
        """Retrieved a subgraph from the graph.

        Given a subgraph's name the corresponding
        Subgraph instance will be returned.

        If one or more subgraphs exist with the same name, a list of
        Subgraph instances is returned.
        An empty list is returned otherwise.
        """
        match = []

        if name in self.obj_dict["subgraphs"]:
            sgraphs_obj_dict = self.obj_dict["subgraphs"].get(name)

            for obj_dict_list in sgraphs_obj_dict:
                match.append(Subgraph(obj_dict=obj_dict_list))

        return match

    def get_subgraphs(self):
        return self.get_subgraph_list()

    def get_subgraph_list(self):
        """Get the list of Subgraph instances.

        This method returns the list of Subgraph instances
        in the graph.
        """
        sgraph_objs = []

        for sgraph in self.obj_dict["subgraphs"]:
            obj_dict_list = self.obj_dict["subgraphs"][sgraph]
            sgraph_objs.extend(
                [Subgraph(obj_dict=obj_d) for obj_d in obj_dict_list]
            )

        return sgraph_objs

    def set_parent_graph(self, parent_graph):
        self.obj_dict["parent_graph"] = parent_graph

        for k in self.obj_dict["nodes"]:
            obj_list = self.obj_dict["nodes"][k]
            for obj in obj_list:
                obj["parent_graph"] = parent_graph

        for k in self.obj_dict["edges"]:
            obj_list = self.obj_dict["edges"][k]
            for obj in obj_list:
                obj["parent_graph"] = parent_graph

        for k in self.obj_dict["subgraphs"]:
            obj_list = self.obj_dict["subgraphs"][k]
            for obj in obj_list:
                Graph(obj_dict=obj).set_parent_graph(parent_graph)

    def to_string(self, indent="", indent_level=0, inline=False):
        """Return string representation of graph in DOT language.

        @return: graph and subelements
        @rtype: `str`
        """
        indent_str = self.get_indent(indent, indent_level)
        child_indent = self.get_indent(indent, indent_level + 1)

        graph = []

        if not inline:
            graph.append(indent_str)

        first_line = []

        if self == self.get_parent_graph() and self.obj_dict.get(
            "strict", False
        ):
            first_line.append("strict")

        graph_type = self.obj_dict["type"]
        if graph_type != "subgraph" or self.obj_dict.get("show_keyword", True):
            first_line.append(graph_type)

            # Suppressing the keyword hides the name as well
            graph_name = self.obj_dict.get("name")
            if graph_name:
                first_line.append(quote_id_if_necessary(graph_name))

        first_line.append("{\n")
        graph.append(" ".join(first_line))

        graph.extend(
            f"{child_indent}{a};\n" for a in self.formatted_attr_list()
        )

        edges_done = set()

        edge_obj_dicts = []
        for k in self.obj_dict["edges"]:
            edge_obj_dicts.extend(self.obj_dict["edges"][k])

        if edge_obj_dicts:
            edge_src_set, edge_dst_set = list(
                zip(*[obj["points"] for obj in edge_obj_dicts])
            )
            edge_src_set, edge_dst_set = set(edge_src_set), set(edge_dst_set)
        else:
            edge_src_set, edge_dst_set = set(), set()

        node_obj_dicts = []
        for k in self.obj_dict["nodes"]:
            node_obj_dicts.extend(self.obj_dict["nodes"][k])

        sgraph_obj_dicts = []
        for k in self.obj_dict["subgraphs"]:
            sgraph_obj_dicts.extend(self.obj_dict["subgraphs"][k])

        obj_list = [
            (obj["sequence"], obj)
            for obj in (edge_obj_dicts + node_obj_dicts + sgraph_obj_dicts)
        ]
        obj_list.sort(key=lambda x: x[0])

        for idx, obj in obj_list:
            if obj["type"] == "node":
                node = Node(obj_dict=obj)

                if self.obj_dict.get("suppress_disconnected", False):
                    if (
                        node.get_name() not in edge_src_set
                        and node.get_name() not in edge_dst_set
                    ):
                        continue

                node_str = node.to_string(
                    indent=indent, indent_level=indent_level + 1
                )
                graph.append(f"{node_str}\n")

            elif obj["type"] == "edge":
                edge = Edge(obj_dict=obj)

                if self.obj_dict.get("simplify", False) and edge in edges_done:
                    continue

                edge_str = edge.to_string(
                    indent=indent, indent_level=indent_level + 1
                )
                graph.append(f"{edge_str}\n")
                edges_done.add(edge)

            else:
                sgraph_str = Subgraph(obj_dict=obj).to_string(
                    indent=indent, indent_level=indent_level + 1
                )
                graph.append(f"{sgraph_str}\n")

        graph.append(f"{indent_str}}}")
        if not inline:
            graph.append("\n")

        return "".join(graph)


__generate_attribute_methods(Graph, GRAPH_ATTRIBUTES)


class Subgraph(Graph):
    """Class representing a subgraph in Graphviz's dot language.

    This class implements the methods to work on a representation
    of a subgraph in Graphviz's dot language.

    subgraph(graph_name='subG',
             suppress_disconnected=False,
             attribute=value,
             ...)

    graph_name:
        the subgraph's name
    suppress_disconnected:
        defaults to false, which will remove from the
        subgraph any disconnected nodes.
    All the attributes defined in the Graphviz dot language should
    be supported.

    Attributes can be set through the dynamically generated methods:

     set_[attribute name], i.e. set_size, set_fontname

    or using the instance's attributes:

     Subgraph.obj_dict['attributes'][attribute name], i.e.

        subgraph_instance.obj_dict['attributes']['label']
        subgraph_instance.obj_dict['attributes']['fontname']
    """

    # RMF: subgraph should have all the
    # attributes of graph so it can be passed
    # as a graph to all methods
    #
    def __init__(
        self,
        graph_name="",
        obj_dict=None,
        suppress_disconnected=False,
        simplify=False,
        **attrs,
    ):
        Graph.__init__(
            self,
            graph_name=graph_name,
            obj_dict=obj_dict,
            suppress_disconnected=suppress_disconnected,
            simplify=simplify,
            **attrs,
        )

        if obj_dict is None:
            self.obj_dict["type"] = "subgraph"


class Cluster(Graph):
    """Class representing a cluster in Graphviz's dot language.

    This class implements the methods to work on a representation
    of a cluster in Graphviz's dot language.

    cluster(graph_name='subG',
            suppress_disconnected=False,
            attribute=value,
            ...)

    graph_name:
        the cluster's name
        (the string 'cluster' will be always prepended)
    suppress_disconnected:
        defaults to false, which will remove from the
        cluster any disconnected nodes.
    All the attributes defined in the Graphviz dot language should
    be supported.

    Attributes can be set through the dynamically generated methods:

     set_[attribute name], i.e. set_color, set_fontname

    or using the instance's attributes:

     Cluster.obj_dict['attributes'][attribute name], i.e.

        cluster_instance.obj_dict['attributes']['label']
        cluster_instance.obj_dict['attributes']['fontname']
    """

    def __init__(
        self,
        graph_name="subG",
        obj_dict=None,
        suppress_disconnected=False,
        simplify=False,
        **attrs,
    ):
        Graph.__init__(
            self,
            graph_name=graph_name,
            obj_dict=obj_dict,
            suppress_disconnected=suppress_disconnected,
            simplify=simplify,
            **attrs,
        )

        if obj_dict is None:
            self.obj_dict["type"] = "subgraph"
            self.obj_dict["name"] = quote_id_if_necessary(
                "cluster_" + graph_name
            )


__generate_attribute_methods(Cluster, CLUSTER_ATTRIBUTES)


class Dot(Graph):
    """A container for handling a dot language file.

    This class implements methods to write and process
    a dot language file. It is a derived class of
    the base class 'Graph'.
    """

    def __init__(self, *argsl, **argsd):
        Graph.__init__(self, *argsl, **argsd)

        self.shape_files = []
        self.formats = OUTPUT_FORMATS
        self.prog = "dot"

    def __getstate__(self):
        state = {
            "obj_dict": copy.copy(self.obj_dict),
            "prog": self.prog,
            "shape_files": copy.deepcopy(self.shape_files),
            "formats": copy.copy(self.formats),
        }
        return state

    def __setstate__(self, state):
        if "obj_dict" not in state:
            # Backwards compatibility for old picklings
            state = {"obj_dict": state}
        self.obj_dict = state.get("obj_dict", {})
        self.prog = state.get("prog", "dot")
        self.shape_files = state.get("shape_files", [])
        self.formats = state.get("formats", OUTPUT_FORMATS)

    def set_shape_files(self, file_paths):
        """Add the paths of the required image files.

        If the graph needs graphic objects to
        be used as shapes or otherwise
        those need to be in the same folder as
        the graph is going to be rendered
        from. Alternatively the absolute path to
        the files can be specified when
        including the graphics in the graph.

        The files in the location pointed to by
        the path(s) specified as arguments
        to this method will be copied to
        the same temporary location where the
        graph is going to be rendered.
        """
        if isinstance(file_paths, str):
            self.shape_files.append(file_paths)

        if isinstance(file_paths, (list, tuple)):
            self.shape_files.extend(file_paths)

    def set_prog(self, prog):
        """Sets the default program.

        Sets the default program in charge of processing
        the dot file into a graph.
        """
        self.prog = prog

    def write(self, path, prog=None, format="raw", encoding=None):
        """Writes a graph to a file.

        Given a filename 'path' it will open/create and truncate
        such file and write on it a representation of the graph
        defined by the dot object in the format specified by
        'format' and using the encoding specified by `encoding` for text.
        The format 'raw' is used to dump the string representation
        of the Dot object, without further processing.
        The output can be processed by any of graphviz tools, defined
        in 'prog', which defaults to 'dot'
        Returns True or False according to the success of the write
        operation.

        There's also the preferred possibility of using:

            write_'format'(path, prog='program')

        which are automatically defined for all the supported formats.
        [write_ps(), write_gif(), write_dia(), ...]

        The encoding is passed to `open` [1].

        [1] https://docs.python.org/3/library/functions.html#open
        """
        if prog is None:
            prog = self.prog
        if format == "raw":
            s = self.to_string()
            with open(path, mode="w", encoding=encoding) as f:
                f.write(s)
        else:
            s = self.create(prog, format, encoding=encoding)
            with open(path, mode="wb") as f:
                f.write(s)
        return True

    def create(self, prog=None, format="ps", encoding=None):
        """Creates and returns a binary image for the graph.

        create will write the graph to a temporary dot file in the
        encoding specified by `encoding` and process it with the
        program given by 'prog' (which defaults to 'twopi'), reading
        the binary image output and return it as `bytes`.

        There's also the preferred possibility of using:

            create_'format'(prog='program')

        which are automatically defined for all the supported formats,
        for example:

          - `create_ps()`
          - `create_gif()`
          - `create_dia()`

        If 'prog' is a list, instead of a string,
        then the fist item is expected to be the program name,
        followed by any optional command-line arguments for it:

            [ 'twopi', '-Tdot', '-s10' ]


        @param prog: either:

          - name of GraphViz executable that
            can be found in the `$PATH`, or

          - absolute path to GraphViz executable.

          If you have added GraphViz to the `$PATH` and
          use its executables as installed
          (without renaming any of them)
          then their names are:

            - `'dot'`
            - `'twopi'`
            - `'neato'`
            - `'circo'`
            - `'fdp'`
            - `'sfdp'`

          On Windows, these have the notorious ".exe" extension that,
          only for the above strings, will be added automatically.

          The `$PATH` is inherited from `os.env['PATH']` and
          passed to `subprocess.Popen` using the `env` argument.

          If you haven't added GraphViz to your `$PATH` on Windows,
          then you may want to give the absolute path to the
          executable (for example, to `dot.exe`) in `prog`.
        """
        if prog is None:
            prog = self.prog

        assert prog is not None

        if isinstance(prog, (list, tuple)):
            prog, args = prog[0], prog[1:]
        else:
            args = []

        # temp file
        with tempfile.TemporaryDirectory(
            ignore_cleanup_errors=True
        ) as tmp_dir:
            fp = tempfile.NamedTemporaryFile(dir=tmp_dir, delete=False)
            fp.close()
            self.write(fp.name, encoding=encoding)

            # For each of the image files, copy it to the temporary directory
            # with the same filename as the original
            for img in self.shape_files:
                outfile = os.path.join(tmp_dir, os.path.basename(img))
                with open(img, "rb") as img_in, open(outfile, "wb") as img_out:
                    img_data = img_in.read()
                    img_out.write(img_data)

            arguments = [f"-T{format}"] + args + [fp.name]

            try:
                stdout_data, stderr_data, process = call_graphviz(
                    program=prog,
                    arguments=arguments,
                    working_dir=tmp_dir,
                )
            except OSError as e:
                if e.errno == errno.ENOENT:
                    args = list(e.args)
                    args[1] = f'"{prog}" not found in path.'
                    raise OSError(*args)
                else:
                    raise

        if process.returncode != 0:
            code = process.returncode
            print(
                f'"{prog}" with args {arguments} returned code: {code}\n\n'
                f"stdout, stderr:\n {stdout_data}\n{stderr_data}\n"
            )

        assert process.returncode == 0, (
            f'"{prog}" with args {arguments} '
            f"returned code: {process.returncode}"
        )

        return stdout_data


__generate_format_methods(Dot)
