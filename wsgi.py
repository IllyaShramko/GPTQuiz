from project import project, socketio
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    socketio.run(project, host="0.0.0.0", port=port)