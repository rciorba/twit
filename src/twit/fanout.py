import zmq.green as zmq


def context():
    return zmq.Context()


class Publisher(object):
    def __init__(self, url=None, context=None):
        self.url = url or "tcp://127.0.0.1:5000"
        context = zmq.Context() if context is None else context
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(self.url)

    def send(self, msg):
        self.socket.send(msg)


class Subscriber(object):
    def __init__(self, url=None, context=None):
        self.url = url or "tcp://127.0.0.1:5000"
        context = zmq.Context() if context is None else context
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(self.url)
        self.socket.setsockopt(zmq.SUBSCRIBE, "")

    def recv(self):
        return self.socket.recv()
