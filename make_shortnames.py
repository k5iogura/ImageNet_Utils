import sys,os
import argparse

p = argparse.ArgumentParser()
p.add_argument('-w','--words_txt', type=str,default='words.txt')
p.add_argument('-l','--target_labels', type=str,default='imagenet-voc.labels.list')
args = p.parse_args()

with open(args.target_labels) as f:
    targets = [ l.strip() for l in f]

with open(args.words_txt) as w:
    words = [ l.strip().split(',')[0].split('\t')  for l in w ]

words0 = [ l[0] for l in words ]
for t in targets:
    widx = words0.index(t)
    print(words[widx][1])

