import project 

def HelloWorld(world):
    print(world)

HelloWorld("Print")

if __name__ == '__main__':
    project.socketio.run(project.project, host="0.0.0.0", port=8080, debug=True)
