# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:37:36 2019

@author: chala
"""

import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class Positions(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.String(100))
    lon = db.Column(db.Integer)
    timestamp = db.Column(db.String(100)) #timestamptz or timestamp; discuss with Gianluca about which timestamp data type to use
    gal_auth = db.Column(db.Integer)