import eventlet
eventlet.monkey_patch()
import socketio
from threading import Thread
import time
import logging

sio = socketio.Server()
app = socketio.WSGIApp(sio)

class TimeKeeper:
    last_time = 0.
    def __init__(self):
        pass
    
tk = TimeKeeper()
tk.last_time = time.time()

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.event
def this_time(sid, data):
    sio.emit('this_time', data)
    print('times ', data['time'] - tk.last_time, (time.time() - data['time']) * 1000)
    tk.last_time = data['time']

running = True
def timing():
    print('thread start')
    last_time = time.time()
    while running:
        if (time.time() - last_time) >= .01:
            print('thread send')
            print(sio.emit('this_time', {'time' : time.time()}))
            last_time = time.time()
        time.sleep()
    print('thread stop')

# t = Thread(target=timing)
# t.start()

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    running = False
    
    