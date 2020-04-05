import socketio

class DataHandler(socketio.Namespace):
    def __init__(self, parent=None):
        super(DataHandler, self).__init__(namespace="/forWatcher")
        self.parent = parent
        self.topics = {}
        self.node_list = []

        print("Data initi")

    def on_connect(self, sid, environ):
        print('watcher in ', sid)

    def on_disconnect(self, sid):
        print('watcher out ', sid)

    def add_node(self, sid, node_name):
        self.node_list.append((node_name, sid))
        self.emit('node_list', self.node_list)

    def on_list_nodes(self, sid, data):
        self.emit('node_list', self.node_list, room=sid)

    def add_to_topic(self, name, publisher=None, subscriber=None):
        pass


class Watcher(socketio.ClientNamespace):
    def __init__(self, callback=None):
        super(Watcher, self).__init__(namespace="/forWatcher")
        self.topic_callback = callback
        self.node_list = []
        print("Watcher initi")

    def on_connect(self):
        # self.emit('list_nodes', None)
        print('watching')

    def on_disconnect(self):
        pass

    def on_node_list(self, data):
        self.node_list = data
        print('got ', self.node_list)

    def on_message(self, data):
        if self.topic_callback:
            self.topic_callback(data)

