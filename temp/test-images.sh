#!/bin/bash

mkdir -p ../data/images/
mkdir -p ../data/thumbs/
mkdir -p ../species

for CODE in `cat ../data/names.txt` ; do

    echo $CODE
    cp square.png ../data/images/${CODE}.png
    cp thumb.png ../data/thumbs/${CODE}.png
    
    cat base.html \
        | sed "s/#CODE#/${CODE}/g" \
        | sed "s?#PATH#?/home/lucas/Dropbox/GitHub/eseb-birds/data/images/${CODE}.png?g" \
        > ../species/${CODE}.html
    
done
