# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session
import time
import json
import sys


class Twitter:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.api = OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)

    def get_tweet_users(self, word, count, url = "https://api.twitter.com/1.1/search/tweets.json"):
        params ={'q': word, 'count': count}
        req = self.api.get(url, params=params)
        id_list = []
        if req.status_code == 200:
            search_timeline = json.loads(req.text)
            for tweet in search_timeline['statuses']:
                id_list.append(tweet['user']['id'])
            id_list = list(set(id_list))
            return id_list
        else:
            print("ERROR: %d" % req.status_code)
            sys.exit()

    def get_followers_id(self, scn, count=5, url='https://api.twitter.com/1.1/followers/list.json'):
        params = {'ids': id, 'cursor': -1, 'count': count}
        req = self.api.get(url, params=params)
        if req.status_code == 200:
            followers_list = req.json()['ids']
            return followers_list
        else: 
            print("ERROR: %d" % req.status_code)
            sys.exit()

    def get_following_id(self, id, count=5, url='https://api.twitter.com/1.1/friends/ids.json'):
        params = {'ids': id, 'cursor': -1, 'count': count}
        req = self.api.get(url, params=params)
        if req.status_code == 200:
            following_list = req.json()['ids']
            return following_list
        else: 
            print("ERROR: %d" % req.status_code)
            return []


if __name__ == "__main__":
    pass
