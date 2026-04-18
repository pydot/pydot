# SPDX-FileCopyrightText: 2026 pydot contributors
#
# SPDX-License-Identifier: MIT

"""Mixin classes to define convenience methods."""

from __future__ import annotations

from typing import Any


class CommonMixin:
    """Attribute convenience methods for Common."""

    def get(self, name: str) -> Any:
        """Generic get method (must be reimplemented)."""
        raise NotImplementedError

    def set(self, name: str, value: Any) -> None:
        """Generic set method (must be reimplemented)."""
        raise NotImplementedError

    def get_URL(self) -> Any:
        """Get the ``URL`` attribute for the graph element."""
        return self.get("URL")

    def set_URL(self, value: Any) -> None:
        """Set the ``URL`` attribute for the graph element."""
        return self.set("URL", value)

    def get_colorscheme(self) -> Any:
        """Get the ``colorscheme`` attribute for the graph element."""
        return self.get("colorscheme")

    def set_colorscheme(self, value: Any) -> None:
        """Set the ``colorscheme`` attribute for the graph element."""
        return self.set("colorscheme", value)

    def get_fontcolor(self) -> Any:
        """Get the ``fontcolor`` attribute for the graph element."""
        return self.get("fontcolor")

    def set_fontcolor(self, value: Any) -> None:
        """Set the ``fontcolor`` attribute for the graph element."""
        return self.set("fontcolor", value)

    def get_fontname(self) -> Any:
        """Get the ``fontname`` attribute for the graph element."""
        return self.get("fontname")

    def set_fontname(self, value: Any) -> None:
        """Set the ``fontname`` attribute for the graph element."""
        return self.set("fontname", value)

    def get_fontsize(self) -> Any:
        """Get the ``fontsize`` attribute for the graph element."""
        return self.get("fontsize")

    def set_fontsize(self, value: Any) -> None:
        """Set the ``fontsize`` attribute for the graph element."""
        return self.set("fontsize", value)

    def get_label(self) -> Any:
        """Get the ``label`` attribute for the graph element."""
        return self.get("label")

    def set_label(self, value: Any) -> None:
        """Set the ``label`` attribute for the graph element."""
        return self.set("label", value)

    def get_nojustify(self) -> Any:
        """Get the ``nojustify`` attribute for the graph element."""
        return self.get("nojustify")

    def set_nojustify(self, value: Any) -> None:
        """Set the ``nojustify`` attribute for the graph element."""
        return self.set("nojustify", value)

    def get_target(self) -> Any:
        """Get the ``target`` attribute for the graph element."""
        return self.get("target")

    def set_target(self, value: Any) -> None:
        """Set the ``target`` attribute for the graph element."""
        return self.set("target", value)


