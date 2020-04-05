from flask import Flask, g, jsonify
from features.node import Node
from features.core_data import Watcher
from features.topics import PubTopic

app = Flask(__name__)

with app.app_context():
    watcher = Watcher()

moove_node = Node('watcher')
moove_node.register_topic(watcher)
moove_node.run()

DEBUG = True

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/node_list')
def node_list():
    return jsonify(watcher.node_list)  # TODO figure out why this doesn't work