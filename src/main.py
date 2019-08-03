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
    from_follower_dict = {}
    follower_list = []
    node_attrs = defaultdict(dict)

    center_dict = twitter.get_users_info(scn='tachibanat')
    center_id = center_dict['id']

    node_attrs[center_id]['screenName'] = center_dict['screen_name']
    node_attrs[center_id]['followersCount'] = center_dict['followers_count']
    node_attrs[center_id]['friendsCount'] = center_dict['friends_count']
    follower_dict = twitter.get_followers_info(id=center_id, count=200)
    for follower in tqdm(follower_dict):
        follower_id = follower['id']
        node_attrs[follower_id]['screenName'] = follower['screen_name']
        node_attrs[follower_id]['followersCount'] = follower['followers_count']
        node_attrs[follower_id]['friendsCount'] = follower['friends_count']
        follower_list.append(follower_id)

        follower_dict2 = twitter.get_followers_info(id=follower_id, count=200)
        if follower_dict2 == {}:
            continue
        follower_list2 = []
        for follower2 in follower_dict2:
            follower_id2 = follower2['id']
            node_attrs[follower_id2]['screenName'] = follower2['screen_name']
            node_attrs[follower_id2]['followersCount'] = follower2['followers_count']
            node_attrs[follower_id2]['friendsCount'] = follower2['friends_count']
            follower_list2.append(follower_id2)
        sleep(60)
        
        from_follower_dict[follower_id] = follower_list2
    from_follower_dict[center_id] = follower_list    

    # sleep(60) # because Twitter API block 15req / 15m  
    # to_follow_dict[id] = friend_list


    # df_to_follow = pd.DataFrame(to_follow_dict)
    # df_to_follow.T.to_csv('data/to_follow.csv', header=False, index=True)
    # df_node_attrs = pd.DataFrame(node_attrs)
    # df_node_attrs.T.to_csv('data/node_attrs.csv', header=True, index=True)

    if from_follower_dict != {}:
        G = nx.from_dict_of_lists(from_follower_dict)
        nx.set_node_attributes(G, node_attrs)
        nx.write_gml(G, 'graph/tachibanat.gml')
        
