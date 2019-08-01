# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session
import json
import sys
import datetime


class Twitter:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.api = OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)

    def get_tweet_users(self, word, target='id', count=5, result_type='recent', 
                        until=str(datetime.date.today()), url="https://api.twitter.com/1.1/search/tweets.json"):
        
        params ={'q': word, 'count': count, 'result_type': result_type, 'until': until}
        user_list = []
        
        req = self.api.get(url, params=params)
        if target not in ['id', 'screen_name']:
            print('Don\'t have {} param, use id or screen_name'.format(target))
            return
        if req.status_code == 200:
            search_timeline = json.loads(req.text)
            for tweet in search_timeline['statuses']:
                user_list.append(tweet['user'][target])
            user_list = list(set(user_list))
            return user_list
        else:
            print("ERROR: %d" % req.status_code)
            return

    # count <= 5000
    def get_followers_id(self, id, count=5, url='https://api.twitter.com/1.1/followers/ids.json'):
        params = {'ids': id, 'cursor': -1, 'count': count}
        req = self.api.get(url, params=params)
        if req.status_code == 200:
            followers_list = req.json()['ids']
            return followers_list
        else: 
            print("ERROR: %d" % req.status_code)
            return None

    # scn = screen name, count <= 200
    def get_followers_scn(self, scn, count=5, url='https://api.twitter.com/1.1/followers/list.json'):
        params = {'screen_name': scn, 'cursor': -1, 'count': count}
        req = self.api.get(url, params=params)
        if req.status_code == 200:
            followers_list = []
            for user in req.json()['users']:
                followers_list.append(user['screen_name'])
            return followers_list
        else: 
            print("ERROR: %d" % req.status_code)
            return None

    # count <= 5000
    def get_following_id(self, id, count=5, url='https://api.twitter.com/1.1/friends/ids.json'):
        params = {'ids': id, 'cursor': -1, 'count': count}
        req = self.api.get(url, params=params)
        if req.status_code == 200:
            following_list = req.json()['ids']
            return following_list
        else: 
            print("ERROR: %d" % req.status_code)
            return None

    # scn = screen name, count <= 200
    def get_following_scn(self, scn, count=5, url='https://api.twitter.com/1.1/friends/list.json'):
        params = {'screen_name': scn, 'cursor': -1, 'count': count}
        req = self.api.get(url, params=params)
        if req.status_code == 200:
            following_list = []
            for user in req.json()['users']:
                following_list.append(user['screen_name'])
            return following_list
        else: 
            print("ERROR: %d" % req.status_code)
            return None
