#/usr/bin/env python3

import tweepy
import requests
import time
import json
import numpy
import matplotlib.pyplot as plt

ckey = 'aqJrn3ZT3uIxKYiJh4Lc5lDaT'
csecret = 'akxhmBeXUh7jZnMCcjJ3WcyEI68EJRFs9xdruQ36Gfua7eXgij'
atoken = '1086639759106154496-3ZSyU6dKz7ILsKiijSUI51evE0xlW4'
asecret = 'o2KvTRZnPuvG1GcD1vtTGn2GEvryL3LXa2h0KezALZYcV'


def main():
    user_id = "acnwala"

    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    api = tweepy.API(auth)

    user_list = api.followers_ids(user_id)
    follower_counts = []

    for each in user_list:

        temp_follower_object = api.get_user(each)
        temp_follower_count = temp_follower_object.followers_count
        follower_counts.append(temp_follower_count)

    follower_counts = sorted(follower_counts)
    curr_mean, curr_median, curr_std = calc_stats(follower_counts)
    gen_graph(follower_counts, len(follower_counts) ,curr_mean, curr_median, curr_std)

def gen_graph(curr_data_list, nwala_follower_count, mean, median, std):

    temp_x_values = [x for x in range(len(curr_data_list))]

    ax = plt.plot(temp_x_values, curr_data_list)

    place_nwala = False
    place_mean = False
    place_median = False
    place_std = False

    for i in range(len(curr_data_list)):

        if curr_data_list[i] >= nwala_follower_count and place_nwala == False:
            plt.plot(i, nwala_follower_count, marker='x',markersize=6, color='red')
            plt.annotate(f'Alexander Nwala: {nwala_follower_count}',(i, nwala_follower_count+ 2000))
            place_nwala = True
        elif curr_data_list[i] >= mean and place_mean == False:
            plt.plot(i, mean, marker='x',markersize=6, color='red')
            plt.annotate(f'Mean: {mean}',(i,mean+50))
            place_mean = True
        elif curr_data_list[i] >= median and place_median == False:
            plt.plot(i, median, marker='x',markersize=6, color='red')
            plt.annotate(f'Median: {median}',(i,median-150))
            place_median = True
        elif curr_data_list[i] >= std and place_std == False:
            plt.plot(i, std, marker='x',markersize=6, color='red')
            plt.annotate(f'Std: {std}',(i,std-1250))
            place_std = True

    plt.title('Chart 2: Friend vs FriendCount(Twitter)')
    plt.xlabel('Followers')
    plt.ylabel('No. of Followers')
    plt.savefig('friend_paradox_Twitter.png')

def calc_stats(data_list):
    data_mean = round(numpy.mean(data_list), 3)
    data_std = round(numpy.std(data_list),3)
    data_median = round(numpy.median(data_list),3)
    print('curr_mean: ', data_mean)
    print('curr_std: ', data_std)
    print('curr_median: ', data_median)
    # returns mean, standard deviation and median in that order
    return data_mean, data_std, data_median

main()
