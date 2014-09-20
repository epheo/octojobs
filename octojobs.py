import tweepy
import sys
from textwrap import TextWrapper
from textblob import TextBlob
from datetime import datetime
from elasticsearch import Elasticsearch
import json


consumer_key="05WXdIClEQleZESrtYBQw"
consumer_secret="fRShUMDyfgHFdoe4kp3vpqxeGDYg5g6B8vyZiw0OU"

access_token="2205093792-nnx06lR2jZ64WCDIA68XxLuPwhP7HwnsytIRh0L"
access_token_secret="3E2JojFK3QCtEuWFm8FTNlSbUR8DU1JXh37DQ0p7Ic82E"


es = Elasticsearch()

class StreamListener(tweepy.StreamListener):
    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')

    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
    
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print '@%s: %s' % (decoded['user']['screen_name'],
        decoded['text'].encode('ascii', 'ignore'))
        print ''
        return True


    def push_in_es(self, input_tweet):
            tweet = TextBlob(input_tweet)
            print str(tweet)

#            es.create(index="my-index", 
#                      doc_type="test-type", 
#                      body={ "author": status.author.screen_name,
#                             "date": status.created_at,
#                             "message": status.text,
#                             "polarity": tweet.sentiment.polarity,
#                             "subjectivity": tweet.sentiment.subjectivity }
#                     )


    def on_error(self, status):
            print status

#class 

#tweepy.create_friendship(iscreen_n1[, follow])


if __name__ == '__main__':
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        print "Showing all new tweets for #linux #jobs:"

        # There are different kinds of streams: public stream, user stream, multi-user streams
        # In this example follow #programming tag
        # For more details refer to  https://dev.twitter.com/docs/streaming-apis
        
        streamer = tweepy.Stream(auth=auth, listener=StreamListener(), timeout=3000000000 )
        # Fill with your own Keywords bellow
        terms = ['#linux', '#jobs']

        streamer.filter(None,terms)




