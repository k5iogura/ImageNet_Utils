import sys
import os
import time
import tarfile
from pdb import set_trace

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    import urlparse
    import urllib

class ImageNetDownloader:
    def __init__(self):
        self.host = 'http://www.image-net.org'

    def download_file(self, url, desc=None, renamed_file=None):
        new = False
        u = urllib2.urlopen(url)

        scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
        filename = os.path.basename(path)
        if not filename:
            filename = 'downloaded.file'

        if not renamed_file is None:
            filename = renamed_file

        if desc:
            filename = os.path.join(desc, filename)

        file_size_dl = 0
        block_sz = 8192
        while True:
            filename = filename.replace('.JPG','.jpg')
            if os.path.exists(filename):
                file_size_dl = 3*block_sz # set as dummy
                sys.stdout.write("skipped {} already existed".format(filename))
                break
            meta = u.info()
            meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
            meta_length = meta_func("Content-Length")
            if 'content-type' in meta and 'image' not in meta['content-type']:
                sys.stdout.write(" {} ".format(meta['content-type']))
                break
            if 'content-type' in meta and 'image/' in meta['content-type']:
                base, meta_image_type = meta['content-type'].split('/')[:2]
                url_suffix    = os.path.splitext(os.path.basename(filename))[-1]
                if url_suffix != meta_image_type:sys.stdout.write(" contente-type:{} ".format(meta_image_type))

            file_size = None
            if meta_length:
                file_size = int(meta_length[0])

            f = open(filename, 'wb')
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break
                if file_size_dl == 0 and len(buffer) < block_sz:
                    break
                file_size_dl += len(buffer)
                f.write(buffer)

                status = "{0:16}".format(file_size_dl)
                if file_size:
                    status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
                status += chr(13)
            if file_size_dl >= 3*block_sz:
                sys.stdout.write("Downloading: {}".format(url))
                new = True
            break
        if os.path.exists(filename) and file_size_dl < 3*block_sz:
            os.remove(filename)
            filename = None
        else:
            sys.stdout.write(" Bytes: {}".format(file_size_dl))
        sys.stdout.write("\n")

        return filename, new

    def extractTarfile(self, filename):
        tar = tarfile.open(filename)
        tar.extractall()
        tar.close()

    def downloadBBox(self, wnid):
        filename = str(wnid) + '.tar.gz'
        url = self.host + '/downloads/bbox/bbox/' + filename
        try:
            filename = self.download_file(url, self.mkWnidDir(wnid))
            currentDir = os.getcwd()
            os.chdir(wnid)
            self.extractTarfile(filename)
            print 'Download bbbox annotation from ' + url + ' to ' + filename
            os.chdir(currentDir)
        except Exception, error:
            print 'Fail to download' + url

    def getImageURLsOfWnid(self, wnid):
        url = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=' + str(wnid)
        f = urllib.urlopen(url)
        contents = f.read().split('\n')
        imageUrls = []

        for each_line in contents:
            # Remove unnecessary char
            each_line = each_line.replace('\r', '').strip()
            if each_line:
                imageUrls.append(each_line)

        return imageUrls

    def mkWnidDirOrg(self, wnid):
        if not os.path.exists(wnid):
            os.mkdir(wnid)
        return os.path.abspath(wnid)

    def mkWnidDir(self):
        iname = 'inet_images'
        if not os.path.exists(iname):
            os.mkdir(iname)
        return os.path.abspath(iname)

    def downloadImagesByURLs(self, wnid, imageUrls, num_images):
        sys.stdout.flush()
        print("*"*30)
        print("**  START {}".format(wnid))
        print("*"*30)
        sys.stdout.flush()
        # save to the dir e.g: n005555_urlimages/
        wnid_urlimages_dir = os.path.join(self.mkWnidDir(), str(wnid))
        # wnid_urlimages_dir = os.path.join(self.mkWnidDir(wnid), str(wnid) + '_urlimages')
        print("mkdir",wnid_urlimages_dir)
        if not os.path.exists(wnid_urlimages_dir):
            os.mkdir(wnid_urlimages_dir)

        ready_fileN = len( [ i for i in os.listdir(wnid_urlimages_dir) ] )
        if ready_fileN >= num_images: return ready_fileN

        gets = 0
        new  = False
        for urlNo, url in enumerate(imageUrls):
            if urlNo+1 <= ready_fileN:
                gets += 1
                continue
            sys.stdout.write("{} {}/{}/{} ".format(wnid, gets, urlNo, len(imageUrls)))
            try:
                filename, new = self.download_file(url, wnid_urlimages_dir)
            except Exception, error:
                new = False
                print('Fail to download : ' + url +' '+ str(error))
            if new: gets+=1
            if gets >= num_images:break
        return gets

    def downloadOriginalImages(self, wnid, username, accesskey):
        download_url = 'http://www.image-net.org/download/synset?wnid=%s&username=%s&accesskey=%s&release=latest&src=stanford' % (wnid, username, accesskey)
        try:
             download_file = self.download_file(download_url, self.mkWnidDir(wnid), wnid + '_original_images.tar')
        except Exception, erro:
            print 'Fail to download : ' + download_url

        currentDir = os.getcwd()
        extracted_folder = os.path.join(wnid, wnid + '_original_images')
        if not os.path.exists(extracted_folder):
            os.mkdir(extracted_folder)
        os.chdir(extracted_folder)
        self.extractTarfile(download_file)
        os.chdir(currentDir)
        print 'Extract images to ' + extracted_folder

