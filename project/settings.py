import flask
import flask_migrate, flask_sqlalchemy
from flask_socketio import SocketIO, emit

project = flask.Flask(
    import_name= 'project',
    template_folder= 'templates',
    static_folder= 'static'
)
project.config['SECRET_KEY'] = "secret"
project.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

DATABASE= flask_sqlalchemy.SQLAlchemy(app= project)

migrate= flask_migrate.Migrate(app= project, db= DATABASE)
socketio = SocketIO(app=project, async_mode='eventlet')

