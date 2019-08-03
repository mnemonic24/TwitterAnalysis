# -*- coding: utf-8 -*-

from collections import defaultdict
from connect_twitter import Twitter
from network_analysis import NetworkAnalysis
from tqdm import tqdm
from time import sleep
from setting.mykeys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import networkx as nx
import matplotlib.pyplot as plot
import pandas as pd


if __name__ == "__main__":
    twitter = Twitter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # users_list = twitter.get_tweet_users(word='#政治家に聞きたいギリギリな質問', count=10)
    user_list = []
    master_dict = {}
    node_attrs = defaultdict(dict)

    tweet_user_list = twitter.get_tweet_users(word='平和の少女像 -RT', count=100, result_type='mixed')

    for user in tqdm(tweet_user_list):
        user_id = user['id']
        node_attrs[user_id]['screenName'] = user['screen_name']
        node_attrs[user_id]['followersCount'] = user['followers_count']
        node_attrs[user_id]['friendsCount'] = user['friends_count']
        user_list.append(user_id)

        follower_dict = twitter.get_friends_info(id=user_id, count=200)
        if follower_dict == {}:
            continue
        follower_list = []
        for follower in follower_dict:
            follower_id = follower['id']
            node_attrs[follower_id]['screenName'] = follower['screen_name']
            node_attrs[follower_id]['followersCount'] = follower['followers_count']
            node_attrs[follower_id]['friendsCount'] = follower['friends_count']
            follower_list.append(follower_id)
        master_dict[user_id] = follower_list
        sleep(60)        

    if master_dict != {}:
        G = nx.from_dict_of_lists(master_dict)
        nx.set_node_attributes(G, node_attrs)
        nx.write_gml(G, 'graph/tachibanat.gml')
        
