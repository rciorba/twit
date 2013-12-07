import sys

import tweepy

import twit.config
from twit.indexer import Indexer


cfg = twit.config.get_config()


consumer_key = cfg["consumer_key"]
consumer_secret = cfg["consumer_secret"]
access_key = cfg["access_key"]
access_secret = cfg["access_secret"]


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

index = Indexer("twit").setup()


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # print status.text, status.coordinates, status.place.name
        index.index(status)

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())

sapi.filter(locations=[-11.206, 49.821, 2.900, 61.186]) # southwest corner first
