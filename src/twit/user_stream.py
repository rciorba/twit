import json

from twit.fanout import Subscriber


class UserStream(object):
    def __init__(self, lon, lat, distance):
        self.sub = Subscriber()
        self._lon = lon
        self._lat = lat
        self._sq_dist = distance**2

    def loop(self):
        _lat, _lon = self._lat, self._lon
        _sq_dist = self._sq_dist
        while True:
            tweet = json.loads(self.sub.recv())
            lat = tweet["location"]["lat"]
            lon = tweet["location"]["lon"]
            sq_dist = (lat-_lat)**2 + (lon-_lon)**2
            if sq_dist < _sq_dist:
                print tweet


if __name__ == "__main__":
    UserStream(-2.27828292, 53.46188953, 1).loop()
