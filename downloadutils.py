#!/usr/bin/env python
import argparse
import sys
import os
import _init_paths
import imagedownloader
import pref_utils
import threading, logging
from copy import copy
from pdb import set_trace

safedomains = ['.gov/', '.jp/', '.edu/', '.ie/', '.us/', '.ch/', '.flickr.com/']
def filterSafeDomainOnly(ilist):
    selected = []
    for url in ilist:
        for safedomain in safedomains:
            if safedomain in url: selected.append(url)
    return selected

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Help the user to download, crop, and handle images from ImageNet')
    p.add_argument('--wnid', nargs='+', help='ImageNet Wnid. E.g. : n02710324')
    p.add_argument('--wnid_list', type=str, default=None)
    p.add_argument('--cat',action="store_true",default=0)
    p.add_argument('-n','--num_images', type=int, default=100)
    p.add_argument('-th','--max_threads', type=int, default=10)
    p.add_argument('--downloadImages', help='Should download images', action='store_true', default=False)
    p.add_argument('--downloadOriginalImages', help='Should download original images', action='store_true', default=False)
    p.add_argument('--downloadBoundingBox', help='Should download bouding box annotation files', action='store_true', default=False)
    p.add_argument('-a', '--urls_all', action='store_true')
    # p.add_argument('--timeout', '-t', type=int, default=10, help='Timeout per image in seconds')
    # p.add_argument('--retry', '-r', type=int, default=10, help='Max count of retry for each image')
    p.add_argument('--verbose', '-v', action='store_true', help='Enable verbose log')
    args = p.parse_args()
    if args.wnid_list is not None:
        with open(args.wnid_list) as f:
            args.wnid = [ wnid.strip() for wnid in f ]
    if args.wnid is None:
        print('No wnid')
        sys.exit()
    logging.basicConfig(level=logging.DEBUG,format='%(message)s')

    downloader = imagedownloader.ImageNetDownloader()
    username = None
    accessKey = None
    userInfo = pref_utils.readUserInfo()
    if not userInfo is None:
        username = userInfo[0]
        accessKey = userInfo[1]

    def kernel_getWnid(iid,imgAcat,ret):
        ilist = downloader.getImageURLsOfWnid(iid)
        ilist = filterSafeDomainOnly(ilist)
        msg = "{:15s} {:6d} urls".format(iid,len(ilist))
        if len(ilist)>=imgAcat:msg = msg + " *"
        logging.debug(msg)
        ret.append([iid,len(ilist)])

    def thread_getWnid(wnid,imgAcat):
        max_ths = args.max_threads
        ret = []
        ths = []
        for iid in wnid:
            if len(ths) < max_ths:
                th = threading.Thread(target=kernel_getWnid,args=(iid,imgAcat,ret,))
                th.start()
                ths.append(th)
                if len(ths) == max_ths:
                    for th in ths:
                        th.join()
                    ths = []
        for th in ths:
            th.join()
        return ret

    if args.cat:
        imgAcat= args.num_images
        filename = 'imagenet.labels.safedomain'+str(imgAcat)+'.list'
        with open(filename,"w") as flickr:
            for ret in thread_getWnid(args.wnid, imgAcat):
                iid, nurls = ret
                if nurls>=imgAcat:
                    flickr.write(iid+"\n")
        sys.exit(0)

    done_labels = []
    ignores_txt = 'ignore.list'
    if os.path.exists(ignores_txt):
        with open(ignores_txt) as f:
            done_labels = [ l.strip() for l in f]
    else:
        with open(ignores_txt,"w") as ignores:pass

    max_threads = args.max_threads
    threads = []
    if args.downloadImages is True:
        for iid in args.wnid:
            if iid in done_labels:continue
            if len(threads) < max_threads:
                ilist = downloader.getImageURLsOfWnid(iid)
                if not args.urls_all: ilist = filterSafeDomainOnly(ilist)
                th = threading.Thread(target=downloader.downloadImagesByURLs, args=(iid, ilist, args.num_images))
                th.start()
                threads.append(th)
                if len(threads) >= max_threads:
                    for th in threads:
                        th.join()
                        with open(ignores_txt,"a") as ignores:ignores.write(th.name+'\n')
                    threads = []
        for th in threads:
            th.join()
            with open(ignores_txt,"a") as ignores:ignores.write(th.name+'\n')

    if args.downloadBoundingBox is True:
        for id in args.wnid:
            # Download annotation files
            downloader.downloadBBox(id)

    if args.downloadOriginalImages is True:
    # Download original image, but need to set key and username
        if username is None or accessKey is None:
            username = raw_input('Enter your username : ')
            accessKey = raw_input('Enter your accessKey : ')
            if username and accessKey:
                pref_utils.saveUserInfo(username, accessKey)

        if username is None or accessKey is None:
            print('need username and accessKey to download original images')
        else:
            for id in args.wnid:
                downloader.downloadOriginalImages(id, username, accessKey)
