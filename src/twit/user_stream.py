import json
import marshal

from twit.fanout import Subscriber, Publisher, context


ctx = context()


def broadcast_tweets():
    """get tweets from zmq and send them to all user_streams
    """
    sub = Subscriber(context=ctx)
    pub = Publisher(url="inproc://twit", context=ctx)
    while True:
        pub.send(marshal.dumps(json.loads(sub.recv())))


def user_stream(lon, lat, dist):
    sub = Subscriber(url="inproc://twit", context=ctx)
    sq_dist = dist**2
    print lat, lon, dist
    while True:
        tweet = marshal.loads(sub.recv())
        _lat = tweet["location"]["lat"]
        _lon = tweet["location"]["lon"]
        _sq_dist = (lat-_lat)**2 + (lon-_lon)**2
        if _sq_dist < sq_dist:
            print tweet


if __name__ == "__main__":
    import gevent

    def _stress(number):
        from random import random as rand
        streams = [
            gevent.spawn(user_stream, -11+rand()*13, 49.5+rand()*12, 1)
            for _ in xrange(number)
        ]
    # UserStream(-2.27828292, 53.46188953, 1).loop()
    _stress(1000)  # check your open fd limit
    _stress(1000)
    broadcast_tweets()
    while 1:
        gevent.sleep(60)
