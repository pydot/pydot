#!/bin/sh

# SPDX-FileCopyrightText: 2024 pydot contributors
#
# SPDX-License-Identifier: MIT

for dir in */; do
    magick composite $dir/err_pydot.jpeg \
        -compose difference $dir/err_graphviz.jpeg \
        $dir/err_difference.png
    magick convert -delay 100 $dir/err_pydot.jpeg \
	-delay 100 $dir/err_graphviz.jpeg \
	$dir/anim_difference.gif
done
