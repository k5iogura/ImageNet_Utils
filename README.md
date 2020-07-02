# For imagenet 1k classes images

## Providing files  

- imagenet1k.shortnames.list  
  from ImageNet web site, copy and past.  
  but 'crane' words represents twice on web page, so modify it.  

- word.inet.txt  
  from pjreddie web site via wget.  
  but 'crane' words represents twice on web page, so modify it.  

**Notice**  
imagenet dataset has duplicated definitions of 'crane'.  
Split 'crane' category to 'crane, Wading birds' and 'crane, Lifing device' in imagenet1k.shortnames.list and words.inet.txt.  
So, use words.inet.txt instead of words.txt.  

<details><summary>imagenet1k.shortnames.list</summary>  
<p>

```
kit fox, Vulpes macrotis
English setter
Australian terrier
...
```

</p></details>  

<details><summary>words.inet.txt</summary>  
<p>

```
n00004475	organism, being
n00005787	benthos
n00006024	heterotroph
...
```

</p></details>  

To make imagenet 1K wnid list, type below,  
```
 $ ./grep-i.py -i imagenet1k.shortnames.list words.inet.txt -o id > imagenet1k.wnid.list
```

<details>
<summary>imagenet1k.wnid.list example</summary>  
<p>  

```
n02119789  
n02100735  
n02096294  
...  
```

</p>
</details>  

## Download images by **ImageNet URLs**  
first, make wnid list.  
```
 $ ./downloadutils.py --cat -n 1 --wnid_list imagenet1k.wnid.list -th 30
```

and download 1000 images/class from ImageNet URLs with -n 1000. if need more images/class then change -n option.  
```
 $ python ./downloadutils.py --downloadImages -th 30 --wnid_list imagenet.labels.safedomain1.list -n 1000
```

30 threads download images.  

<details>  
<summary>imagenet.labels.safedomain1.list</summary>  
<p>  

```
n02119789
n02442845
...
```

</p>
</details>  

## Download images by **flickr URLs**  
ImageNet URLs is not enough URLs per class.  
below script can donwload (1000 - ImageNet URLs) images via flickr API.  
1000 is fixed value in script, change it if need.  

```
 $ ./iflickr.sh
```

## Make train.txt and valid.txt  
find JPG images from ./inet_images or ./inet_flickr directories and make path list as train.txt and valid.txt.  
```
 $ ./make_trainval.sh
```

see and check train.txt valid.txt which include file paths of target images to use training.  
its are randm sorted and splited to 5k validation images and about 1M training images.  

## Results  
see and check inet_images/ and inet_flickr/ directories.  

```
 $ find inet_images inet_flickr -iname \*.jpg | wc
 981077
```
your number of images may be different because flickr or imagenet url link down so,on.  
1K categories have about 1M images.  

or  
```
 $ ./summary.py
```

<details><summary>outputs example below</summary><p>  

```
    ...
    88 n02089973 English foxhound
    83 n03485407 hand-held computer, hand-held microcomputer
    70 n02112706 Brabancon griffon
    63 n04579145 whiskey jug
n04399382         0 images warning!
n04579145        63 images
n04209133      1099 images
999 classes images in ['inet_images', 'inet_flickr']
982.986 images/class

here n04399382 directory is empty, it denote that there is no images for category n04399382 to train classifier. please be carefly.  
 $ grep n04399382 words.inet.txt
n04399382       teddy, teddy bear
```

</p></details>  
