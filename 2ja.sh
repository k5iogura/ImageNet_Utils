#!/bin/bash

if [ $# -lt 1 ];then
    exit
fi

lang4=en
lang2=ja

word=$*
word=$(echo $* | nkf -WwMQ | tr = %)
#word=$(echo $word | sed -e 's/ /%20/g')
#word=$(echo $word | sed -e 's/ /%20/g' -e 's/$/%22/')
#echo $word

req=$(echo 'https://script.google.com/macros/s/AKfycbwTMyNXe0JroZEy0UA6DHx34-FeH-s48oqYRbNxofxGh8amqkp-/exec?')
req=$(echo ${req}text=${word}?source=${lang4}?target=${lang2})
#echo $req

res=$(curl --silent -L https://script.google.com/macros/s/AKfycbwTMyNXe0JroZEy0UA6DHx34-FeH-s48oqYRbNxofxGh8amqkp-/exec?text=${word}\&source=en\&target=ja)

echo $res
