#!/usr/bin/python

import tweepy
import sys
from textwrap import TextWrapper
from datetime import datetime
from elasticsearch import Elasticsearch
import json

from configuration import *

es = Elasticsearch()

class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.author.screen_name in IGNORE_LIST:
            pass
        else:
            print (status.text)
            self.push_in_es(status)
            self.follow(status.author.screen_name)
            self.retweet(status.id_str)

    def push_in_es(self, tweet):
        es.create(index="linux-jobs-tweets", 
                  doc_type="tweet", 
                  body={ "author": tweet.author.screen_name,
                         "date": tweet.created_at,
                         "message": tweet.text}
                  )

    def follow(self, user):
        try:
            tweepyapi.create_friendship(user)
        except Exception, e:
            pass

    def retweet(self, id_str):
        tweepyapi.retweet(id_str)

    def on_error(self, status):
            print status



if __name__ == '__main__':
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        tweepyapi = tweepy.API(auth)

        # There are different kinds of streams: public stream, user stream, multi-user streams
        # In this example follow #programming tag
        # For more details refer to  https://dev.twitter.com/docs/streaming-apis
        
        streamer = tweepy.Stream(auth=auth, listener=StreamListener(), timeout=3000000000 )
        # Fill with your own Keywords bellow
        terms = ['linux jobs','linux job', 'linux hiring']

        streamer.filter(None,terms)




