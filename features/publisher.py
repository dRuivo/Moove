import eventlet
eventlet.monkey_patch()
import socketio
from threading import Thread
import time

class Publisher:

    def __init__(self, data_id=''):
        self.sio = socketio.Server()
        self.app = socketio.WSGIApp(self.sio)
        self.data_id = data_id

        self.sio.on('connect', lambda sid, environ: self.connect(sid, environ))
        self.sio.on('disconnect', lambda sid: self.disconnect(sid))

    
    def connect(self, sid, environ):
        print(sid)

    def disconnect(self, sid):
        print('disconnect ', sid)

    def send(self, data):
        self.sio.emit(self.data_id, data)

    def run(self):
        def t_run():
            eventlet.wsgi.server(eventlet.listen(('', 5000)), self.app)
        t = Thread(target=t_run)
        t.start()

    def register_topic(self, topic):
        self.sio.register_namespace(topic)

    def process(self):
        while True:
            self.sio.emit('this_time', {'time' : time.time()})
            time.sleep(1)

if __name__ == "__main__":
    pub = Publisher('this_time')
    pub.run()
    while True:
        pub.send({'time' : time.time()})
        time.sleep(1)
