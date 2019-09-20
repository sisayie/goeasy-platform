# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:29:00 2019

@author: chala
"""

from flask import Flask
#import flask_sqlalchemy

from .models import db
from . import config

def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URL'] = config.DATABASE_CONNECTION_URL
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.app_context().push()
    db.init_app(flask_app)
    db.create_all()
    print("Create app done")
    return flask_app