#!/usr/bin/python
# coding: utf-8

import os
from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
from flaskext.bcrypt import Bcrypt
from flaskext.login import LoginManager

app = Flask( __name__,
    static_folder="../static",
    template_folder="../templates" )

app.secret_key = os.environ["SECRET_KEY"]

bcrypt = Bcrypt( app )

login_manager = LoginManager()
login_manager.setup_app( app )

@login_manager.user_loader
def load_user( id ):
    return User.query.filter_by( id=id ).first()

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["HEROKU_SHARED_POSTGRESQL_ORANGE_URL"]
app.config["GOOGLE_API_BROWSER_KEY"] = os.environ["GOOGLE_API_BROWSER_KEY"]

db = SQLAlchemy( app )

from models import *
from views import *
from forms import *
