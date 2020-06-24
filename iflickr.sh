#!/bin/bash

for i in $(find inet_images/* -type d);do fn=$(find $i -type f | wc -l); i=$(basename $i); num=$(expr 1000 - $fn);if [ $num -ne 0 ];then echo -n $i $num " ";grep $i words.inet.txt|sed -e 's/n[0-9]*\t//';fi;done > iflickr.list

idir="inet_flikr"
ppp=$(pwd)
while read ll;do

    iid=$(echo $ll | awk '{print $1;}') 
    mkdir -p $idir/$iid
    pushd $idir/$iid >& /dev/null

    num=$(echo $ll  | awk '{print $2;}')
    word=$(echo $ll | sed 's/^n[0-9 ]*//')
    short=$(echo $word | awk -F ',' '{print $1;}')

    echo -n $iid $num $word "->"
    python3 ${ppp}/libs/flickr.py --quiet -n $num "$word" -o ${iid}.url
    urls=$(cat ${iid}.url | wc -l)

    if [ $urls -eq 0 ];then
        rm -f ${iid}.url
    fi
#    if [ $urls -le $(expr $num / 2) ];then
#        urls2=$urls
#        python3 ${ppp}/libs/flickr.py --quiet -n $num "$short" -o ${iid}.url
#        urls=$(cat ${iid}.url | wc -l)
#        echo $urls2 "->" $urls $iid $short
#    fi
    echo $urls $iid $short

    if [ $urls -gt 0 ];then
        wget -q -b -i ${iid}.url
    fi

    popd >& /dev/null
done < iflickr.list
