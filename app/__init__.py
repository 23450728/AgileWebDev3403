from flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from elasticsearch import Elasticsearch

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'login'
moment = Moment()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    from blueprints import main
    app.register_blueprint(main)
    db.init_app(app)
    login.init_app(app)
    moment.init_app(app)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']])

    return app



    

