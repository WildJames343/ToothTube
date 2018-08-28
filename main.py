#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
I get bored brushing my teeth. 
This script will search youtube until it finds a video that's two minutes long for me to 
watch while I scrub, to lessen the shitty experience that is dental care. 

Maybe also add some reminder to do those tongue scrub things? Flossing too?
'''

import json
import urllib.request
import string
import random


count = 1
API_KEY = 'AIzaSyABQnIe2JmgV63knYmS4XpMNjkCpzxDLYM'
random = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}".format(API_KEY,count,random)
webURL = urllib.request.urlopen(urlData)
data = webURL.read()
encoding = webURL.info().get_content_charset('utf-8')
results = json.loads(data.decode(encoding))


videoIDs = []
for data in results['items']:
    videoID = data['id']['videoId']
    videoURL = 'https://www.youtube.com/embed/'+videoID

    videoKind        = data['kind']
    snippet          = data['snippet']
    videoTitle       = snippet['title']
    videoDescription = snippet['description']
    videoChannel     = snippet['channelTitle']

    print('Video Title: [%s]\n - URL: [%s]\n - Kind: [%s]\n - Description: [%s]\n - Channel: [%s]\n-----------------' % 
        (videoTitle, videoURL, videoKind, videoDescription, videoChannel)
        )
    videoIDs.append(videoID)

print('\nFetched.\n')

for ID in videoIDs:
    urlData = 'https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id={}&key={}'.format(ID, API_KEY)
    print(urlData)
    webURL = urllib.request.urlopen(urlData)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    results = json.loads(data.decode(encoding))

    for i in results.keys():
        print(i.__class__, i)





