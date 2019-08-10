#! /usr/bin/env python3
import os
import pickle
import tweepy

ckey = 'aqJrn3ZT3uIxKYiJh4Lc5lDaT'
csecret = 'akxhmBeXUh7jZnMCcjJ3WcyEI68EJRFs9xdruQ36Gfua7eXgij'
atoken = '1086639759106154496-3ZSyU6dKz7ILsKiijSUI51evE0xlW4'
asecret = 'o2KvTRZnPuvG1GcD1vtTGn2GEvryL3LXa2h0KezALZYcV'

class listener(tweepy.StreamListener):

    def __init__(self):
        self.tweet_list1 = []
        self.tweet_list2 = []
        self.currList = self.tweet_list1
        self.outFile = 'out.txt'
        self.total = 0

    def set_cur_list(self, num):
        if num == 1:
            self.currList = self.tweet_list1
        else:
            self.currList = self.tweet_list2

    def write_output(self, list):
        with open(self.outFile,'ab') as f:
            pickle.dump(list, f)
        #os._exit(0)

    def on_data(self, data):

        if len(self.currList) == 5000:
            self.total += 1
            if self.currList == self.tweet_list1:
                outList = self.tweet_list1
                self.currList = self.tweet_list2
                self.tweet_list2.clear()
            else:
                 outList = self.tweet_list2
                 self.currList = self.tweet_list1
                 self.tweet_list1.clear()

            p = os.fork()
            if p == 0:
                print(str(self.total))
                self.write_output(outList)
                os._exit(0)
            else:
                os.wait()


        else:
            #print(data)
            if self.total == 5:
                return

            self.currList.append(data)

    def on_error(self,status):
        print(status)

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = tweepy.Stream(auth, listener())
twitterStream.filter(track=["Trump","Sports"])
