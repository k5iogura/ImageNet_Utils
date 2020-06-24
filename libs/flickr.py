from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from math import ceil
import os, time, sys, argparse

def getUrls(keyword, num_of_photos, per_page=100, verbose=False):

    # Flicker API key from flickr app name "fromFLICKR"
    # https://www.flickr.com/services/apps/create/noncommercial/?

    key = "3a87ffaee7fc6617272a73e3de524123"
    secret = "2dc9b8ea7c839dd8"

    # FlickrAPI(key, secret, data_format)
    flickr = FlickrAPI(key, secret, format='parsed-json')

    # flickr.photos.search(text_for_search, per_page, media, short, safe_search, extra='keyname_of_urls')
    # 'url_q' : special word to get urls
    urls      = []
    PerPage   = min(num_of_photos, per_page)
    num_pages = int(ceil(num_of_photos/PerPage))
    for i in range(1,num_pages+1):
        result = flickr.photos.search(
            #text = keyword,
            tags=keyword,
            tag_mode='all', 
            page = i,
            per_page = PerPage,
            media = 'photos',
            sort = 'relevance',
            safe_search = 1,
            extras = 'url_q, licence'
        )
        photos = result['photos']
        url = [ { 'id':p['id'], 'title':p['title'], 'url_q':p['url_q'], 'w':p['width_q'], 'h':p['height_q'] } for p in photos['photo'] ]
        if len(url) <=0 : break
        urls.extend(url)
        if len(urls) >= int(photos['total']) : break
        if verbose : sys.stderr.write("{} {} {} {} {} {} {}\n".format(i,num_of_photos, PerPage,num_pages,len(url),len(urls),int(photos['total'])))
    return urls

if __name__=='__main__':
    args = argparse.ArgumentParser()
    args.add_argument('keyword', type=str)
    args.add_argument('-n', '--num_of_images', type=int, default=100)
    args.add_argument('-o', '--output', type=str, default=None)
    args = args.parse_args()

    num_of_photos = args.num_of_images
    keyword = args.keyword
    urls = getUrls(keyword, num_of_photos)

    # Output log file
    log_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]+'.log'
    sys.stderr.write("* write out log into \"{}\"".format(log_name)+'\n')
    with open(log_name,'w') as f:
        for url in urls:
            f.write("{} {} {} {} {}\n".format(url['id'], url['title'], url['w'], url['h'], url['url_q']))

    # Dump Results
    if args.output is not None:
        with open(args.output,'w') as f:
            for url in urls:
                f.write("{}\n".format(url['url_q']))
    else:
        for url in urls: print(url['url_q'])

    sys.exit(0)

#for url in urls:
#    print(url[2])

# photos.keys()
# dict_keys(['page', 'pages', 'perpage', 'total', 'photo'])
# >>> photos['page']
# 1
# >>> photos['pages']
# 63830
# >>> photos['perpage']
# 10
# >>> photos['total']
# '638300'
# >>> photos['photo'].keys()
# >>> photos['photo'][0]
# {'id': '49872208862', 'owner': '146613830@N05', 'secret': 'a731c82667', 'server': '65535', 'farm': 66, 'title': 'Beaver', 'ispublic': 1, 'isfriend': 0, 'isfamily': 0, 'url_q': 'https://live.staticflickr.com/65535/49872208862_a731c82667_q.jpg', 'height_q': 150, 'width_q': 150}
