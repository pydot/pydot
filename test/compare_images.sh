#!/bin/sh

for dir in */; do
    magick composite $dir/err_pydot.jpeg \
        -compose difference $dir/err_graphviz.jpeg \
        $dir/err_difference.png
done
