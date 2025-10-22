import eventlet
eventlet.monkey_patch()

import project 
import os

def HelloWorld(world):
    print(world)

HelloWorld("Print")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    project.socketio.run(project.project, host="0.0.0.0", port=port, debug=False)
