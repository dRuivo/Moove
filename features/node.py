import socketio
from threading import Thread

if __name__ == "__main__":
    from topics import ServerTopic
else:
    from features.topics import ServerTopic

class Base(socketio.ClientNamespace):
    def __init__(self, parent=None):
        super(Base, self).__init__(namespace=None)
        self.parent = parent

    def on_connect(self):
        if self.parent:
            print(self.parent.name, ' connected')
            self.emit('identify', self.parent.name)

    def on_disconnect(self):
        if self.parent:
            print(self.parent.name, ' disconnected')

    def on_message(self, data):
        self.parent.on_message(data)

class Node:
    """

    """
    def __init__(self, name=''):
        self.name = name
        self.sio = socketio.Client()
        self.sio.register_namespace(Base(self))

    def run(self):
        self.sio.connect('http://localhost:5000')
        t = Thread(target=self.sio.wait)
        t.start()

    def on_message(self, data):
        print('message ', data)


if __name__ == "__main__":
    # for checking
    node1 = Node('1')
    node2 = Node('2')
    node1.run()
    node2.run()
    while True:
        pass