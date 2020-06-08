#!/usr/bin/env python

import sys,re,os,argparse
from glob import glob
import cv2

def showf(f,wname='view'):
    img=cv2.imread(f)
    cv2.imshow(wname,img)
    while True:
        key=cv2.waitKey(10)
        if key==ord('q'):sys.exit(-1)
        if key!=-1: break

def dirfiles(d):
    files=glob(d+'/*')
    return files

def check(f):
    assert os.path.exists(f),"not found {}".format(f)
    return f

if __name__ == '__main__':
    args=argparse.ArgumentParser()
    args.add_argument('-d','--directory', type=check, nargs='+', default=[])
    args.add_argument('-f','--file',      type=check, nargs='+', default=[])
    args.add_argument('-s','--shortnames',type=check, default='inet-voc.shortnames.list')
    args.add_argument('-l','--labels',    type=check, default='inet-voc.labels.list')
    args=args.parse_args()

    with open(args.shortnames) as f:
        shortnames = [l.strip() for l in f]
    with open(args.labels) as f:
        labels = [l.strip() for l in f]
    assert len(shortnames)==len(labels),"{} {}".format(len(shortnames),len(labels))
    shortPlabel = { l:s for s,l in zip(shortnames,labels) }

    for i in args.directory: args.file.extend(dirfiles(i))
    for img in args.file:
        b1 = os.path.basename(img)
        b2 = os.path.basename(os.path.dirname(img))
        wname = os.path.join(b2,b1) if b2 is not None else b1
        sname = shortPlabel.get(b2, b1)
        print(wname,sname)
        showf(img)

