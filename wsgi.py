import os
from flask import Flask
from flask_socketio import SocketIO

project = Flask(__name__)

@project.route('/')
def index():
    return "Hello World! SocketIO works!"

socketio = SocketIO(app=project, async_mode='gevent')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    socketio.run(project, host="0.0.0.0", port=port)
