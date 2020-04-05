import socketio

class ServerTopic(socketio.Namespace):
    def __init__(self, namespace=None, publisher=None, subscriber=None):
        super(ServerTopic, self).__init__(namespace=namespace)
        self.publisher = publisher
        self.subscribers = [] # arrey of tuple (sid, id)
        self.definition = ''

    def on_connect(self, sid, environ):
        pass

    def on_disconnect(self, sid):
        self.leave_room(sid, self.namespace)

    def on_publisher(self, sid, data):
        if not self.publisher:
            self.enter_room(sid, self.namespace)
            self.publisher = sid
            if 'definition' in data:
                self.definition = data['definition']
            return 'OK'
        return 'ERROR'

    def on_subscriber(self, sid, data):
        self.subscribers.append((sid, data['id']))
        self.enter_room(sid, self.namespace)

    def on_list_subscribers(self, sid, data):
        return self.subscribers

    def on_define(self, sid, data):
        return self.definition

    def on_message(self, sid, data):
        self.send(data, room=self.namespace, skip_sid=sid)

class PubTopic(socketio.ClientNamespace):
    def __init__(self, namespace=None, definition=None):
        super(PubTopic, self).__init__(namespace=namespace)
        self.definition = definition

    def on_connect(self):
        self.emit('publisher', {'definition': self.definition})

    def on_disconnect(self):
        pass


class SubTopic(socketio.ClientNamespace):
    def __init__(self, namespace=None, callback=None):
        super(SubTopic, self).__init__(namespace=namespace)
        self.topic_callback = callback

    def on_connect(self):
        self.emit('subscriber', None)

    def on_disconnect(self):
        pass

    def on_message(self, data):
        if self.topic_callback:
            self.topic_callback(data)
