import http.client
import json
import urllib

#function to check if user wants more info on a given film
def more_info():
    global filmtitle
    print('Do you want some more info about ', filmtitle)
    inp = input('Y/N')
    if inp == 'y' or inp == 'Y':
        return True
    else:
        return False

#Function to retrieve synopsis of given film
def get_synopsis():
    global filmid
    conn.request("GET", "/title/get-synopses?tconst="+filmid, headers=headers)
    res = conn.getresponse()
    data = res.read().decode()
    jss = json.loads(data)
    if len(jss) > 0 and 'text' in jss[0]:
        print(jss[0]['text'])
    else:
        print('No result found')

#Function to retrieve trivia of given film
def get_trivia():
    global filmid
    conn.request("GET", "/title/get-trivia?tconst="+filmid, headers=headers)
    res = conn.getresponse()
    data = res.read().decode()
    jss = json.loads(data)

    if 'unspoilt' in jss:
        unspoiler_trivia = len(jss['unspoilt'])
        print('The amount of trivias without spoilers are: ', unspoiler_trivia)

    if 'spoilt' in jss:
        spoiler_trivia = len(jss['spoilt'])
        print('The amount of trivias which contain spoilers are: ', spoiler_trivia)
        print('Would you like to see trivias with spoilers? (Y/N)')
        inp = input()
    else:
        inp = 'n'

    triviacount = 1
    if inp == 'y' or inp == 'Y':
        for trivia in jss['spoilt']:
            print(triviacount)
            print(trivia['text'])
            print(' ')
            triviacount += 1
    for trivia in jss['unspoilt']:
        print(triviacount)
        print(trivia['text'])
        print('')
        triviacount += 1


#required information to connect to rapidapi IMDB API
conn = http.client.HTTPSConnection("imdb8.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "imdb8.p.rapidapi.com",
    'x-rapidapi-key': "INSERT RADPID API KEY HERE"
    }

#Variable to check if we're still running
working = True
#Variable to check if someone wants to start over
so = False
while working:
    inp = str()
    print('For which film or tv series would you like some information?')
    inp = input()
    search = urllib.parse.urlencode({'q':inp})
    search = "/auto-complete?"+search
    conn.request("GET", search, headers=headers)

    res = conn.getresponse()
    data = res.read().decode()
    jss = json.loads(data)
    
    resultsfound = len(jss['d'])

    print('Results found: ', resultsfound)

    filmid = str()
    filmtitle = str()
    count = 1
    for result in jss['d']:
        print('\n')
        print('Result number: ', count)
        if 'l' in result:
            print('Title: ', result['l'])
        if 'q' in result:
            print('Type: ', result['q'])
        if 's' in result:
            print('Top cast: ', result['s'])
        count += 1

    unknownresult = True

    while unknownresult:
        print('For which result would you like some more information? Press 0 to start over.')
        res = input()

        try:
            res = int(res)
            if res > resultsfound:
                print('Result not found')
            elif res == 0:
                so = True
                break
            else:
                filmid = jss['d'][res-1]['id']
                if 'l' in jss['d'][res-1]:
                    filmtitle = jss['d'][res-1]['l']
                unknownresult = False
        except:
            print('A number has to be given')
        if so:
            so = False
            continue

    print(filmid)
    print(filmtitle)
    
    unknowninfo = True
    while unknowninfo:
        print('What kind of information would you like about ', filmtitle)
        print('Or press 0 to start over')
        print('1. Synopsis')
        print('2. Trivia')
        res = input()

        try:
            res = int(res)
            if res == 1:
                print('Synopsis is coming')
                get_synopsis()
                if more_info():
                    continue
                else:
                    so = True
                    break
            elif res == 2:
                print('Trivia is coming')
                get_trivia()
                if more_info():
                    continue
                else:
                    so = True
                    break
            elif res == 0:
                so = True
                break
            else:
                print('No valid input')
        except:
            print('A number has to be given')
    if so:
        so = False
        continue