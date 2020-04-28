#!/bin/bash

if [ ! -e words.txt ]; then
    echo download
    wget http://image-net.org/archive/words.txt
else
    echo Using words.txt
fi

if [ ! -e voc.names ]; then
    echo download
    wget https://raw.githubusercontent.com/pjreddie/darknet/master/data/voc.names
else
    echo Using voc.names
fi

if [ ! -e imagenet.labels.list ]; then
    echo download
    wget https://raw.githubusercontent.com/pjreddie/darknet/master/data/imagenet.labels.list
else
    echo Using imagenet.labels.list
fi

if [ ! -e words.inet.txt ]; then
    echo Take a long time... generating words.inet.txt
    grep -f imagenet.labels.list words.txt > words.inet.txt
fi

if [ ! -e inet-voc.list ];then
    echo generating inet-voc.list
    grep -f voc.names words.inet.txt | awk '{print $1;}' > inet-voc.list
fi

./downloadutils.py --cat -n 900 --wnid_list inet-voc.list -th 1

echo geterate shortnames
python make_shortnames.py -w words.txt -l imagenet.labels.safedomain900.list > imagenet.shortnames.safedomain900.list

cp imagenet.labels.safedomain900.list     inet-voc.labels.list
cp imagenet.shortnames.safedomain900.list inet-voc.shortnames.list

wc words.txt voc.names imagenet.labels.list words.inet.txt inet-voc.list imagenet.labels.safedomain900.list imagenet.shortnames.safedomain900.list
wc inet-voc.labels.list inet-voc.shortnames.list
echo use 2 files for classifier inet-voc.labels.list inet-voc.shortnames.list

echo Run below to download images from IMAGENET related VOC.NAMES
echo ./downloadutils.py --downloadImages --wnid_list inet-voc.labels.list -n 1000 -th 50
