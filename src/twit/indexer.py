import json
import time

import pyelasticsearch as es

from twit.fanout import Subscriber


class Indexer(object):
    def __init__(self, name, client=None, settings=None):
        self.name = name
        self.settings = settings
        self.client = client or es.ElasticSearch(
            urls=["http://localhost:49167"])
        self.sub = Subscriber()

    def setup(self):
        try:
            self.client.create_index(self.name, self.settings)
        except es.IndexAlreadyExistsError as err:
            pass
        self.client.put_mapping(
            "twit",
            "tweet",
            {
                "tweet":
                {
                    "properties":
                    {
                        "location": {"type": "geo_point"},
                        "text": {"type": "string",
                                 "store": "yes"}
                    },
                    "_ttl":
                    {
                        "enabled": True,
                        "default": "1h"
                    },
                    "_id": {"path": "id"},
                }
            })
        return self

    def index(self, tweet):
        print tweet
        self.client.index(self.name, "tweet", tweet)

    def loop(self):
        while True:
            tweet = json.loads(self.sub.recv())
            self.index(tweet)

if __name__ == "__main__":
    indexer = Indexer("twit").setup()
    indexer.loop()
