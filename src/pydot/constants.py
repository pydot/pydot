# SPDX-FileCopyrightText: 2025 pydot contributors
#
# SPDX-License-Identifier: MIT

"""Constants used by Pydot."""

from __future__ import annotations

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
