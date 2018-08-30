#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
I get bored brushing my teeth. 
This script will search youtube until it finds a video that's two minutes long for me to 
watch while I scrub, to lessen the shitty experience that is dental care. 

Maybe also add some reminder to do those tongue scrub things? Flossing too?

I also store the IDs of 2 min videos I find in a database, cos why not. 
Literally just a list of IDs.
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
        webbrowser.open_new_tab(videoURL)
        with open('database.txt', 'a') as f:
            f.write('{}\n'.format(ID))
        print('Wrote ID, [{}] to file.'.format(ID))
        return True

    return False

## MAIN ###
count = 50
with open('api_key.json', 'r') as f:
    API_KEY = json.load(f)
API_KEY = API_KEY['api_key']
print(API_KEY)
cont = False

which = 0 
# 0 - random word
# 1 - randomly generated string, repeated searches until matched to ID
# 2 - randomly generated IDs, until one matches.
# 3 - randomyoutube.net API 

## Different styles...

# Select a random word from words.txt and search for that. 
# Take a random result from the result.
if which == 0:
    cont = True
random = rand.randint(0, 466545)
while cont:
    random = rand.randint(0, 466545)
    with open('words.txt', 'r') as f:
        for i, line in enumerate(f):
            if i == random:
                word = line.strip()
                break
    print('Searching for the following word: [{}]'.format(word))
    urlData = "https://www.googleapis.com/youtube/v3/search?key={}&videoDuration=short&maxResults={}&part=snippet&type=video&q={}".format(
        API_KEY,count,word
        )

    # Request and parse the search returns
    webURL = urllib.request.urlopen(urlData)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    results = json.loads(data.decode(encoding))

    videoIDs = []
    for data in results['items']:
        videoID = data['id']['videoId']
        videoURL = 'https://www.youtube.com/watch?v='+videoID
        videoIDs.append(videoID)

    for videoID in videoIDs:
        cont = use_ID(videoID, API_KEY) # True if we found a compatible video
        print('ID: %s, cont: %r' % (videoID, bool(cont)))
        if cont:
            cont = not cont
            break
        else:
            cont = True
     

# Search for a random string of three characters and take that as the ID
if which == 1:
    length = 4
    cont = True
while cont:
    random = ''.join(rand.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))
    # random = 'v='+random
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
        if random in videoID:
            videoIDs.append(videoID)

    print(videoIDs)

    for videoID in videoIDs:
        cont = use_ID(videoID, API_KEY) # True if we found a compatible video
        # print('ID: %s, cont: %r' % (videoID, bool(cont)))
        if cont:
            cont = not cont
            break
        else:
            cont = True
    if cont:
        print("Didn't find a 2 minute video! I'll try again.")
        


# Try generating a full ID string and query it. This turns up invalid IDs almost every time.
if which == 2:
    cont = True
while cont:
    random = ''.join(rand.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits + '_-') for _ in range(11))
    print('Searching for random ID: [%s]' % random)
    
    cont = use_ID(random, API_KEY)
    cont = not cont
    print(cont)
    

# Use the random video API from randomyoutube.net. Hardcoded API key - fight me nerd.
if which == 3:
    cont = True
fail = 0
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
        print("Didn't get a response")
        fail += 1
    if fail >= 5:
        cont = False

