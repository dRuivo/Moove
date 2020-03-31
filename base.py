import socketio
from threading import Thread
import time

sio = socketio.Client()
class TimeKeeper:
    last_time = 0.
    def __init__(self):
        pass

tk = TimeKeeper()
tk.last_time = time.time()

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

running = True
def timing():
    print('thread start')
    last_time = time.time()
    while running:
        if (time.time() - last_time) >= 1.:
            sio.emit('this_time', {'time' : time.time()})
            print('times', time.time() - last_time)
            last_time = time.time()
        time.sleep(0)
    print('thread stop')

t = Thread(target=timing)
t.start()

sio.connect('http://localhost:5000')
sio.wait()
