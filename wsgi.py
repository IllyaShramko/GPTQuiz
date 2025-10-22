from flask import Flask
from flask_socketio import SocketIO

project = Flask(__name__)

@project.route('/')
def index():
    return "Hello World! SocketIO works!"

socketio = SocketIO(app=project, async_mode='gevent')