class NodeMixin:
    """Attribute convenience methods for Node."""

    def get(self, name: str) -> Any:
        """Generic get method (must be reimplemented)."""
        raise NotImplementedError

    def set(self, name: str, value: Any) -> None:
        """Generic set method (must be reimplemented)."""
        raise NotImplementedError

    def get_color(self) -> Any:
        """Get the ``color`` attribute for the graph element."""
        return self.get("color")

    def set_color(self, value: Any) -> None:
        """Set the ``color`` attribute for the graph element."""
        return self.set("color", value)

    def get_comment(self) -> Any:
        """Get the ``comment`` attribute for the graph element."""
        return self.get("comment")

    def set_comment(self, value: Any) -> None:
        """Set the ``comment`` attribute for the graph element."""
        return self.set("comment", value)

    def get_distortion(self) -> Any:
        """Get the ``distortion`` attribute for the graph element."""
        return self.get("distortion")

    def set_distortion(self, value: Any) -> None:
        """Set the ``distortion`` attribute for the graph element."""
        return self.set("distortion", value)

    def get_fillcolor(self) -> Any:
        """Get the ``fillcolor`` attribute for the graph element."""
        return self.get("fillcolor")

    def set_fillcolor(self, value: Any) -> None:
        """Set the ``fillcolor`` attribute for the graph element."""
        return self.set("fillcolor", value)

    def get_fixedsize(self) -> Any:
        """Get the ``fixedsize`` attribute for the graph element."""
        return self.get("fixedsize")

    def set_fixedsize(self, value: Any) -> None:
        """Set the ``fixedsize`` attribute for the graph element."""
        return self.set("fixedsize", value)

    def get_group(self) -> Any:
        """Get the ``group`` attribute for the graph element."""
        return self.get("group")

    def set_group(self, value: Any) -> None:
        """Set the ``group`` attribute for the graph element."""
        return self.set("group", value)

    def get_height(self) -> Any:
        """Get the ``height`` attribute for the graph element."""
        return self.get("height")

    def set_height(self, value: Any) -> None:
        """Set the ``height`` attribute for the graph element."""
        return self.set("height", value)

    def get_id(self) -> Any:
        """Get the ``id`` attribute for the graph element."""
        return self.get("id")

    def set_id(self, value: Any) -> None:
        """Set the ``id`` attribute for the graph element."""
        return self.set("id", value)

    def get_image(self) -> Any:
        """Get the ``image`` attribute for the graph element."""
        return self.get("image")

    def set_image(self, value: Any) -> None:
        """Set the ``image`` attribute for the graph element."""
        return self.set("image", value)

    def get_imagescale(self) -> Any:
        """Get the ``imagescale`` attribute for the graph element."""
        return self.get("imagescale")

    def set_imagescale(self, value: Any) -> None:
        """Set the ``imagescale`` attribute for the graph element."""
        return self.set("imagescale", value)

    def get_labelloc(self) -> Any:
        """Get the ``labelloc`` attribute for the graph element."""
        return self.get("labelloc")

    def set_labelloc(self, value: Any) -> None:
        """Set the ``labelloc`` attribute for the graph element."""
        return self.set("labelloc", value)

    def get_layer(self) -> Any:
        """Get the ``layer`` attribute for the graph element."""
        return self.get("layer")

    def set_layer(self, value: Any) -> None:
        """Set the ``layer`` attribute for the graph element."""
        return self.set("layer", value)

    def get_margin(self) -> Any:
        """Get the ``margin`` attribute for the graph element."""
        return self.get("margin")

    def set_margin(self, value: Any) -> None:
        """Set the ``margin`` attribute for the graph element."""
        return self.set("margin", value)

    def get_orientation(self) -> Any:
        """Get the ``orientation`` attribute for the graph element."""
        return self.get("orientation")

    def set_orientation(self, value: Any) -> None:
        """Set the ``orientation`` attribute for the graph element."""
        return self.set("orientation", value)

    def get_penwidth(self) -> Any:
        """Get the ``penwidth`` attribute for the graph element."""
        return self.get("penwidth")

    def set_penwidth(self, value: Any) -> None:
        """Set the ``penwidth`` attribute for the graph element."""
        return self.set("penwidth", value)

    def get_peripheries(self) -> Any:
        """Get the ``peripheries`` attribute for the graph element."""
        return self.get("peripheries")

    def set_peripheries(self, value: Any) -> None:
        """Set the ``peripheries`` attribute for the graph element."""
        return self.set("peripheries", value)

    def get_pin(self) -> Any:
        """Get the ``pin`` attribute for the graph element."""
        return self.get("pin")

    def set_pin(self, value: Any) -> None:
        """Set the ``pin`` attribute for the graph element."""
        return self.set("pin", value)

    def get_pos(self) -> Any:
        """Get the ``pos`` attribute for the graph element."""
        return self.get("pos")

    def set_pos(self, value: Any) -> None:
        """Set the ``pos`` attribute for the graph element."""
        return self.set("pos", value)

    def get_rects(self) -> Any:
        """Get the ``rects`` attribute for the graph element."""
        return self.get("rects")

    def set_rects(self, value: Any) -> None:
        """Set the ``rects`` attribute for the graph element."""
        return self.set("rects", value)

    def get_regular(self) -> Any:
        """Get the ``regular`` attribute for the graph element."""
        return self.get("regular")

    def set_regular(self, value: Any) -> None:
        """Set the ``regular`` attribute for the graph element."""
        return self.set("regular", value)

    def get_root(self) -> Any:
        """Get the ``root`` attribute for the graph element."""
        return self.get("root")

    def set_root(self, value: Any) -> None:
        """Set the ``root`` attribute for the graph element."""
        return self.set("root", value)

    def get_samplepoints(self) -> Any:
        """Get the ``samplepoints`` attribute for the graph element."""
        return self.get("samplepoints")

    def set_samplepoints(self, value: Any) -> None:
        """Set the ``samplepoints`` attribute for the graph element."""
        return self.set("samplepoints", value)

    def get_shape(self) -> Any:
        """Get the ``shape`` attribute for the graph element."""
        return self.get("shape")

    def set_shape(self, value: Any) -> None:
        """Set the ``shape`` attribute for the graph element."""
        return self.set("shape", value)

    def get_shapefile(self) -> Any:
        """Get the ``shapefile`` attribute for the graph element."""
        return self.get("shapefile")

    def set_shapefile(self, value: Any) -> None:
        """Set the ``shapefile`` attribute for the graph element."""
        return self.set("shapefile", value)

    def get_showboxes(self) -> Any:
        """Get the ``showboxes`` attribute for the graph element."""
        return self.get("showboxes")

    def set_showboxes(self, value: Any) -> None:
        """Set the ``showboxes`` attribute for the graph element."""
        return self.set("showboxes", value)

    def get_sides(self) -> Any:
        """Get the ``sides`` attribute for the graph element."""
        return self.get("sides")

    def set_sides(self, value: Any) -> None:
        """Set the ``sides`` attribute for the graph element."""
        return self.set("sides", value)

    def get_skew(self) -> Any:
        """Get the ``skew`` attribute for the graph element."""
        return self.get("skew")

    def set_skew(self, value: Any) -> None:
        """Set the ``skew`` attribute for the graph element."""
        return self.set("skew", value)

    def get_sortv(self) -> Any:
        """Get the ``sortv`` attribute for the graph element."""
        return self.get("sortv")

    def set_sortv(self, value: Any) -> None:
        """Set the ``sortv`` attribute for the graph element."""
        return self.set("sortv", value)

    def get_style(self) -> Any:
        """Get the ``style`` attribute for the graph element."""
        return self.get("style")

    def set_style(self, value: Any) -> None:
        """Set the ``style`` attribute for the graph element."""
        return self.set("style", value)

    def get_texlbl(self) -> Any:
        """Get the ``texlbl`` attribute for the graph element."""
        return self.get("texlbl")

    def set_texlbl(self, value: Any) -> None:
        """Set the ``texlbl`` attribute for the graph element."""
        return self.set("texlbl", value)

    def get_texmode(self) -> Any:
        """Get the ``texmode`` attribute for the graph element."""
        return self.get("texmode")

    def set_texmode(self, value: Any) -> None:
        """Set the ``texmode`` attribute for the graph element."""
        return self.set("texmode", value)

    def get_tooltip(self) -> Any:
        """Get the ``tooltip`` attribute for the graph element."""
        return self.get("tooltip")

    def set_tooltip(self, value: Any) -> None:
        """Set the ``tooltip`` attribute for the graph element."""
        return self.set("tooltip", value)

    def get_vertices(self) -> Any:
        """Get the ``vertices`` attribute for the graph element."""
        return self.get("vertices")

    def set_vertices(self, value: Any) -> None:
        """Set the ``vertices`` attribute for the graph element."""
        return self.set("vertices", value)

    def get_width(self) -> Any:
        """Get the ``width`` attribute for the graph element."""
        return self.get("width")

    def set_width(self, value: Any) -> None:
        """Set the ``width`` attribute for the graph element."""
        return self.set("width", value)

    def get_z(self) -> Any:
        """Get the ``z`` attribute for the graph element."""
        return self.get("z")

    def set_z(self, value: Any) -> None:
        """Set the ``z`` attribute for the graph element."""
        return self.set("z", value)


