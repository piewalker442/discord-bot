#brought to you by nananananate

#mapq_output


import google_api_interact
import traceback
import asyncio
import twitter_interact
import json
import re
import requests

Stopswitch_Proxy_g_plus = 1
County_Bluff_youtube = 'youtube-id'
Stopswitch_Proxy_youtube = 'youtube-id'
test_g_plus = 1
yoda = 'youtube-id'
sim_9 = 'youtube-id'

Sheets_practice = 'sheet_id'
Insomnia_sheet = 'sheet-id'



DEBUG = False

def dp(wot: str):
    '''Debug Print (hence dp) '''
    if DEBUG:
        print(wot)

class TestError(Exception):
    pass

###### OBTAINING JSON, WRITING/READING LOG FILE


def get_google_plus_json(userid: int):
    '''get that google+ shit'''
    url = google_api_interact.build_google_url(userid)

    #print(url)

    return google_api_interact.get_json(url)






def get_youtube_json(userid: str):
    ''' oh yeah bby I want some JSON vids ;) '''
    url = google_api_interact.build_youtube_url(userid)

    #print(url)

    return google_api_interact.get_json(url)

def get_sheets_json(sheet_id: str, sheet_range: 'A1:A1 FORMAT'):
    url = google_api_interact.build_sheets_url(sheet_id, sheet_range)

    #print(url)

    return google_api_interact.get_json(url)


def get_twitter_statuses(userid = None):
    timeline = Status_collector()

    statuses = timeline.return_statuses()

    return statuses


def recording_post(content, outfile):
    'records BOT post on file'
    myfile = open(outfile, 'a')
    if type(content) == list:
        for line in content:
            try:
                myfile.write(line + '\n')
            except:
                myfile.write('INVALID CHARACTER IN LINE'+ '\n')
                traceback.print_exc()

    else:
        try:
            myfile.write(content + '\n')
        except:
            print('FAILED TO WRITE')

    myfile.close()

def read_file(file):
    '''For reading log file'''
    infile = open(file, 'r')
    lines = infile.readlines()
    infile.close()
    formatted_lines = []

    for line in lines:
        formatted_line = line
        if len(line) > 3:
            '''Format to remove '\n' '''
            formatted_line = line[:-1]
        formatted_lines.append(formatted_line)

    return formatted_lines


##### JSON EXTRACTION, FORMATTING, AND METHODS ######


class Google_post:
    def __init__(self, json_response: dict):
        '''Extacts JSON, and returns a list of dictionaries
        for the meaningful data from Google+ activity'''

        self.account = Account(json_response['items'][0]['actor']['id'],
                json_response['items'][0]['actor']['displayName'], url = json_response['items'][0]['actor']['url'],
                avatar_url = json_response['items'][0]['actor']['image']['url'])


        self.posts = json_response['items']


    def get(self):
        '''list of json'''
        return self.posts

    def check_empty(self, content):
        '''Cuz discord hates empty shit for some
        reason'''
        if content == None or len(content) == 0:
            return '#EMPTY, NO CONTENT# -BOT'

        elif len(content) > 300:
            return content[:300] + '... Content was long, so I put it in Hastebin <3 ' + Hastebin(content)

        else:
            formatted_content = content.replace('<br />', ' ')
            return formatted_content

    def format_posts(self, post):
        '''Formats post that are going to be
        messaged to channel '''
        formatted = []
        try:

            self.account.url = post['url']
            #formatted.append('Look, a Google+ Post!')

            formatted.append("[{}]({})".format(('Posted (UTC): ' + self.check_empty(post['published'])), post['url']))

            if post['object']['objectType'] == 'note':
                '''If activity is a post'''
                formatted.append(('Content', self.check_empty(post['object']['content'])))





            return formatted

        except:
            print('ERROR with Formatting!')
            print(post)
            traceback.print_exc()



    def new_post(self, post):
        '''Checks if bot has messaged this post already, then returns formatted lines
        to be posted'''
        file = read_file('logs.txt')
        if post['url'] not in file:
            dp(post['url'])
            return self.format_posts(post)
        else:
            dp('AHHH')
            return []


    def record_post(self, post):
        '''Records new post to log, to be used AFTER messaging on Discord'''
        file = read_file('logs.txt')
        if post['url'] not in file:
            dp('writing')
            recording_post(post['url'], 'logs.txt')
        else:
            dp('nope')


    def get_latest_post(self):
        return self.format_posts(self.posts[0])




