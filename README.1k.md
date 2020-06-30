# for imagenet 1k images

1k
1k.shortnames.list
word.inet.txt
-> inet-grep.sh -> abc
cp abc imagenet1k.list

./downloadutils.py --cat -n 1 --wnid_list imagenet1k.wnid.list -th 30
python ./downloadutils.py --downloadImages -th 30 --wnid_list imagenet.labels.safedomain1.list -n 1000


#sed 's/^n[0-9]* //' abc > imagenet1k.shortnames.list
#awk '{print $1;}' abc > imagenet1k.wnid.list

./grep-i.py -i imagenet1k.shortnames.list words.inet.txt -o id > imagenet1k.wnid.list

**Notice**  
imagenet dataset has duplicated definitions of 'crane'.  
Split 'crane' category to 'crane, Wading birds' and 'crane, Lifing device' in imagenet1k.shortnames.list and words.inet.txt.  
