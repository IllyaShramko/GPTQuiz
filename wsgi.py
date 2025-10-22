print("Before any imports")
import eventlet
eventlet.monkey_patch()
print("After monkey_patch")

from project import project, socketio  

if __name__ == "__main__":
    socketio.run(project, host="0.0.0.0", port=8080, debug=False)