class Youtube_post:
    def __init__(self, json_response: dict):
        '''Extacts JSON, and returns a list of dictionaries
        for the meaningful data from Youtube activity'''
        self.base_video_url = 'https://www.youtube.com/watch?v='

        self.account = Account(json_response['items'][0]['snippet']["channelId"],
                        json_response['items'][0]['snippet']['channelTitle'])


        self.posts = json_response['items']


    def get(self):
        return self.posts


    def check_empty(self, content):
        '''Cuz discord hates empty shit for some
        reason'''
        if content == None or len(content) == 0:
            return '#EMPTY, NO CONTENT# -BOT'

        elif len(content) > 300:
            return content[:300] + '... Content was long, so I put it in Hastebin <3 ' + Hastebin(content)

        else:
            formatted_content = content.replace('<br />', ' ')
            return formatted_content


    def format_posts(self, post):
        formatted = []
        info = post['snippet']
        url = self.base_video_url + post['contentDetails']['upload']['videoId']

        self.account.url = url
        try:
            self.account.thumbnail = info['thumbnails']['maxres']['url']
        except KeyError:
            try:
                self.account.thumbnail = info['thumbnails']['high']['url']
            except KeyError:
                try:
                    self.account.thumbnail = info['thumbnails']['default']['url']
                except KeyError:
                    pass
        finally:
            try:
                self.account.avatar_url = info['thumbnails']['default']['url']
            except:
                pass


        #formatted.append('Look A YouTube Post!')

        formatted.append("[{}]({})".format(('Posted (UTC): ' + self.check_empty(info['publishedAt'])), url))
        formatted.append((self.check_empty(info['title']), self.check_empty(info['description'])))


        return formatted


    def new_post(self, post):
        '''Checks if bot has messaged this post already, then returns formatted lines
        to be posted'''
        file = read_file('logs.txt')
        url = self.base_video_url + post['contentDetails']['upload']['videoId']
        if url not in file:
            dp(url)
            return self.format_posts(post)
        else:
            dp('AHHH')
            return []


    def record_post(self, post):
        file = read_file('logs.txt')
        url = self.base_video_url + post['contentDetails']['upload']['videoId']
        if url not in file:
            dp('writing')
            recording_post([url], 'logs.txt')
        else:
            dp('already written')



    def get_latest_post(self):
        return self.format_posts(self.posts[0])



class Form_update:
    def __init__(self, json_response: dict):
        '''Extacts JSON, and returns a list of dictionaries
        for the meaningful data from Youtube activity'''
        self.sheet = json_response['values']

        self.headers = self.sheet[0]




    def get(self):
        return self.sheet


    def check_empty(self, content):
        '''Cuz discord hates empty shit for some
        reason'''
        if content == None or len(content) == 0:
            return '#EMPTY, NO CONTENT# -BOT'

        else:
            formatted_content = content.replace('<br />', ' ')
            return formatted_content


    def format_posts(self, row):
        formatted = []

        formatted.append('-------------')
        #formatted.append('Look A YouTube Post!')
        index = 0

        for column in row:

            try:
                formatted.append(self.headers[index] + ': ' + self.check_empty(column))

            except:
                formatted.append(self.headers[index] + ' NO DATA')

            index += 1


        formatted.append('-------------')

        return formatted


    def new_post(self, row):
        '''use timestamp'''
        file = read_file('logs.txt')
        try:
            if ('Timestamp ' + row[0]) not in file and len(row[0] > 0) and len(row) > 2:

                return self.format_posts(row)
            else:
                dp('AHHH')
                return []
        except:
            return []

    def record_post(self, row):
        file = read_file('logs.txt')
        try:
            if row[0] not in file:
                dp('writing')
                recording_post(self.format_posts(row), 'logs.txt')
            else:
                dp('already written')
        except:
            pass



    def get_latest_post(self):
        valid_rows = []
        for row in self.sheet:
            if len(row) > 1:
                valid_rows.append(row)
        return self.format_posts(valid_rows[-1])