class EdgeMixin:
    """Attribute convenience methods for Edge."""

    def get(self, name: str) -> Any:
        """Generic get method (must be reimplemented)."""
        raise NotImplementedError

    def set(self, name: str, value: Any) -> None:
        """Generic set method (must be reimplemented)."""
        raise NotImplementedError

    def get_arrowhead(self) -> Any:
        """Get the ``arrowhead`` attribute for the graph element."""
        return self.get("arrowhead")

    def set_arrowhead(self, value: Any) -> None:
        """Set the ``arrowhead`` attribute for the graph element."""
        return self.set("arrowhead", value)

    def get_arrowsize(self) -> Any:
        """Get the ``arrowsize`` attribute for the graph element."""
        return self.get("arrowsize")

    def set_arrowsize(self, value: Any) -> None:
        """Set the ``arrowsize`` attribute for the graph element."""
        return self.set("arrowsize", value)

    def get_arrowtail(self) -> Any:
        """Get the ``arrowtail`` attribute for the graph element."""
        return self.get("arrowtail")

    def set_arrowtail(self, value: Any) -> None:
        """Set the ``arrowtail`` attribute for the graph element."""
        return self.set("arrowtail", value)

    def get_color(self) -> Any:
        """Get the ``color`` attribute for the graph element."""
        return self.get("color")

    def set_color(self, value: Any) -> None:
        """Set the ``color`` attribute for the graph element."""
        return self.set("color", value)

    def get_comment(self) -> Any:
        """Get the ``comment`` attribute for the graph element."""
        return self.get("comment")

    def set_comment(self, value: Any) -> None:
        """Set the ``comment`` attribute for the graph element."""
        return self.set("comment", value)

    def get_constraint(self) -> Any:
        """Get the ``constraint`` attribute for the graph element."""
        return self.get("constraint")

    def set_constraint(self, value: Any) -> None:
        """Set the ``constraint`` attribute for the graph element."""
        return self.set("constraint", value)

    def get_decorate(self) -> Any:
        """Get the ``decorate`` attribute for the graph element."""
        return self.get("decorate")

    def set_decorate(self, value: Any) -> None:
        """Set the ``decorate`` attribute for the graph element."""
        return self.set("decorate", value)

    def get_dir(self) -> Any:
        """Get the ``dir`` attribute for the graph element."""
        return self.get("dir")

    def set_dir(self, value: Any) -> None:
        """Set the ``dir`` attribute for the graph element."""
        return self.set("dir", value)

    def get_edgeURL(self) -> Any:
        """Get the ``edgeURL`` attribute for the graph element."""
        return self.get("edgeURL")

    def set_edgeURL(self, value: Any) -> None:
        """Set the ``edgeURL`` attribute for the graph element."""
        return self.set("edgeURL", value)

    def get_edgehref(self) -> Any:
        """Get the ``edgehref`` attribute for the graph element."""
        return self.get("edgehref")

    def set_edgehref(self, value: Any) -> None:
        """Set the ``edgehref`` attribute for the graph element."""
        return self.set("edgehref", value)

    def get_edgetarget(self) -> Any:
        """Get the ``edgetarget`` attribute for the graph element."""
        return self.get("edgetarget")

    def set_edgetarget(self, value: Any) -> None:
        """Set the ``edgetarget`` attribute for the graph element."""
        return self.set("edgetarget", value)

    def get_edgetooltip(self) -> Any:
        """Get the ``edgetooltip`` attribute for the graph element."""
        return self.get("edgetooltip")

    def set_edgetooltip(self, value: Any) -> None:
        """Set the ``edgetooltip`` attribute for the graph element."""
        return self.set("edgetooltip", value)

    def get_headURL(self) -> Any:
        """Get the ``headURL`` attribute for the graph element."""
        return self.get("headURL")

    def set_headURL(self, value: Any) -> None:
        """Set the ``headURL`` attribute for the graph element."""
        return self.set("headURL", value)

    def get_headclip(self) -> Any:
        """Get the ``headclip`` attribute for the graph element."""
        return self.get("headclip")

    def set_headclip(self, value: Any) -> None:
        """Set the ``headclip`` attribute for the graph element."""
        return self.set("headclip", value)

    def get_headhref(self) -> Any:
        """Get the ``headhref`` attribute for the graph element."""
        return self.get("headhref")

    def set_headhref(self, value: Any) -> None:
        """Set the ``headhref`` attribute for the graph element."""
        return self.set("headhref", value)

    def get_headlabel(self) -> Any:
        """Get the ``headlabel`` attribute for the graph element."""
        return self.get("headlabel")

    def set_headlabel(self, value: Any) -> None:
        """Set the ``headlabel`` attribute for the graph element."""
        return self.set("headlabel", value)

    def get_headport(self) -> Any:
        """Get the ``headport`` attribute for the graph element."""
        return self.get("headport")

    def set_headport(self, value: Any) -> None:
        """Set the ``headport`` attribute for the graph element."""
        return self.set("headport", value)

    def get_headtarget(self) -> Any:
        """Get the ``headtarget`` attribute for the graph element."""
        return self.get("headtarget")

    def set_headtarget(self, value: Any) -> None:
        """Set the ``headtarget`` attribute for the graph element."""
        return self.set("headtarget", value)

    def get_headtooltip(self) -> Any:
        """Get the ``headtooltip`` attribute for the graph element."""
        return self.get("headtooltip")

    def set_headtooltip(self, value: Any) -> None:
        """Set the ``headtooltip`` attribute for the graph element."""
        return self.set("headtooltip", value)

    def get_href(self) -> Any:
        """Get the ``href`` attribute for the graph element."""
        return self.get("href")

    def set_href(self, value: Any) -> None:
        """Set the ``href`` attribute for the graph element."""
        return self.set("href", value)

    def get_id(self) -> Any:
        """Get the ``id`` attribute for the graph element."""
        return self.get("id")

    def set_id(self, value: Any) -> None:
        """Set the ``id`` attribute for the graph element."""
        return self.set("id", value)

    def get_labelURL(self) -> Any:
        """Get the ``labelURL`` attribute for the graph element."""
        return self.get("labelURL")

    def set_labelURL(self, value: Any) -> None:
        """Set the ``labelURL`` attribute for the graph element."""
        return self.set("labelURL", value)

    def get_labelangle(self) -> Any:
        """Get the ``labelangle`` attribute for the graph element."""
        return self.get("labelangle")

    def set_labelangle(self, value: Any) -> None:
        """Set the ``labelangle`` attribute for the graph element."""
        return self.set("labelangle", value)

    def get_labeldistance(self) -> Any:
        """Get the ``labeldistance`` attribute for the graph element."""
        return self.get("labeldistance")

    def set_labeldistance(self, value: Any) -> None:
        """Set the ``labeldistance`` attribute for the graph element."""
        return self.set("labeldistance", value)

    def get_labelfloat(self) -> Any:
        """Get the ``labelfloat`` attribute for the graph element."""
        return self.get("labelfloat")

    def set_labelfloat(self, value: Any) -> None:
        """Set the ``labelfloat`` attribute for the graph element."""
        return self.set("labelfloat", value)

    def get_labelfontcolor(self) -> Any:
        """Get the ``labelfontcolor`` attribute for the graph element."""
        return self.get("labelfontcolor")

    def set_labelfontcolor(self, value: Any) -> None:
        """Set the ``labelfontcolor`` attribute for the graph element."""
        return self.set("labelfontcolor", value)

    def get_labelfontname(self) -> Any:
        """Get the ``labelfontname`` attribute for the graph element."""
        return self.get("labelfontname")

    def set_labelfontname(self, value: Any) -> None:
        """Set the ``labelfontname`` attribute for the graph element."""
        return self.set("labelfontname", value)

    def get_labelfontsize(self) -> Any:
        """Get the ``labelfontsize`` attribute for the graph element."""
        return self.get("labelfontsize")

    def set_labelfontsize(self, value: Any) -> None:
        """Set the ``labelfontsize`` attribute for the graph element."""
        return self.set("labelfontsize", value)

    def get_labelhref(self) -> Any:
        """Get the ``labelhref`` attribute for the graph element."""
        return self.get("labelhref")

    def set_labelhref(self, value: Any) -> None:
        """Set the ``labelhref`` attribute for the graph element."""
        return self.set("labelhref", value)

    def get_labeltarget(self) -> Any:
        """Get the ``labeltarget`` attribute for the graph element."""
        return self.get("labeltarget")

    def set_labeltarget(self, value: Any) -> None:
        """Set the ``labeltarget`` attribute for the graph element."""
        return self.set("labeltarget", value)

    def get_labeltooltip(self) -> Any:
        """Get the ``labeltooltip`` attribute for the graph element."""
        return self.get("labeltooltip")

    def set_labeltooltip(self, value: Any) -> None:
        """Set the ``labeltooltip`` attribute for the graph element."""
        return self.set("labeltooltip", value)

    def get_layer(self) -> Any:
        """Get the ``layer`` attribute for the graph element."""
        return self.get("layer")

    def set_layer(self, value: Any) -> None:
        """Set the ``layer`` attribute for the graph element."""
        return self.set("layer", value)

    def get_len(self) -> Any:
        """Get the ``len`` attribute for the graph element."""
        return self.get("len")

    def set_len(self, value: Any) -> None:
        """Set the ``len`` attribute for the graph element."""
        return self.set("len", value)

    def get_lhead(self) -> Any:
        """Get the ``lhead`` attribute for the graph element."""
        return self.get("lhead")

    def set_lhead(self, value: Any) -> None:
        """Set the ``lhead`` attribute for the graph element."""
        return self.set("lhead", value)

    def get_lp(self) -> Any:
        """Get the ``lp`` attribute for the graph element."""
        return self.get("lp")

    def set_lp(self, value: Any) -> None:
        """Set the ``lp`` attribute for the graph element."""
        return self.set("lp", value)

    def get_ltail(self) -> Any:
        """Get the ``ltail`` attribute for the graph element."""
        return self.get("ltail")

    def set_ltail(self, value: Any) -> None:
        """Set the ``ltail`` attribute for the graph element."""
        return self.set("ltail", value)

    def get_minlen(self) -> Any:
        """Get the ``minlen`` attribute for the graph element."""
        return self.get("minlen")

    def set_minlen(self, value: Any) -> None:
        """Set the ``minlen`` attribute for the graph element."""
        return self.set("minlen", value)

    def get_penwidth(self) -> Any:
        """Get the ``penwidth`` attribute for the graph element."""
        return self.get("penwidth")

    def set_penwidth(self, value: Any) -> None:
        """Set the ``penwidth`` attribute for the graph element."""
        return self.set("penwidth", value)

    def get_pos(self) -> Any:
        """Get the ``pos`` attribute for the graph element."""
        return self.get("pos")

    def set_pos(self, value: Any) -> None:
        """Set the ``pos`` attribute for the graph element."""
        return self.set("pos", value)

    def get_rank(self) -> Any:
        """Get the ``rank`` attribute for the graph element."""
        return self.get("rank")

    def set_rank(self, value: Any) -> None:
        """Set the ``rank`` attribute for the graph element."""
        return self.set("rank", value)

    def get_samehead(self) -> Any:
        """Get the ``samehead`` attribute for the graph element."""
        return self.get("samehead")

    def set_samehead(self, value: Any) -> None:
        """Set the ``samehead`` attribute for the graph element."""
        return self.set("samehead", value)

    def get_sametail(self) -> Any:
        """Get the ``sametail`` attribute for the graph element."""
        return self.get("sametail")

    def set_sametail(self, value: Any) -> None:
        """Set the ``sametail`` attribute for the graph element."""
        return self.set("sametail", value)

    def get_showboxes(self) -> Any:
        """Get the ``showboxes`` attribute for the graph element."""
        return self.get("showboxes")

    def set_showboxes(self, value: Any) -> None:
        """Set the ``showboxes`` attribute for the graph element."""
        return self.set("showboxes", value)

    def get_style(self) -> Any:
        """Get the ``style`` attribute for the graph element."""
        return self.get("style")

    def set_style(self, value: Any) -> None:
        """Set the ``style`` attribute for the graph element."""
        return self.set("style", value)

    def get_tailURL(self) -> Any:
        """Get the ``tailURL`` attribute for the graph element."""
        return self.get("tailURL")

    def set_tailURL(self, value: Any) -> None:
        """Set the ``tailURL`` attribute for the graph element."""
        return self.set("tailURL", value)

    def get_tailclip(self) -> Any:
        """Get the ``tailclip`` attribute for the graph element."""
        return self.get("tailclip")

    def set_tailclip(self, value: Any) -> None:
        """Set the ``tailclip`` attribute for the graph element."""
        return self.set("tailclip", value)

    def get_tailhref(self) -> Any:
        """Get the ``tailhref`` attribute for the graph element."""
        return self.get("tailhref")

    def set_tailhref(self, value: Any) -> None:
        """Set the ``tailhref`` attribute for the graph element."""
        return self.set("tailhref", value)

    def get_taillabel(self) -> Any:
        """Get the ``taillabel`` attribute for the graph element."""
        return self.get("taillabel")

    def set_taillabel(self, value: Any) -> None:
        """Set the ``taillabel`` attribute for the graph element."""
        return self.set("taillabel", value)

    def get_tailport(self) -> Any:
        """Get the ``tailport`` attribute for the graph element."""
        return self.get("tailport")

    def set_tailport(self, value: Any) -> None:
        """Set the ``tailport`` attribute for the graph element."""
        return self.set("tailport", value)

    def get_tailtarget(self) -> Any:
        """Get the ``tailtarget`` attribute for the graph element."""
        return self.get("tailtarget")

    def set_tailtarget(self, value: Any) -> None:
        """Set the ``tailtarget`` attribute for the graph element."""
        return self.set("tailtarget", value)

    def get_tailtooltip(self) -> Any:
        """Get the ``tailtooltip`` attribute for the graph element."""
        return self.get("tailtooltip")

    def set_tailtooltip(self, value: Any) -> None:
        """Set the ``tailtooltip`` attribute for the graph element."""
        return self.set("tailtooltip", value)

    def get_tooltip(self) -> Any:
        """Get the ``tooltip`` attribute for the graph element."""
        return self.get("tooltip")

    def set_tooltip(self, value: Any) -> None:
        """Set the ``tooltip`` attribute for the graph element."""
        return self.set("tooltip", value)

    def get_weight(self) -> Any:
        """Get the ``weight`` attribute for the graph element."""
        return self.get("weight")

    def set_weight(self, value: Any) -> None:
        """Set the ``weight`` attribute for the graph element."""
        return self.set("weight", value)


