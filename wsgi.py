from project.settings import project, socketio

def HelloWorld(world):
    print(world)

HelloWorld("Print")

# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 8080))
#     project.socketio.run(project.project, host="127.0.0.1", port=port, debug=False)