class Discord_post:
    def __init__(self, posts: list, channel_name):
        '''To be called on each channel'''
        self.posts = posts

        self.media = []
        self.notes = []
        self.channel_name = channel_name

        for post in self.posts:
            if post.startswith('http'):
                self.media.append(post)

            else:
                self.notes.append(post)


    def get(self):
        return self.posts


    def check_empty(self, content):
        '''Cuz discord hates empty shit for some
        reason'''
        if content == None or len(content) == 0:
            return '#EMPTY, NO CONTENT# -BOT'

        else:
            formatted_content = content.replace('<br />', ' ')
            return formatted_content


    def format_posts(self):
        formatted = []

        formatted.append('--------' + self.channel_name + '--------')
        #formatted.append('Look A YouTube Post!')

        formatted.append('-- Decodes/comments/theories --')

        for post in self.notes:
            formatted.append(post)

        formatted.append('-- Media (Audio/Photos/Links/Videos) --')

        for post in self.media:
            formatted.append(self.check_empty(post))


        formatted.append('----------------')
        formatted.append('-')
        formatted.append('•')
        formatted.append('-')

        return formatted



    def record_post(self, post):
        recording_post(self.format_posts(), 'discord_log.txt')




    def get_latest_post(self):
        valid_rows = []
        for row in self.row:
            if len(row) > 1:
                valid_rows.append(row)
        return self.format_posts(valid_rows[-1])







class Stream_post:
    def __init__(self, json_response: dict):
        '''Extacts JSON, and returns a list of dictionaries
        for the meaningful data from Youtube activity'''
        self.posts = []
        base_video_url = 'https://www.youtube.com/watch?v='

        self.streaming = False

        dp(json_response['items'])

        self.account = Account('null', 'null')

        if len(json_response['items']) > 0:
            self.streaming = True


        if self.streaming:
            for item in json_response['items']:
                dp('looking at json')

                post = dict()
                object = item['snippet']


                post.update({'username': object['channelTitle']})

                post.update({'time': object['publishedAt']})


                post.update({'title': object['title']})

                post.update({'description': object['description']})

                post.update({'url': base_video_url + item['id']['videoId']})

                self.posts.append(post)


    def get(self):
        return self.posts


    def check_empty(self, content):
        '''Cuz discord hates empty shit for some
        reason'''
        if content == None or len(content) == 0:
            return '#EMPTY, NO CONTENT# -BOT'

        elif len(content) > 300:
            return content[:300] + '... Content was long, so I put it in Hastebin <3 ' + Hastebin(content)


        else:
            formatted_content = content.replace('<br />', ' ')
            return formatted_content


    def format_posts(self, post):
        formatted = []

        formatted.append('-------------')
        #formatted.append('Look A YouTube Post!')

        formatted.append('Time (Using Coordinated Universal Time): ' + self.check_empty(post['time']))
        formatted.append('Username: ' + self.check_empty(post['username']))
        formatted.append('Title: ' + self.check_empty(post['title']))
        formatted.append('Description: ' + self.check_empty(post['description']))
        formatted.append(post['url'])
        formatted.append('•')
        formatted.append('NOTE: Bot may repost if this stream is uploaded :P')

        formatted.append('-------------')

        return formatted


    def new_post(self, post):
        '''Checks if bot has messaged this post already, then returns formatted lines
        to be posted'''
        file = read_file('logs.txt')
        try:
            if post['url'] not in file:
                dp('new post!')
                dp(post['url'])
                #dp(file[2])
                return self.format_posts(post)
            else:
                dp('AHHH')
                return []
        except AttributeError:
            dp('terrible things')
            return []


    def record_post(self, post):
        file = read_file('logs.txt')
        if post['url'] not in file:
            dp('writing')
            recording_post(self.format_posts(post), 'logs.txt')
        else:
            dp('already written')



    def get_latest_post(self):
        return self.format_posts(self.posts[0])




