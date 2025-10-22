import project 
import os

def HelloWorld(world):
    print(world)

HelloWorld("Print")

if __name__ == '__main__':
    project.socketio.run(project.project, host="127.0.0.1", port=5000, debug=True)
