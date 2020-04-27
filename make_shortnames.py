import sys,os

flickr = 'imagenet.labels.flickr900.list'
word = 'words.txt'
short = 'imagenet.shortnames.flickr900.list'

with open(flickr) as f:
    flickrs = [ l.strip() for l in f]

with open(word) as w:
    words = [ l.strip().split(',')[0].split('\t')  for l in w ]

words0 = [ l[0] for l in words ]
shorts = []
for f in flickrs:
    widx = words0.index(f)
    shorts.append( words[widx] )

with open(short,"w") as f:
    for shortname in shorts:
        f.write("{}\n".format(shortname[1]))
