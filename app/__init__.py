from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from elasticsearch import Elasticsearch

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
app.config.from_object(Config)
app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']])
db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)

from app import routes, models