# For imagenet 1k images

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
```
 $ ./downloadutils.py --cat -n 1 --wnid_list imagenet1k.wnid.list -th 30
 $ python ./downloadutils.py --downloadImages -th 30 --wnid_list imagenet.labels.safedomain1.list -n 1000
```

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
```
 $ ./iflickr.sh
```

## Make train.txt and valid.txt  
```
 $ ./make_trainval.sh
```

## Results  
see and check inet_images/ and inet_flickr/ directories.  

```
 $ find inet_images inet_flickr -iname \*.jpg | wc
 981077
```

see and check train.txt and valid.txt  
