from flask import Flask
from logging.config import dictConfig
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from os import path
from datetime import timedelta
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

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


session = Session()

def create_app():
    app = Flask(__name__)
    app.logger.info('==================MOBIDOT=====================')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SECRET_KEY'] = 'sceret secret'
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    # app.config['SESSION_FILE_THRESHOLD'] = 5
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=50)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SESSION_SQLALCHEMY_TABLE'] = "sessions"
    # app.config["SESSION_PERMANENT"] = False
    # app.config['SESSION_SQLALCHEMY'] = db

    app.config.update(SESSION_COOKIE_SECURE=True)

    db.init_app(app)
    # app.session = Session(app)
    session.secret_key = 'super secret key'
    # app.session.permanent = True
    # app.session.permanent_session_lifetime = timedelta(seconds=30)
    # session.init_app(app)
    from .models import User
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'back_office.auth_login'
    login_manager.init_app(app)
    from app.back_office import back_office
    app.register_blueprint(back_office, url_prefix='/')
    app.session = {}

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
