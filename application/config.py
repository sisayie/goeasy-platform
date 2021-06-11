# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:37:10 2019

@author: chala
"""
import os

from flask import Flask, jsonify, request, Blueprint
from flask_restplus import Api, Resource, apidoc

from flask_sqlalchemy import SQLAlchemy

from flask_marshmallow import Marshmallow
from sqlalchemy.orm import joinedload
from marshmallow import Schema, fields, pprint

import json

import logging

from resources.errors import errors

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)


user = os.environ['POSTGRES_USER']
pwd = os.environ['POSTGRES_PASSWORD']
db = os.environ['POSTGRES_DB']
host = os.environ['POSTGRES_HOST']
port = os.environ['POSTGRES_PORT']

DB_URI = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(user=user, pw=pwd, host=host, port=port, db=db)

server = Flask(__name__) 

server.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
server.config['SQLALCHEMY_ECHO'] = True
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
server.config["JSON_SORT_KEYS"] = False

db = SQLAlchemy(server)

blueprint = Blueprint('api', __name__)#, url_prefix='/v1')

api = Api(blueprint, #app=app, 
          doc='/doc/',
          version='1.0', 
          title='GOEASY Platform', 
          description='GOEASY Privacy-Aware Information Base and API',
          errors=errors
          )  
server.register_blueprint(blueprint)


ns = api.namespace('paib',description = 'GOEASY Platform Measurements for Location Based Services (LBS)')

ma = Marshmallow(api)