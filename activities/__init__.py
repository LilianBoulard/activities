from flask import Flask

from .database.sql import db
from .utils import secret_key
from .app import app as app_blueprint


def create_app():
    app = Flask(__name__)

    # SQL database config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Session config
    #app.config['SESSION_FILE_DIR']
    #app.config['SESSION_FILE_THRESHOLD']
    #app.config['SESSION_FILE_MODE']
    app.config['SECRET_KEY'] = secret_key()

    db.init_app(app)

    app.register_blueprint(app_blueprint)

    return app
