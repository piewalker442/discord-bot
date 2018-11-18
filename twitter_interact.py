import tweepy
import asyncio
from collections import defaultdict
import json

consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'
access_token = 'access_token'
access_secret = 'access_secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_secret)


#Construct the API instance
api = tweepy.API(auth, wait_on_rate_limit=True) # create an API object


# user = api.get_user('1009695025951674368')
# for friend in user.friends():
#    for status in api.user_timeline(friend.id):
#        status_url = 'https://twitter.com/statuses/' + status.id_str
#        print(status.text)
#        print(status_url)
#        print(status.source)
#        print('replying:', status.in_reply_to_status_id_str)
#        print()


class TestError(Exception):
    pass

class Status_collector:
    def __init__(self, userid = None):
        self.userid = userid
        if self.userid == '':
            self.userid == None
            self.myself = api.get_user('bot_twitter_id')
            self.friends = self.myself.friends()
        else:
            self.user = api.get_user(self.userid)

        self.statuses = [] # list of statuses


    def collect_all_statuses(self):
        for friend in self.friends:
            for status in api.user_timeline(friend.id):
                json_status = (status._json)

                self.statuses.append(json_status)

    def return_id(self):
        return str(self.user.id)


    def collect_user_statuses(self):
        user = self.user
        print(self.userid)
        for status in api.user_timeline(user.id):
            # status_info = {'author': status.author.screen_name, 'time': str(status.created_at),
            #         'content': status.text, 'in_reply_to': self.build_tweet_url(status.in_reply_to_status_id_str),
            #         'source': str(status.source), 'url': self.build_tweet_url(status.id_str)}
            # self.statuses.append(status_info)

            json_status = (status._json)

            self.statuses.append(json_status)



    def build_tweet_url(self, id):
        if id == None:
            return 'None'
        status_url = 'https://twitter.com/statuses/' + id
        return status_url



    def return_statuses(self):
        try:
            if self.userid == None or self.userid == '':
                print('collected all')
                self.collect_all_statuses()
            else:
                print('collected user')
                self.collect_user_statuses()

            print('successful collection of twitter statuses')
            return self.statuses
        except TestError:
            print('failed to return status')



class Search_twitter_user:
    def __init__(self, query: str):
        self.results = api.search_users(query)

    def format_results(self):
        formatted = ['{:20s} | id'.format('handle')]

        for user in self.results:
            result = '{:20s} | {}'.format(user.screen_name, user.id_str)

            formatted.append(result)

        return formatted


    def print_results(self):
        for result in self.format_results():
            print(result)





class Stalk_twitter:
    def __init__(self, userid = None):

        self.userid = userid
        self.user = api.get_user(self.userid)

    def return_user(self):
        return self.user

    def if_none(self, line):
        '''for when info is unavailable'''
        if line == None or line == 'None' or line == '':
            return 'not available'
        else:
            return str(line)

    def format_user_info(self):
        print('formatting')
        formatted = [
        'Name: ' + self.user.name,
        'Handle: ' + self.user.screen_name,
        'User ID: ' + self.user.id_str,
        'Created: ' + str(self.user.created_at),
        'Description: ' + self.user.description,
        'Followers:' + str(self.user.followers_count),
        'Track location?: ' + str(self.user.geo_enabled),
        'Location: ' + self.if_none(self.user.location),
        'Timezone: ' + self.if_none(self.user.time_zone),
        'https://twitter.com/' + self.user.screen_name
        ]

        return formatted

    def print_user_info(self):

        for line in self.format_user_info():
            print(line)



#Search_twitter_user('nate').print_results()


#Stalk_twitter('1009771306181636097').print_user_info()



#print(api.rate_limit_status())


# python3 twitter_interact.py
# for status in api.home_timeline():
#     print(status.text)
