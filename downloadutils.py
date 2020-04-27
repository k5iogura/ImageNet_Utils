#!/usr/bin/env python
import argparse
import sys
import os
import _init_paths
import imagedownloader
import pref_utils
import threading
from pdb import set_trace

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
    # p.add_argument('--jobs', '-j', type=int, default=1, help='Number of parallel threads to download')
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

    downloader = imagedownloader.ImageNetDownloader()
    username = None
    accessKey = None
    userInfo = pref_utils.readUserInfo()
    if not userInfo is None:
        username = userInfo[0]
        accessKey = userInfo[1]

    if args.cat:
        needcat=1000
        imgAcat= 900
        filename = 'imagenet.labels.flickr'+str(imgAcat)+'.list'
        with open(filename,"w") as flickr:
            for iid in args.wnid:
                try:
                    ilist = downloader.getImageURLsOfWnid(iid)
                except:
                    print("retry getting url list")
                    continue
                ilist = [ url for url in ilist if '.flickr.com' in url]
                sys.stdout.write("{:10s}\t{:6d} images".format(iid,len(ilist)))
                if len(ilist)>=imgAcat:
                    sys.stdout.write("\t* {}".format(needcat))
                    flickr.write(iid+"\n")
                    flickr.flush()
                    needcat-=1
                sys.stdout.write("\n")
                if needcat<=0:break
        sys.exit(0)

    max_threads = args.max_threads
    threads = []
    if args.downloadImages is True:
        for iid in args.wnid:
            if len(threads) < max_threads:
                ilist = downloader.getImageURLsOfWnid(iid)
                th = threading.Thread(target=downloader.downloadImagesByURLs, args=(iid, ilist, args.num_images))
                th.start()
                threads.append(th)
                if len(threads) >= max_threads:
                    for th in threads:
                        th.join()
                    threads = []

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
