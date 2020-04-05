from flask import Flask, g
from features.node import Node

app = Flask(__name__)
node = Node('watcher')
node.run()

DEBUG = True

@app.route('/')
def hello_world():
    return 'Hello, World!'

