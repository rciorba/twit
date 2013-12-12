import json
import sys

import gevent
import tweepy

import twit.config
from twit.fanout import Publisher


cfg = twit.config.get_config()


consumer_key = cfg["consumer_key"]
consumer_secret = cfg["consumer_secret"]
access_key = cfg["access_key"]
access_secret = cfg["access_secret"]


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# index = Indexer("twit").setup()
pub = Publisher()


def tweet_to_dict(tweet):
    doc = {
        "text": tweet.text,
        "id": tweet.id,
        "user": {"id": tweet.user.id, "name": tweet.user.name},
        "timestamp": int(tweet.created_at.strftime("%s")),
    }
    if tweet.geo is None:
        return
    # ignore tweets that don't provide latitude/longitude
    lat, lon = tweet.geo["coordinates"]
    doc["location"] = {"lat": lat, "lon": lon}
    return doc


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # print status.text, status.coordinates, status.place.name
        # index.index(status)
        tweet = tweet_to_dict(status)
        if tweet is not None:
            pub.send(json.dumps(tweet))

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        gevent.sleep(60)
        return True  # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream


sapi = tweepy.streaming.Stream(auth, CustomStreamListener())

# sapi.filter(locations=[-11.206, 49.821, 2.900, 61.186])  # southwest corner first
sapi.filter(locations=[-180,-90,180,90])  # southwest corner first
