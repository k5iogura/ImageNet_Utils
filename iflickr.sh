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

    echo -n $iid "request:" $num "images" "tags:" $word "->"
    python3 ${ppp}/libs/flickr.py --quiet -n $num "$word" -o ${iid}.url
    urls=$(cat ${iid}.url | wc -l)

    if [ $urls -eq 0 ];then
        rm -f ${iid}.url
    fi

    tags=$(echo $word | awk -F ',' '{printf NF;}')
    for w in $(seq $tags -1 2);do
        if [ $urls -le $(expr $num / 2) ];then
            short=$(echo $word | awk -v tags=$w -F ',' '{for(i=1;i<=tags-1;i++){printf $i ",";}}')
            #echo ""
            #echo $word ":" $short ":" $w
            urls2=$urls
            python3 ${ppp}/libs/flickr.py --quiet -n $num "$short" -o ${iid}.url
            urls=$(cat ${iid}.url | wc -l)
            echo $urls2 "->" $urls $short
        else
            break
        fi
    done


    if [ $urls -gt 0 ];then
        echo wget -q -b -i ${iid}.url
        echo $iid $urls "images" "tags:" $word
    else
        echo $urls $word "->" $short
        exit
    fi

    popd >& /dev/null
done < iflickr.list
