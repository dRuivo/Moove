import eventlet
eventlet.monkey_patch()
import socketio
from threading import Thread
import time
import logging
from topics import ServerTopic

class DataHandler:
    def __init__(self):
        self.topics = {}
        self.node_list = []

    def add_node(self, sid, node_name):
        self.node_list.append((node_name, sid))

    def add_to_topic(self, name, publisher=None, subscriber=None):
        pass


class Base(socketio.Namespace):
    def __init__(self, parent=None):
        super(Base, self).__init__(namespace=None)
        self.parent = parent

    def on_connect(self, sid, environ):
        print('connect ', sid)

    def on_identify(self, sid, data):
        print('connected to ', data)
        self.parent.add_node(sid, data)
        #TODO keep track of who's connected

    def on_disconnect(self, sid):
        print('disconnect ', sid)

    def on_register(self, data):
        pass
    

class Core:
    def __init__(self):
        self.sio = socketio.Server()
        self.app = socketio.WSGIApp(self.sio)

        self.data = DataHandler()

        self.sio.register_namespace(Base())

    def run(self, port=5000):
        eventlet.wsgi.server(eventlet.listen(('', port)), self.app)

if __name__ == '__main__':
    core = Core()
    core.run()
    
    