# -*- coding: utf-8 -*-

from connect_twitter import Twitter
from tqdm import tqdm
from setting.mykeys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import networkx as nx


if __name__ == "__main__":
    twitter = Twitter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    tweet_id_list = twitter.get_tweet_users(word='#参院選2019', count=15)
    data_dict = {}
    if tweet_id_list != []:
        for id in tqdm(tweet_id_list):
            following_list = twitter.get_following_id(id=id, count=5000)
            if following_list != []:
                data_dict[id] = following_list
            else: 
                break

    graph = nx.from_dict_of_lists(data_dict)
    nx.write_gml(graph, 'data/twitter.gml')