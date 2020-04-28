#!/bin/bash

if [ ! -e words.txt ]; then
    echo download
    wget http://image-net.org/archive/words.txt
fi

if [ ! -e voc.names ]; then
    echo copy voc.names from darknet
    wget https://raw.githubusercontent.com/pjreddie/darknet/master/data/voc.names
fi

if [ ! -e imagenet.labels.list ]; then
    wget https://raw.githubusercontent.com/pjreddie/darknet/master/data/imagenet.labels.list
fi

if [ ! -e words.inet.txt ]; then
    echo Take a long time... words.inet.txt
    grep -f imagenet.labels.txt words.txt > words.inet.txt
fi

if [ ! -e inet-voc.list ];then
    grep -f voc.names words.inet.txt | awk '{print $1;}' > inet-voc.list
fi

./downloadutils.py --cat -n 900 --wnid_list inet-voc.list -th 20

wc words.txt voc.names imagenet.labels.list words.inet.txt inet-voc.list imagenet.labels.safedomain900.list

echo Run below to download images from IMAGENET related VOC.NAMES
echo ./downloadutils.py --downloadImages --wnid_list imagenet.labels.safedomain900.list -n 1000 -th 50
