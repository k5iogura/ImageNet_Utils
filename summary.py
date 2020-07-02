#!/usr/bin/env python3

import sys,re,os,argparse
import shutil, subprocess

def searchdir( d ):
    files = [ f for f in os.listdir( d ) if re.search( r'\.jpg$', f ) ]
    return len(files), files

if __name__=='__main__':
    def check( d ):
        if type(d)==list:
            for i in d: assert os.path.exists( i )
        if type(d)!=str : os.path.exists( d )
        return d
    args = argparse.ArgumentParser()
    args.add_argument('-d','--dirlist', nargs='+',    default=[ 'inet_images', 'inet_flickr' ])
    args.add_argument('-w','--wnid_list', type=check, default='imagenet1k.wnid.list')
    args.add_argument('-a','--words_txt', type=str,   default='words.inet.txt')
    args.add_argument('-j','--ja_flag',   action='store_true')
    args.add_argument('-r','--reverse',   action='store_true')
    args.add_argument('-top', nargs=1, type=int, default=100000)
    args = args.parse_args()
    if type(args.top) == list: args.top = args.top[0]

    # which translator
    ja_sh = '2ja.sh'
    if not shutil.which(ja_sh): args.ja_flag = False

    # load Shortnames
    words = {}
    idx_id, idx_word = 0, 1
    if os.path.exists( args.words_txt ):
        with open(args.words_txt) as f:
            witems = [ i.strip().split('\t') for i in f ]
            for w in witems: words[ w[idx_id] ] = w[idx_word]

    # load WNID
    with open(args.wnid_list) as f:
        wnid = [ i.strip() for i in f ]

    # make images data
    img2info_tmp = {}
    for iid in wnid:
        if all( [ not os.path.exists( os.path.join( dirx, iid ) ) for dirx in args.dirlist ] ):
            print("{} class has no images and directory but be in {} file".format(iid,args.wnid_list), file=sys.stderr)
        for dirx in args.dirlist:
            img_dir = os.path.join( dirx, iid )
            if os.path.exists( img_dir ):
                Nimg, _ = searchdir( img_dir )
                img2info_tmp.setdefault( iid, 0 )
                img2info_tmp[ iid ] += Nimg
    img2info = [ { 'id':k, 'images':img2info_tmp[k] } for k in img2info_tmp.keys() ]

    # sorting at in-order from minumum:0 to maximum:-1
    img2info.sort( key = lambda x: x['images'], reverse = args.reverse )

    # print information out
    total_img = 0
    for info in reversed(img2info):
        wnid, Nimg = info['id'], info['images']
        total_img += Nimg

    # print out
    print_out = 0
    for info in reversed(img2info):
        print_out += 1
        wnid, Nimg = info['id'], info['images']
        if wnid in words.keys():
            Iimg = words[ wnid ]
            if args.ja_flag:
                jIimg = subprocess.check_output( [ ja_sh, words[ wnid ] ] )
                jIimg = jIimg.decode('utf-8').strip()
                Iimg += " / "+jIimg
        else:
            Iimg = ""
        if print_out <= args.top:
            print("{:-6d} {} {}".format( Nimg, wnid, Iimg ))
        else:
            print("end of top {}".format(args.top))
            break

    print("{:12s} {:6d} images".format(img2info[0]['id'] ,img2info[0]['images']), file=sys.stderr)
    print("{:12s} {:6d} images".format(img2info[-1]['id'],img2info[-1]['images']), file=sys.stderr)
    print("{} classes images in {}".format(len(img2info),args.dirlist), file=sys.stderr)
    print("{:.3f} images/class".format(total_img/len(img2info)), file=sys.stderr)

