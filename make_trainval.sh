#!/bin/bash
export jpgs=$(find inet_images -iname \*.jpg | wc -l)
echo "JPEGs=" $jpgs

export valids=5000
export trains=$(($jpgs-$valids))
echo "train=" $trains "valid=" $valids

find inet_images -iname \*.jpg | sort -R | head -$trains > train.txt
echo -n "check train jpeg= "; wc -l train.txt

find inet_images -iname \*.jpg | sort -R | tail -$valids > valid.txt
echo -n "check valid jpeg= "; wc -l valid.txt

echo Ready train.txt valid.txt
