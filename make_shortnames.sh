#!/bin/bash
if [ ! -e words.txt ]; then
    wget http://image-net.org/archive/words.txt
fi
grep -f imagenet.labels.flickr900.list words.txt | awk -F ',' '{print $1;}' | sed -e 's/n[0-9]*\t//' -e 's/ *$//' -e 's/  */ /g' 
