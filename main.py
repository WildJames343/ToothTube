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
import random as rand
import webbrowser

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

def use_ID(ID, key):
    urlData = "https://www.googleapis.com/youtube/v3/videos?id={}&key={}&part=contentDetails".format(ID, key)

    webURL = urllib.request.urlopen(urlData)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    results = json.loads(data.decode(encoding))

    if results['pageInfo']['totalResults'] == 0:
        print('Not a valid ID')
        return False

    videoURL = 'https://www.youtube.com/watch?v='+ID

    duration = results['items'][0]['contentDetails']['duration']
    duration = parse_duration(duration)
    # print('Found a video %d seconds long.' % duration)

    # If the video is about 2 minutes long, open it
    if duration > 110 and duration < 130:
        videoURL = 'https://www.youtube.com/watch?v='+ID
        # webbrowser.open_new_tab(videoURL)
        with open('database', 'a') as f:
            f.write('{}\n'.format(ID))
        print('Wrote ID, [{}] to file.'.format(ID))
        return True

    return False

count = 1
API_KEY = 'AIzaSyABQnIe2JmgV63knYmS4XpMNjkCpzxDLYM'

cont = False
while cont:
    # Search for a random string of three characters and take that as the ID
    random = ''.join(rand.choice(string.ascii_uppercase + string.digits) for _ in range(3))
    print('Searching for random videos with the string: [%s]' % random)

    urlData = "https://www.googleapis.com/youtube/v3/search?key={}&videoDuration=short&maxResults={}&part=snippet&type=video&q={}".format(
        API_KEY,count,random
        )
    # https://www.youtube.com/results?sp=CAMSBBABGAE%253D&search_query=SEARCH

    webURL = urllib.request.urlopen(urlData)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    results = json.loads(data.decode(encoding))

    videoIDs = []
    for data in results['items']:
        videoID = data['id']['videoId']
        videoURL = 'https://www.youtube.com/watch?v='+videoID

        videoIDs.append(videoID)

    print(videoIDs)

    for videoID in videoIDs:
        cont = use_ID(videoID, API_KEY)
        cont = not cont
        if cont:
            break

cont = False
while cont:
    random = ''.join(rand.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits + '_-') for _ in range(11))
    print('Searching for random ID: [%s]' % random)
    
    cont = use_ID(random, API_KEY)
    cont = not cont
    print(cont)
    

cont = True
RAND_API_KEY = 'Tx5DngnUxrHmzSOmPjfuc7GTAafKN9qRbmTB6Uk5XpIIs1ggmRB5GJkivpIH'
urlData = 'https://randomyoutube.net/api/getvid?api_token={}'.format(RAND_API_KEY)
while cont:
    webURL  = urllib.request.urlopen(urlData)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    response = json.loads(data.decode(encoding))

    try:
        videoID = response['vid']

        cont = use_ID(videoID, API_KEY)
        cont = not cont
    except:
        pass
        print("Didn't get a response")

