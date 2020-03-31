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

@sio.on('connect', namespace='/topic1')
def on_connect1():
    print("I'm connected to the /topic1 namespace!")

@sio.on('connect', namespace='/topic2')
def on_connect2():
    print("I'm connected to the /topic2 namespace!")

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.on('this_time', namespace='/topic1')
def this_time1(data):
    print('1times %.3f %.3f' % (data['time'] - tk.last_time, (time.time() - data['time']) * 1000))
    tk.last_time = data['time']
    sio.emit('someting', data='here', namespace='/topic2')

@sio.on('this_time', namespace='/topic2')
def this_time2(data):
    print('2times %.3f %.3f' % (data['time'] - tk.last_time, (time.time() - data['time']) * 1000))
    tk.last_time = data['time']

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:5000', namespaces=['/topic1', '/topic2'])
sio.wait()
