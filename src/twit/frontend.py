import os.path

import gevent
import gevent.pywsgi
import paste.cascade
import paste.urlparser

import twit
import twit.search as search


def main():
    static_app = paste.urlparser.StaticURLParser(
        os.path.join(twit.__path__[0], "static"))
    apps = paste.cascade.Cascade([static_app, search.app])
    http_server = gevent.pywsgi.WSGIServer(
        ('', 8000), apps)
    http_server.start()
    while True:
        gevent.sleep(1)


if __name__ == "__main__":
    main()