class Twitter_updates:
    def __init__(self, statuses: dict):
        self.posts = statuses

        name = "{} (@{})".format(statuses[0]['user']["name"], statuses[0]['user']["screen_name"])


        self.account = Account(statuses[0]['user']["screen_name"], name,
                    avatar_url = statuses[0]['user']["profile_image_url"])


    def get(self):
        return self.posts


    def check_empty(self, content):
        '''Cuz discord hates empty shit for some
        reason'''
        if content == None or len(content) == 0:
            return 'Click the Username for content'

        elif len(content) > 300:
            return content[:300] + '... Content was long, so I put it in Hastebin <3 ' + Hastebin(content)


        else:
            formatted_content = content.replace('<br />', ' ')
            return formatted_content


    def format_posts(self, post):
        formatted = []
        url = 'https://twitter.com/statuses/' + post['id_str']
        self.account.url = url
        self.account.platform = post['source'].split('>')[1].replace('</a','')
        self.account.post_id = post['id_str']



        formatted.append('[{}]({})'.format(('Posted (UTC): ' + str(post["created_at"])), url))

        if post["in_reply_to_status_id_str"] != None:
            formatted.append('[{}]({})'.format('Replying to', 'https://twitter.com/statuses/' + post["in_reply_to_status_id_str"]))

        formatted.append(('Content', self.check_empty(post['text'])))

        try:
            if len(post['entities']['media']) > 0:
                media_url = self.check_empty(post['entities']['media'][0]["media_url_https"])
                if ('.jpg' in media_url) or ('.png' in media_url) or ('.gif' in media_url):
                    self.account.thumbnail = media_url
                else:
                    formatted.append(('Media', media_url))
        except KeyError:
            pass



        return formatted


    def new_post(self, post):
        '''Checks if bot has messaged this post already, then returns formatted lines
        to be posted'''
        file = read_file('logs.txt')
        if ('https://twitter.com/statuses/' + post['id_str']) not in file:
            #dp(post['url'])
            dp(file[2])
            return self.format_posts(post)
        else:
            dp('AHHH')
            return []


    def record_post(self, post):
        file = read_file('logs.txt')
        url = 'https://twitter.com/statuses/' + post['id_str']
        if url not in file:
            dp('writing')
            recording_post(url, 'logs.txt')
            recording_post(self.account.name, 'logs.txt')
        else:
            dp('already written')



#### newer classes ######
'''
For the sake of being a little cleaner,
I am now building and retrieving the JSON
request within __init__.... Idk why I
was not doing this before
'''


class Specific_search:
    def __init__(self, s_id, query):
        url = google_api_interact.build_specific_search_url(s_id, query)

        self.json = google_api_interact.get_json(url)

        self.query = query

        self.total = self.json["searchInformation"]["totalResults"]

        self.results = []


        try:
            self.corrected = ' Did you mean: ' + self.json['spelling']["correctedQuery"]
        except:
            self.corrected = ''





        if self.total != '0':
            self.results = self.json['items']


    def format_results(self):
        formatted = []
        for result in self.results:
            info = [result['snippet']]
            info.append(result['link'])
            formatted.append((result['title'], info))

        return formatted


