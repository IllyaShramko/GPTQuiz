import project 

if __name__ == '__main__':
    project.socketio.run(project.project, host="localhost", port=5000, debug=True)