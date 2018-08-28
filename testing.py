#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
I get bored brushing my teeth. 
This script will search youtube until it finds a video that's two minutes long for me to 
watch while I scrub, to lessen the shitty experience that is dental care. 

This is a 'messing about and testing' script

Maybe also add some reminder to do those tongue scrub things? Flossing too?
'''

import json
import urllib.request
import string
import random
import webbrowser

count = 3
API_KEY = 'AIzaSyABQnIe2JmgV63knYmS4XpMNjkCpzxDLYM'
random = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

print('Searching for random videos with the string: [%s]' % random)

urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}".format(API_KEY,count,random)
webURL = urllib.request.urlopen(urlData)
data = webURL.read()
encoding = webURL.info().get_content_charset('utf-8')
results = json.loads(data.decode(encoding))

print(urlData)

videoIDs = []
for data in results['items']:
    videoID = data['id']['videoId']
    videoURL = 'https://www.youtube.com/watch?v='+videoID

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

def parse_duration(string):
    # Strip off the leading PT
    string = string[2:]
    
    total_seconds = 0

    # try and get the hours:
    if 'H' in string:
        H_index = string.index('H')
        hours = int(string[:H_index])
        string = string[H_index+1:]

        total_seconds += hours *60*60

    if 'M' in string:
        # get the minutes
        M_index = string.index('M')
        minutes = int(string[:M_index])
        string = string[M_index+1:]

        total_seconds += minutes*60

    if 'S' in string:
        # Get the seconds
        S_index = string.index('S')
        seconds = int(string[:S_index])

        total_seconds += seconds

    return total_seconds



for ID in videoIDs:
    # urlData = 'https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id={}&key={}'.format(ID, API_KEY)
    urlData = "https://www.googleapis.com/youtube/v3/videos?id={}&key={}&part=contentDetails".format(ID, API_KEY)
    webURL = urllib.request.urlopen(urlData)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    results = json.loads(data.decode(encoding))

    duration = results['items'][0]['contentDetails']['duration']
    duration = parse_duration(duration)

    videoURL = 'https://www.youtube.com/watch?v='+ID
    webbrowser.open_new_tab(videoURL)