class GraphMixin:
    """Attribute convenience methods for Graph."""

    def get(self, name: str) -> Any:
        """Generic get method (must be reimplemented)."""
        raise NotImplementedError

    def set(self, name: str, value: Any) -> None:
        """Generic set method (must be reimplemented)."""
        raise NotImplementedError

    def get_Damping(self) -> Any:
        """Get the ``Damping`` attribute for the graph element."""
        return self.get("Damping")

    def set_Damping(self, value: Any) -> None:
        """Set the ``Damping`` attribute for the graph element."""
        return self.set("Damping", value)

    def get_K(self) -> Any:
        """Get the ``K`` attribute for the graph element."""
        return self.get("K")

    def set_K(self, value: Any) -> None:
        """Set the ``K`` attribute for the graph element."""
        return self.set("K", value)

    def get_aspect(self) -> Any:
        """Get the ``aspect`` attribute for the graph element."""
        return self.get("aspect")

    def set_aspect(self, value: Any) -> None:
        """Set the ``aspect`` attribute for the graph element."""
        return self.set("aspect", value)

    def get_bb(self) -> Any:
        """Get the ``bb`` attribute for the graph element."""
        return self.get("bb")

    def set_bb(self, value: Any) -> None:
        """Set the ``bb`` attribute for the graph element."""
        return self.set("bb", value)

    def get_bgcolor(self) -> Any:
        """Get the ``bgcolor`` attribute for the graph element."""
        return self.get("bgcolor")

    def set_bgcolor(self, value: Any) -> None:
        """Set the ``bgcolor`` attribute for the graph element."""
        return self.set("bgcolor", value)

    def get_center(self) -> Any:
        """Get the ``center`` attribute for the graph element."""
        return self.get("center")

    def set_center(self, value: Any) -> None:
        """Set the ``center`` attribute for the graph element."""
        return self.set("center", value)

    def get_charset(self) -> Any:
        """Get the ``charset`` attribute for the graph element."""
        return self.get("charset")

    def set_charset(self, value: Any) -> None:
        """Set the ``charset`` attribute for the graph element."""
        return self.set("charset", value)

    def get_clusterrank(self) -> Any:
        """Get the ``clusterrank`` attribute for the graph element."""
        return self.get("clusterrank")

    def set_clusterrank(self, value: Any) -> None:
        """Set the ``clusterrank`` attribute for the graph element."""
        return self.set("clusterrank", value)

    def get_comment(self) -> Any:
        """Get the ``comment`` attribute for the graph element."""
        return self.get("comment")

    def set_comment(self, value: Any) -> None:
        """Set the ``comment`` attribute for the graph element."""
        return self.set("comment", value)

    def get_compound(self) -> Any:
        """Get the ``compound`` attribute for the graph element."""
        return self.get("compound")

    def set_compound(self, value: Any) -> None:
        """Set the ``compound`` attribute for the graph element."""
        return self.set("compound", value)

    def get_concentrate(self) -> Any:
        """Get the ``concentrate`` attribute for the graph element."""
        return self.get("concentrate")

    def set_concentrate(self, value: Any) -> None:
        """Set the ``concentrate`` attribute for the graph element."""
        return self.set("concentrate", value)

    def get_defaultdist(self) -> Any:
        """Get the ``defaultdist`` attribute for the graph element."""
        return self.get("defaultdist")

    def set_defaultdist(self, value: Any) -> None:
        """Set the ``defaultdist`` attribute for the graph element."""
        return self.set("defaultdist", value)

    def get_dim(self) -> Any:
        """Get the ``dim`` attribute for the graph element."""
        return self.get("dim")

    def set_dim(self, value: Any) -> None:
        """Set the ``dim`` attribute for the graph element."""
        return self.set("dim", value)

    def get_dimen(self) -> Any:
        """Get the ``dimen`` attribute for the graph element."""
        return self.get("dimen")

    def set_dimen(self, value: Any) -> None:
        """Set the ``dimen`` attribute for the graph element."""
        return self.set("dimen", value)

    def get_diredgeconstraints(self) -> Any:
        """Get the ``diredgeconstraints`` attribute for the graph element."""
        return self.get("diredgeconstraints")

    def set_diredgeconstraints(self, value: Any) -> None:
        """Set the ``diredgeconstraints`` attribute for the graph element."""
        return self.set("diredgeconstraints", value)

    def get_dpi(self) -> Any:
        """Get the ``dpi`` attribute for the graph element."""
        return self.get("dpi")

    def set_dpi(self, value: Any) -> None:
        """Set the ``dpi`` attribute for the graph element."""
        return self.set("dpi", value)

    def get_epsilon(self) -> Any:
        """Get the ``epsilon`` attribute for the graph element."""
        return self.get("epsilon")

    def set_epsilon(self, value: Any) -> None:
        """Set the ``epsilon`` attribute for the graph element."""
        return self.set("epsilon", value)

    def get_esep(self) -> Any:
        """Get the ``esep`` attribute for the graph element."""
        return self.get("esep")

    def set_esep(self, value: Any) -> None:
        """Set the ``esep`` attribute for the graph element."""
        return self.set("esep", value)

    def get_fontnames(self) -> Any:
        """Get the ``fontnames`` attribute for the graph element."""
        return self.get("fontnames")

    def set_fontnames(self, value: Any) -> None:
        """Set the ``fontnames`` attribute for the graph element."""
        return self.set("fontnames", value)

    def get_fontpath(self) -> Any:
        """Get the ``fontpath`` attribute for the graph element."""
        return self.get("fontpath")

    def set_fontpath(self, value: Any) -> None:
        """Set the ``fontpath`` attribute for the graph element."""
        return self.set("fontpath", value)

    def get_id(self) -> Any:
        """Get the ``id`` attribute for the graph element."""
        return self.get("id")

    def set_id(self, value: Any) -> None:
        """Set the ``id`` attribute for the graph element."""
        return self.set("id", value)

    def get_labeljust(self) -> Any:
        """Get the ``labeljust`` attribute for the graph element."""
        return self.get("labeljust")

    def set_labeljust(self, value: Any) -> None:
        """Set the ``labeljust`` attribute for the graph element."""
        return self.set("labeljust", value)

    def get_labelloc(self) -> Any:
        """Get the ``labelloc`` attribute for the graph element."""
        return self.get("labelloc")

    def set_labelloc(self, value: Any) -> None:
        """Set the ``labelloc`` attribute for the graph element."""
        return self.set("labelloc", value)

    def get_landscape(self) -> Any:
        """Get the ``landscape`` attribute for the graph element."""
        return self.get("landscape")

    def set_landscape(self, value: Any) -> None:
        """Set the ``landscape`` attribute for the graph element."""
        return self.set("landscape", value)

    def get_layers(self) -> Any:
        """Get the ``layers`` attribute for the graph element."""
        return self.get("layers")

    def set_layers(self, value: Any) -> None:
        """Set the ``layers`` attribute for the graph element."""
        return self.set("layers", value)

    def get_layersep(self) -> Any:
        """Get the ``layersep`` attribute for the graph element."""
        return self.get("layersep")

    def set_layersep(self, value: Any) -> None:
        """Set the ``layersep`` attribute for the graph element."""
        return self.set("layersep", value)

    def get_layout(self) -> Any:
        """Get the ``layout`` attribute for the graph element."""
        return self.get("layout")

    def set_layout(self, value: Any) -> None:
        """Set the ``layout`` attribute for the graph element."""
        return self.set("layout", value)

    def get_levels(self) -> Any:
        """Get the ``levels`` attribute for the graph element."""
        return self.get("levels")

    def set_levels(self, value: Any) -> None:
        """Set the ``levels`` attribute for the graph element."""
        return self.set("levels", value)

    def get_levelsgap(self) -> Any:
        """Get the ``levelsgap`` attribute for the graph element."""
        return self.get("levelsgap")

    def set_levelsgap(self, value: Any) -> None:
        """Set the ``levelsgap`` attribute for the graph element."""
        return self.set("levelsgap", value)

    def get_lheight(self) -> Any:
        """Get the ``lheight`` attribute for the graph element."""
        return self.get("lheight")

    def set_lheight(self, value: Any) -> None:
        """Set the ``lheight`` attribute for the graph element."""
        return self.set("lheight", value)

    def get_lp(self) -> Any:
        """Get the ``lp`` attribute for the graph element."""
        return self.get("lp")

    def set_lp(self, value: Any) -> None:
        """Set the ``lp`` attribute for the graph element."""
        return self.set("lp", value)

    def get_lwidth(self) -> Any:
        """Get the ``lwidth`` attribute for the graph element."""
        return self.get("lwidth")

    def set_lwidth(self, value: Any) -> None:
        """Set the ``lwidth`` attribute for the graph element."""
        return self.set("lwidth", value)

    def get_margin(self) -> Any:
        """Get the ``margin`` attribute for the graph element."""
        return self.get("margin")

    def set_margin(self, value: Any) -> None:
        """Set the ``margin`` attribute for the graph element."""
        return self.set("margin", value)

    def get_maxiter(self) -> Any:
        """Get the ``maxiter`` attribute for the graph element."""
        return self.get("maxiter")

    def set_maxiter(self, value: Any) -> None:
        """Set the ``maxiter`` attribute for the graph element."""
        return self.set("maxiter", value)

    def get_mclimit(self) -> Any:
        """Get the ``mclimit`` attribute for the graph element."""
        return self.get("mclimit")

    def set_mclimit(self, value: Any) -> None:
        """Set the ``mclimit`` attribute for the graph element."""
        return self.set("mclimit", value)

    def get_mindist(self) -> Any:
        """Get the ``mindist`` attribute for the graph element."""
        return self.get("mindist")

    def set_mindist(self, value: Any) -> None:
        """Set the ``mindist`` attribute for the graph element."""
        return self.set("mindist", value)

    def get_mode(self) -> Any:
        """Get the ``mode`` attribute for the graph element."""
        return self.get("mode")

    def set_mode(self, value: Any) -> None:
        """Set the ``mode`` attribute for the graph element."""
        return self.set("mode", value)

    def get_model(self) -> Any:
        """Get the ``model`` attribute for the graph element."""
        return self.get("model")

    def set_model(self, value: Any) -> None:
        """Set the ``model`` attribute for the graph element."""
        return self.set("model", value)

    def get_mosek(self) -> Any:
        """Get the ``mosek`` attribute for the graph element."""
        return self.get("mosek")

    def set_mosek(self, value: Any) -> None:
        """Set the ``mosek`` attribute for the graph element."""
        return self.set("mosek", value)

    def get_nodesep(self) -> Any:
        """Get the ``nodesep`` attribute for the graph element."""
        return self.get("nodesep")

    def set_nodesep(self, value: Any) -> None:
        """Set the ``nodesep`` attribute for the graph element."""
        return self.set("nodesep", value)

    def get_normalize(self) -> Any:
        """Get the ``normalize`` attribute for the graph element."""
        return self.get("normalize")

    def set_normalize(self, value: Any) -> None:
        """Set the ``normalize`` attribute for the graph element."""
        return self.set("normalize", value)

    def get_nslimit(self) -> Any:
        """Get the ``nslimit`` attribute for the graph element."""
        return self.get("nslimit")

    def set_nslimit(self, value: Any) -> None:
        """Set the ``nslimit`` attribute for the graph element."""
        return self.set("nslimit", value)

    def get_nslimit1(self) -> Any:
        """Get the ``nslimit1`` attribute for the graph element."""
        return self.get("nslimit1")

    def set_nslimit1(self, value: Any) -> None:
        """Set the ``nslimit1`` attribute for the graph element."""
        return self.set("nslimit1", value)

    def get_ordering(self) -> Any:
        """Get the ``ordering`` attribute for the graph element."""
        return self.get("ordering")

    def set_ordering(self, value: Any) -> None:
        """Set the ``ordering`` attribute for the graph element."""
        return self.set("ordering", value)

    def get_orientation(self) -> Any:
        """Get the ``orientation`` attribute for the graph element."""
        return self.get("orientation")

    def set_orientation(self, value: Any) -> None:
        """Set the ``orientation`` attribute for the graph element."""
        return self.set("orientation", value)

    def get_outputorder(self) -> Any:
        """Get the ``outputorder`` attribute for the graph element."""
        return self.get("outputorder")

    def set_outputorder(self, value: Any) -> None:
        """Set the ``outputorder`` attribute for the graph element."""
        return self.set("outputorder", value)

    def get_overlap(self) -> Any:
        """Get the ``overlap`` attribute for the graph element."""
        return self.get("overlap")

    def set_overlap(self, value: Any) -> None:
        """Set the ``overlap`` attribute for the graph element."""
        return self.set("overlap", value)

    def get_overlap_scaling(self) -> Any:
        """Get the ``overlap_scaling`` attribute for the graph element."""
        return self.get("overlap_scaling")

    def set_overlap_scaling(self, value: Any) -> None:
        """Set the ``overlap_scaling`` attribute for the graph element."""
        return self.set("overlap_scaling", value)

    def get_pack(self) -> Any:
        """Get the ``pack`` attribute for the graph element."""
        return self.get("pack")

    def set_pack(self, value: Any) -> None:
        """Set the ``pack`` attribute for the graph element."""
        return self.set("pack", value)

    def get_packmode(self) -> Any:
        """Get the ``packmode`` attribute for the graph element."""
        return self.get("packmode")

    def set_packmode(self, value: Any) -> None:
        """Set the ``packmode`` attribute for the graph element."""
        return self.set("packmode", value)

    def get_pad(self) -> Any:
        """Get the ``pad`` attribute for the graph element."""
        return self.get("pad")

    def set_pad(self, value: Any) -> None:
        """Set the ``pad`` attribute for the graph element."""
        return self.set("pad", value)

    def get_page(self) -> Any:
        """Get the ``page`` attribute for the graph element."""
        return self.get("page")

    def set_page(self, value: Any) -> None:
        """Set the ``page`` attribute for the graph element."""
        return self.set("page", value)

    def get_pagedir(self) -> Any:
        """Get the ``pagedir`` attribute for the graph element."""
        return self.get("pagedir")

    def set_pagedir(self, value: Any) -> None:
        """Set the ``pagedir`` attribute for the graph element."""
        return self.set("pagedir", value)

    def get_quadtree(self) -> Any:
        """Get the ``quadtree`` attribute for the graph element."""
        return self.get("quadtree")

    def set_quadtree(self, value: Any) -> None:
        """Set the ``quadtree`` attribute for the graph element."""
        return self.set("quadtree", value)

    def get_quantum(self) -> Any:
        """Get the ``quantum`` attribute for the graph element."""
        return self.get("quantum")

    def set_quantum(self, value: Any) -> None:
        """Set the ``quantum`` attribute for the graph element."""
        return self.set("quantum", value)

    def get_rank(self) -> Any:
        """Get the ``rank`` attribute for the graph element."""
        return self.get("rank")

    def set_rank(self, value: Any) -> None:
        """Set the ``rank`` attribute for the graph element."""
        return self.set("rank", value)

    def get_rankdir(self) -> Any:
        """Get the ``rankdir`` attribute for the graph element."""
        return self.get("rankdir")

    def set_rankdir(self, value: Any) -> None:
        """Set the ``rankdir`` attribute for the graph element."""
        return self.set("rankdir", value)

    def get_ranksep(self) -> Any:
        """Get the ``ranksep`` attribute for the graph element."""
        return self.get("ranksep")

    def set_ranksep(self, value: Any) -> None:
        """Set the ``ranksep`` attribute for the graph element."""
        return self.set("ranksep", value)

    def get_ratio(self) -> Any:
        """Get the ``ratio`` attribute for the graph element."""
        return self.get("ratio")

    def set_ratio(self, value: Any) -> None:
        """Set the ``ratio`` attribute for the graph element."""
        return self.set("ratio", value)

    def get_remincross(self) -> Any:
        """Get the ``remincross`` attribute for the graph element."""
        return self.get("remincross")

    def set_remincross(self, value: Any) -> None:
        """Set the ``remincross`` attribute for the graph element."""
        return self.set("remincross", value)

    def get_repulsiveforce(self) -> Any:
        """Get the ``repulsiveforce`` attribute for the graph element."""
        return self.get("repulsiveforce")

    def set_repulsiveforce(self, value: Any) -> None:
        """Set the ``repulsiveforce`` attribute for the graph element."""
        return self.set("repulsiveforce", value)

    def get_resolution(self) -> Any:
        """Get the ``resolution`` attribute for the graph element."""
        return self.get("resolution")

    def set_resolution(self, value: Any) -> None:
        """Set the ``resolution`` attribute for the graph element."""
        return self.set("resolution", value)

    def get_root(self) -> Any:
        """Get the ``root`` attribute for the graph element."""
        return self.get("root")

    def set_root(self, value: Any) -> None:
        """Set the ``root`` attribute for the graph element."""
        return self.set("root", value)

    def get_rotate(self) -> Any:
        """Get the ``rotate`` attribute for the graph element."""
        return self.get("rotate")

    def set_rotate(self, value: Any) -> None:
        """Set the ``rotate`` attribute for the graph element."""
        return self.set("rotate", value)

    def get_searchsize(self) -> Any:
        """Get the ``searchsize`` attribute for the graph element."""
        return self.get("searchsize")

    def set_searchsize(self, value: Any) -> None:
        """Set the ``searchsize`` attribute for the graph element."""
        return self.set("searchsize", value)

    def get_sep(self) -> Any:
        """Get the ``sep`` attribute for the graph element."""
        return self.get("sep")

    def set_sep(self, value: Any) -> None:
        """Set the ``sep`` attribute for the graph element."""
        return self.set("sep", value)

    def get_showboxes(self) -> Any:
        """Get the ``showboxes`` attribute for the graph element."""
        return self.get("showboxes")

    def set_showboxes(self, value: Any) -> None:
        """Set the ``showboxes`` attribute for the graph element."""
        return self.set("showboxes", value)

    def get_size(self) -> Any:
        """Get the ``size`` attribute for the graph element."""
        return self.get("size")

    def set_size(self, value: Any) -> None:
        """Set the ``size`` attribute for the graph element."""
        return self.set("size", value)

    def get_smoothing(self) -> Any:
        """Get the ``smoothing`` attribute for the graph element."""
        return self.get("smoothing")

    def set_smoothing(self, value: Any) -> None:
        """Set the ``smoothing`` attribute for the graph element."""
        return self.set("smoothing", value)

    def get_sortv(self) -> Any:
        """Get the ``sortv`` attribute for the graph element."""
        return self.get("sortv")

    def set_sortv(self, value: Any) -> None:
        """Set the ``sortv`` attribute for the graph element."""
        return self.set("sortv", value)

    def get_splines(self) -> Any:
        """Get the ``splines`` attribute for the graph element."""
        return self.get("splines")

    def set_splines(self, value: Any) -> None:
        """Set the ``splines`` attribute for the graph element."""
        return self.set("splines", value)

    def get_start(self) -> Any:
        """Get the ``start`` attribute for the graph element."""
        return self.get("start")

    def set_start(self, value: Any) -> None:
        """Set the ``start`` attribute for the graph element."""
        return self.set("start", value)

    def get_stylesheet(self) -> Any:
        """Get the ``stylesheet`` attribute for the graph element."""
        return self.get("stylesheet")

    def set_stylesheet(self, value: Any) -> None:
        """Set the ``stylesheet`` attribute for the graph element."""
        return self.set("stylesheet", value)

    def get_truecolor(self) -> Any:
        """Get the ``truecolor`` attribute for the graph element."""
        return self.get("truecolor")

    def set_truecolor(self, value: Any) -> None:
        """Set the ``truecolor`` attribute for the graph element."""
        return self.set("truecolor", value)

    def get_viewport(self) -> Any:
        """Get the ``viewport`` attribute for the graph element."""
        return self.get("viewport")

    def set_viewport(self, value: Any) -> None:
        """Set the ``viewport`` attribute for the graph element."""
        return self.set("viewport", value)

    def get_voro_margin(self) -> Any:
        """Get the ``voro_margin`` attribute for the graph element."""
        return self.get("voro_margin")

    def set_voro_margin(self, value: Any) -> None:
        """Set the ``voro_margin`` attribute for the graph element."""
        return self.set("voro_margin", value)


