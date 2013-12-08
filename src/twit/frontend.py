import os.path

import gevent
import gevent.pywsgi
from geventwebsocket.handler import WebSocketHandler
import paste.cascade
import paste.urlparser

import twit
import twit.search as search
import twit.user_stream as user_stream


def main():
    static_app = paste.urlparser.StaticURLParser(
        os.path.join(twit.__path__[0], "static"))
    apps = paste.cascade.Cascade([static_app, search.app])
    ws_server = gevent.pywsgi.WSGIServer(
        ('', 8001), user_stream.web_socket_handler,
        handler_class=WebSocketHandler)
    ws_server.start()
    http_server = gevent.pywsgi.WSGIServer(
        ('', 8000), apps)
    http_server.start()
    gevent.spawn(user_stream.broadcast_tweets)
    while True:
        gevent.sleep(1)


if __name__ == "__main__":
    main()