class Contextual_search:
    def __init__(self, query: str):
        url = google_api_interact.build_contextual_search_url(query)
        self.json = google_api_interact.get_json(url)
        self.total = self.json['totalCount']
        self.corrected = ''

        if len(self.json['didUMean']) > 1:
            self.corrected = ' Did you mean: ' + self.json['didUMean']

        self.related = 'Related terms: '

        for item in self.json["relatedSearch"]:
            self.related += item + ', '

        self.results = self.json['value']
        self.results = self.results[:-1]

    def clean_string(self, s: str):
        s = s.replace('<b>', '').replace('<\/b>', '').replace('</b>', '')
        if len(s) > 140:
            s = s[:140] + '...'

        return s


    def format_results(self):
        formatted = []

        for result in self.results:
            if result['isSafe']:
                info = [self.clean_string(result['description'])]
                # info.append('Published: ' + result["datePublished"]) # <-- not very helpful
                info.append(result['url'])
                formatted.append((self.clean_string(result['title']), info))
        if len(formatted) > 0: # for safe search, too lazy to explain
            result = [self.clean_string(self.related)]
            result.extend(formatted)
        else:
            result = ['Nothing to see here dude. Sorrs.']

        return result







class Tumblr_updates:
    def __init__(self, userid: str):
        url = google_api_interact.build_tumblr_url(userid + '.tumblr.com')
        dp(url)
        self.json = google_api_interact.get_json(url)
        self.account = Account(userid, self.json['response']['blog']['name'], url = self.json['response']['blog']['url'],
                        description = self.json['response']['blog']['description'])

        self.posts = self.json['response']['posts']




    def get(self):
        return self.posts


    def check_empty(self, content):
        '''Cuz discord hates empty shit for some
        reason'''
        if content == None or len(content) == 0:
            return '#EMPTY, NO CONTENT# -BOT'

        elif len(content) > 300:
            return content[:300] + '... Content was long, so I put it in Hastebin <3 ' + Hastebin(content)


        else:
            formatted_content = content.replace('<br />', ' ')
            return formatted_content

    def account_info(self, post):
        info = {'name': post['blog_name'], 'pfp': None}
        return info


    def format_posts(self, post):
        formatted = []

        self.account.url = post["short_url"]

        #formatted.append('Look A YouTube Post!')

        formatted.append("[{}]({})".format('Posted (UTC): ' + post["date"], post["short_url"]))
        if len(post['summary']) > 0:
            formatted.append(('Summary', self.check_empty(post['summary'])))
        try:
            self.account.thumbnail = post['photos'][0]['original_size']['url']
        except:
            pass




        return formatted


    def new_post(self, post):
        '''Checks if bot has messaged this post already, then returns formatted lines
        to be posted'''
        file = read_file('logs.txt')
        if post["short_url"] not in file:
            #dp(post['url'])
            return self.format_posts(post)
        else:
            dp('AHHH')
            return []


    def record_post(self, post):
        file = read_file('logs.txt')
        if post["short_url"] not in file:
            dp('writing')
            recording_post(post["short_url"], 'logs.txt')
        else:
            dp('already written')







class Account:
    def __init__(self, userid, name, url = None, avatar_url = None, created_at = '0000', medium = None, description = None,
                platform = '', thumbnail = None, post_id = None):
        self.id = userid
        self.name = name
        self.url = url
        self.avatar_url = avatar_url
        self.created_at = created_at
        self.medium = medium
        self.description = description
        self.platform = platform
        self.thumbnail = thumbnail
        self.post_id = post_id

    def __str__(self):
        return self.name








def Hastebin(content):
    try:
        post = requests.post("https://hastebin.com/documents", data=content.encode('utf-8'))
        print(post)
        return "https://hastebin.com/" + post.json()["key"]
    except:
        return google_api_interact.pastee(content)
        




####### FINAL FUNCTIONS COMPILED FOR EACH PROFILE, outdated #########



def get_proxy_google_plus():
    '''Returns class object'''
    return Google_post(get_google_plus_json(Stopswitch_Proxy_g_plus))


def get_bluff_youtube():
    '''Returns class object'''
    return Youtube_post(get_youtube_json(County_Bluff_youtube))


def get_proxy_youtube():
    '''Returns class object'''
    return Youtube_post(get_youtube_json(Stopswitch_Proxy_youtube))



    #return Form_update(google_api_interact.get_json(ugh))

#print(Tumblr_updates('paradoxpoppi').json)
# print(Specific_search('122', 'yo').json)


#pastee('test')
#### tests ###

#
# print(obj.total)
# print(obj.format_results())




'''




'''
