from flask import Flask
from logging.config import dictConfig
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_login import LoginManager
from flask_mysqldb import MySQL
import json

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
db = SQLAlchemy()
session = Session()

with open('./config.json') as config:
    config_data = json.load(config)


def create_app():
    app = Flask(__name__)
    app.logger.info('==================MOBIDOT=====================')

    app.config['SECRET_KEY'] = 'sceret secret'
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)
    app.config['SESSION_SQLALCHEMY_TABLE'] = "sessions"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    app.config.update(SESSION_COOKIE_SECURE=True)

    db.init_app(app)
    # app.session = Session(app)
    session.secret_key = 'super secret key'

    from app.back_office import back_office
    app.register_blueprint(back_office, url_prefix='/')
    app.session = {}

    return app

# def create_database(app):
#     if not path.exists('app/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')
