# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:37:10 2019

@author: chala
"""
import os

from flask import Flask, jsonify, request
from flask_restplus import Api,Resource

from flask_sqlalchemy import SQLAlchemy

from flask_marshmallow import Marshmallow
from sqlalchemy.orm import joinedload
from marshmallow import Schema, fields, pprint

import json

user = os.environ['POSTGRES_USER']
pwd = os.environ['POSTGRES_PASSWORD']
db = os.environ['POSTGRES_DB']
host = os.environ['POSTGRES_HOST']
port = os.environ['POSTGRES_PORT']

DB_URI = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(user=user, pw=pwd, host=host, port=port, db=db)

app = Flask(__name__) 

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_ECHO'] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#app.config["JSON_SORT_KEYS"] = False

db = SQLAlchemy(app)

api = Api(app=app, 
          version='1.0', 
          title='Anonymizer Api', 
          description='GOEASY Api for Anonymizing Journeys')

ns = api.namespace('gep',description = 'GOEASY Platform Measurements for LBS')

ma = Marshmallow(api)