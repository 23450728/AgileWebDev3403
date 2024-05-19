from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes

#Refer to https://github.com/miguelgrinberg/microblog/tree/v0.15/app/auth