from features.publisher import Publisher
import socketio
import time

class MyCustomNamespace(socketio.Namespace):
    def on_connect(self, sid, environ):
        pass

    def on_disconnect(self, sid):
        pass

    def on_my_event(self, sid, data):
        self.emit('my_response', data)

if __name__ == "__main__":
    pub = Publisher()
    pub.register_topic(MyCustomNamespace('/topic1'))
    pub.run()
    while True:
        pub.sio.emit('this_time', {'time' : time.time()}, namespace='/topic1')
        time.sleep(1)