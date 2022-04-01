from flask import Flask
from logging.config import dictConfig
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

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


def create_app():
    app = Flask(__name__)
    app.logger.info('==================MOBIDOT=====================')

    app.config['SECRET_KEY'] = 'super secret key'
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)
    app.config['SESSION_SQLALCHEMY_TABLE'] = "sessions"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    app.config.update(SESSION_COOKIE_SAMESITE="Strict")
    # app.config['SESSION_COOKIE_DOMAIN'] = '127.0.0.1'
    app.config[' SESSION_COOKIE_NAME'] = 'session'
    # app.config['SERVER_NAME'] = '35.158.69.207:5001'
    db.init_app(app)
    session.secret_key = 'super secret key'

    # app.config['SECRET_KEY'] = 'sceret secret'
    # app.config['SESSION_TYPE'] = 'sqlalchemy'
    # # app.config['SERVER_NAME'] = '35.158.69.207'
    # # app.config['SESSION_COOKIE_HTTPONLY'] = '35.158.69.207:5001'
    # app.config['SESSION_COOKIE_DOMAIN'] = '127.0.1:5001'
    #
    # app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)
    # app.config['SESSION_SQLALCHEMY_TABLE'] = "sessions"
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # app.config['SQLALCHEMY_DATABASE_URI'] = ''
    # app.config.update(SESSION_COOKIE_SECURE=True)

    # db.init_app(app)
    # session.secret_key = 'super secret key'
    # session.seesion_type= 'filesystem'

    from app.back_office import back_office
    app.register_blueprint(back_office, url_prefix='/')
    # app.session = {}

    return app
