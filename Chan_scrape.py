#!/usr/bin/env python
# coding: utf-8

# In[4]:


import urllib
#import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os

page_url = input('Enter the URL of board: ')
try:
    req = Request(url = page_url, headers={'User-Agent': 'Mozilla/5.0'})
except:
    print("Can't get to the url")

page_webcode = urlopen(req).read()
soup = BeautifulSoup(page_webcode, 'html.parser')

def getFileLinks (soup):
    fuzzy = (soup.findAll('a', {'class':'fileThumb','href': True}))
    links = [fuzz.get('href') for fuzz in fuzzy]
    return links

def getFileNames (soup):
    name_ = soup.findAll('div',{'class':'fileText'})
    names_list_ = [(name_[i].find('a',href=True)) for i in                  range(0,len(name_))]
    names_list = [name.text for name in names_list_]
    return names_list

def getBoardName (page_url):
    board = page_url.split('org/')[1].split('/thread')[0]
    return board

def getPostTitle (soup):
    name_ = soup.find('span', {'class':'name'})
    name = str(name_).split('"name">')[1].split('</span>')[0]
    return name

def getPostNum (soup):
    number_ = soup.find('span', {'class':'postNum desktop' })
    number = str(number_).split('#p')[1].split('"')[0]
    return number

home = 'D:/'
chan = page_url.split('boards.')[1].split('.org')[0]
if (chan=='4channel'):
    chan = '4chan'
board = getBoardName(page_url)
post_title = getPostTitle(soup)
post_number = getPostNum(soup)
links = getFileLinks(soup)

post_path = home+chan+'/'+board+'/'+post_title+'_'+post_number+'/'

try:
    os.makedirs(post_path)
except OSError:
    print("Can't create a folder at path:", post_path)

j = 0
file_names = getFileNames(soup)
while (j < len(links)):
    filename = os.path.join(post_path, file_names[j])
    urllib.request.urlretrieve('https:'+links[j], filename)
    print(j)
    j+=1
    
print('Finished')

