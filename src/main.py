# -*- coding: utf-8 -*-

from connect_twitter import Twitter
from tqdm import tqdm
from time import sleep
from setting.mykeys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import networkx as nx


if __name__ == "__main__":
    twitter = Twitter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    tweet_scn_list = twitter.get_tweet_users(word='#参院選2019 -RT', count=30, 
                                            result_type='popular', target='screen_name')
    data_dict = {}
    if tweet_scn_list is not None:
        for scn in tqdm(tweet_scn_list):
            following_list = twitter.get_following_scn(scn=scn, count=200)
            if following_list is not None:
                data_dict[id] = following_list
                sleep(60) # because Twitter API block 15req / 15m  
            else: 
                break

    # dict change to graph and save graph
    if data_dict != {}:
        graph = nx.from_dict_of_lists(data_dict)
        nx.write_gml(graph, 'data/twitter.gml')
