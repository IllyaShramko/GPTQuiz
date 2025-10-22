import os
from flask import Flask

project = Flask(__name__)

@project.route('/')
def index():
    return "Hello World! Railway test works!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    project.run(host="0.0.0.0", port=port, debug=True)
