import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # docker run --name elasticsearch -d --rm -p 9200:9200 \
    # --memory="2GB" \
    # -e discovery.type=single-node -e xpack.security.enabled=false \
    # -t docker.elastic.co/elasticsearch/elasticsearch:8.13.0

    # export ELASTICSEARCH_URL=http://localhost:9200
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    ADMINS = ['admin@gmail.com']
    POSTS_PER_PAGE = 25

class TestConfig(Config):
    #References to  Miguel Grinberg https://github.com/miguelgrinberg/microblog/blob/v0.23/tests.py
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'