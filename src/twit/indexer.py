import json

import pyelasticsearch as es

from twit.fanout import Subscriber
from twit import config


cfg = config.get_config()


class Indexer(object):
    BATCH_SIZE = 100
    def __init__(self, name, client=None, settings=None):
        self.name = name
        self.settings = settings
        self.client = client or es.ElasticSearch(
            urls=[cfg.get("ES_URL", "http://localhost:9200")])
        self.sub = Subscriber()
        self._buffer = []

    def setup(self):
        try:
            self.client.create_index(self.name, self.settings)
        except es.IndexAlreadyExistsError as err:
            pass
        self.client.put_mapping(
            "twit",
            "tweet", {
                "tweet": {
                    "properties": {
                        "location": {"type": "geo_point"},
                        "text": {"type": "string"},
                        "timestamp": {"type": "integer"},
                    },
                    "_ttl": {
                        "enabled": True,
                        "default": "15m"
                    },
                    "_id": {"path": "id"},
                }
            })
        return self

    def index(self, tweet):
        self._buffer.append(tweet)
        if len(self._buffer) >= self.BATCH_SIZE:
            self.client.bulk_index(self.name, "tweet", self._buffer)
            self._buffer = []
            print tweet

    def loop(self):
        while True:
            tweet = json.loads(self.sub.recv())
            self.index(tweet)


if __name__ == "__main__":
    settings = {"number_of_shards": 1, "number_of_replicas": 0}
    indexer = Indexer("twit", settings=settings).setup()
    indexer.loop()
