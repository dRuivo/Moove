import eventlet
eventlet.monkey_patch()
import socketio
from threading import Thread
import time
import logging

if __name__ == "__main__":
    from topics import ServerTopic
    from core_data import DataHandler
else:
    from features.topics import ServerTopic
    from features.core_data import DataHandler

class Base(socketio.Namespace):
    def __init__(self, parent=None):
        super(Base, self).__init__(namespace=None)
        self.parent = parent

    def on_connect(self, sid, environ):
        # print('connect ', sid)
        pass

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

        self.data = DataHandler(parent=self)
        self.add_node = self.data.add_node
        
        self.sio.register_namespace(self.data)
        self.sio.register_namespace(Base(parent=self))


    def run(self, port=5000):
        eventlet.wsgi.server(eventlet.listen(('', port)), self.app, debug=True)    
    