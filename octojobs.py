#!/usr/bin/python

import tweepy
import sys
from textwrap import TextWrapper
from datetime import datetime
from elasticsearch import Elasticsearch
import json

from configuration import *


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.author.screen_name in IGNORE_LIST:
            pass
        else:
            print (status.text)
            self.follow(status.author.screen_name)
#           self.retweet(status.id_str)
            self.favorite(status.id_str)
            self.push_in_es(status)

    def push_in_es(self, tweet):
        try:
            es.create(
                    index="linux-jobs-tweets", 
                    doc_type="tweet", 
                    body={ 
                        "author": tweet.author.screen_name,
                        "date": tweet.created_at,
                        "message": tweet.text
                        } 
                    )
        except Exception, e:                                                                                                                                                                                                              
            print('No connection to ElasticSearch DB')
            pass


    def follow(self, user):
        try:
            tweepyapi.create_friendship(user)
        except Exception, e:
            pass

    def retweet(self, id_str):
        tweepyapi.retweet(id_str)
        
    def favorite(self, id_str):
        tweepyapi.create_favorite(id_str)

    def on_error(self, status):
        print status



if __name__ == '__main__':
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        tweepyapi = tweepy.API(auth)

        es = Elasticsearch()

        # There are different kinds of streams: public stream, user stream, multi-user streams
        # For more details refer to  https://dev.twitter.com/docs/streaming-apis
        
        streamer = tweepy.Stream(auth=auth, listener=StreamListener(), timeout=3000000000 )
        # Fill with your own Keywords bellow
        terms = ['linux jobs','linux job', 'linux hiring']

        streamer.filter(None,terms)


#        print('Let\s crawl Twitter for %s' % terms)

