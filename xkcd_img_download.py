#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
import bs4
import os
import html5lib
import shutil

url = 'http://xkcd.com/'
loc = input('enter folder name')

if os.path.isdir(loc) == True:
    shutil.rmtree(loc) 
else: 
    os.makedirs(loc)


while not url.endswith('#'): 
    
    print ('Downloading %s page...' % url)
    res = requests.get(url) 

    soup = bs4.BeautifulSoup(res.text) 

    comicElem = soup.select('#comic img') 
    if comicElem == []: 
        print ('Couldn\'t find the image!')
    else:
        try:
            comicUrl = 'http:' + comicElem[0].get('src')             #getting comic url and then downloading its image
            print('Downloading image %s.....' %(comicUrl))
            res = requests.get(comicUrl)
            res.raise_for_status()

        except requests.exceptions.MissingSchema:
        #skip if not a normal image file
            prev = soup.select('a[rel="prev"]')[0]
            url = 'http://xkcd.com' + prev.get('href')
            continue

        imageFile = open(os.path.join(loc,os.path.basename(comicUrl)),'wb')     #write  downloaded image to hard disk
        for chunk in res.iter_content(10000):
            imageFile.write(chunk)
        imageFile.close()

        #get previous link and update url
        prev = soup.select('a[rel="prev"]')[0]
        url = "http://xkcd.com" + prev.get('href')

print ('Done!')


# In[ ]:




