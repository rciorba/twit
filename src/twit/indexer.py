import pyelasticsearch as es
import time


class Indexer(object):
    def __init__(self, name, client=None, settings=None):
        self.name = name
        self.settings = settings
        self.client = client or es.ElasticSearch(
            urls=["http://localhost:49167"])

    def setup(self):
        if self.client is None:
            self.client = es.ElasticSearch(self.urls)
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
                        "location": {"type":"geo_point"},
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
        if tweet.geo is None:
            # ignore tweets that don't provide latitude/longitude
            return
        assert tweet.geo["type"] == "Point", "expected Point not %r" % tweet.geo
        lat, lon = tweet.geo["coordinates"]
        doc = {
            "text": tweet.text,
            "location": {"lat": lat, "lon": lon},
            "id": tweet.id,
            "user": {"id": tweet.user.id, "name": tweet.user.name},
        }
        # "geo": {"long":}
        t = time.time
        b = t()
        print doc
        self.client.index(self.name, "tweet", doc)
        print t() - b

if __name__ == "__main__":
    indexer = Indexer("twit").setup()
    print indexer.client.get_mapping("twit", "tweet")
