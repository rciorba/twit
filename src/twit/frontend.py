import os.path

import gevent
import gevent.pywsgi
from geventwebsocket.handler import WebSocketHandler
import paste.cascade
import paste.urlparser

import twit
import twit.search as search
import twit.user_stream as user_stream


def ws_server():
    ws_server = gevent.pywsgi.WSGIServer(
        ('', 8001), user_stream.web_socket_handler,
        handler_class=WebSocketHandler)
    ws_server.start()
    gevent.spawn(user_stream.broadcast_tweets)
    print "started ws_server"


def http_server():
    static_app = paste.urlparser.StaticURLParser(
        os.path.join(twit.__path__[0], "static"))
    apps = paste.cascade.Cascade([static_app, search.app])
    http_server = gevent.pywsgi.WSGIServer(
        ('', 8000), apps)
    http_server.start()
    print "started http_server"


if __name__ == "__main__":
    import sys
    print """alternate invocations:
python -m twit.frontend ws  # starts websocket server only
python -m twit.frontend http  # starts search + static server only
"""
    if len(sys.argv) > 1:
        invocation = sys.argv[1]
        if invocation == "ws":
            ws_server()
        elif invocation == "http":
            http_server()
        else:
            print "illegal invocation %r" % invocation
            sys.exit(1)
    else:
        ws_server()
        http_server()
    while True:
        gevent.sleep(1)
