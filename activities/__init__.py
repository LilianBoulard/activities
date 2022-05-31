from flask import Flask

from .database.sql import db
from .app import app as app_blueprint


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    app.register_blueprint(app_blueprint)

    return app