class ClusterMixin:
    """Attribute convenience methods for Cluster."""

    def get(self, name: str) -> Any:
        """Generic get method (must be reimplemented)."""
        raise NotImplementedError

    def set(self, name: str, value: Any) -> None:
        """Generic set method (must be reimplemented)."""
        raise NotImplementedError

    def get_color(self) -> Any:
        """Get the ``color`` attribute for the graph element."""
        return self.get("color")

    def set_color(self, value: Any) -> None:
        """Set the ``color`` attribute for the graph element."""
        return self.set("color", value)

    def get_fillcolor(self) -> Any:
        """Get the ``fillcolor`` attribute for the graph element."""
        return self.get("fillcolor")

    def set_fillcolor(self, value: Any) -> None:
        """Set the ``fillcolor`` attribute for the graph element."""
        return self.set("fillcolor", value)

    def get_pencolor(self) -> Any:
        """Get the ``pencolor`` attribute for the graph element."""
        return self.get("pencolor")

    def set_pencolor(self, value: Any) -> None:
        """Set the ``pencolor`` attribute for the graph element."""
        return self.set("pencolor", value)

    def get_penwidth(self) -> Any:
        """Get the ``penwidth`` attribute for the graph element."""
        return self.get("penwidth")

    def set_penwidth(self, value: Any) -> None:
        """Set the ``penwidth`` attribute for the graph element."""
        return self.set("penwidth", value)

    def get_peripheries(self) -> Any:
        """Get the ``peripheries`` attribute for the graph element."""
        return self.get("peripheries")

    def set_peripheries(self, value: Any) -> None:
        """Set the ``peripheries`` attribute for the graph element."""
        return self.set("peripheries", value)

    def get_style(self) -> Any:
        """Get the ``style`` attribute for the graph element."""
        return self.get("style")

    def set_style(self, value: Any) -> None:
        """Set the ``style`` attribute for the graph element."""
        return self.set("style", value)

    def get_tooltip(self) -> Any:
        """Get the ``tooltip`` attribute for the graph element."""
        return self.get("tooltip")

    def set_tooltip(self, value: Any) -> None:
        """Set the ``tooltip`` attribute for the graph element."""
        return self.set("tooltip", value)
