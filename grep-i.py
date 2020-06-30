#!/usr/bin/env python
import sys,re,os,argparse

def check(f):
    assert os.path.exists(f),"not found".format(f)
    return str(f)

args=argparse.ArgumentParser()
args.add_argument('-i','--keyword_file',type=check,required=True,help='file including keyword file')
args.add_argument('-o','--type',type=str,choices=['id','shortnames','list'],default='shortnames',help='output type')
args.add_argument('target',type=check,help='target for searching')
args=args.parse_args()

with open(args.keyword_file) as f:
    wd_file = [ i.strip() for i in f ]

with open(args.target) as f:
    tg_file = [ i.strip() for i in f ]

for w in wd_file:
    for tg in tg_file:
        iid, wd = tg.split('\t')
        if wd == w:
            if args.type == 'id':
                print(iid)
            elif args.type == 'list':
                print("{} {}".format(iid,wd))
            else:
                print(w)
            break
