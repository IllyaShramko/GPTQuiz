import eventlet
eventlet.monkey_patch()

import project, os

if __name__ == '__main__':
    project.socketio.run(project.project, host="0.0.0.0", port=int(os.environ.get("PORT")), debug=False)