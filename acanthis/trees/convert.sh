#!/bin/bash

for f in `ls *.svg` ; do

    n=${f/svg/png}

    inkscape \
        --export-height=1200 \
        --export-png=$n \
        $f
      
    # --export-background-opacity=0 \ 
    # --export-filename=$n
    # --export-type=png \
done

