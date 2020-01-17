# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:37:10 2019

@author: chala
"""

from datetime import datetime
from config import db, ma

#Model
#==========================================
class Position(db.Model):
    __tablename__ = "position"
    id = db.Column(db.Integer, primary_key = True)
    lat = db.Column(db.Numeric(9,7)) #precision & scale => https://www.postgresql.org/docs/9.6/datatype-numeric.html
    lon = db.Column(db.Numeric(9,7))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) # , onupdate=datetime.utcnow
    authenticity = db.Column(db.Integer)
    
    journey_id = db.Column(db.Integer, db.ForeignKey("journey.id"))
#==========================================
 
class Journey(db.Model):
    __tablename__ = 'journey'
    id = db.Column(db.Integer, primary_key=True)
    deviceId = db.Column(db.Integer)
    sessionId = db.Column(db.Integer)
    sourceApp = db.String(20)
    #common = db.Column(db.String(40))
    #positions = db.Column(db.String(10))
    t_behaviour = db.Column(db.String(10)) # tpv_defined_behaviour
    a_behaviour = db.Column(db.String(10)) # app_defined_behaviour
    u_behaviour = db.Column(db.String(10))  # user_defined_behaviour
    
    positions = db.relationship("Position", backref = "positions", uselist=True)

class JourneySchema(ma.ModelSchema):
    class Meta:
        model = Journey
        db_session = db.session
        
class PositionSchema(ma.ModelSchema):
    class Meta:
        model = Position
        db_session = db.session

journey_schema = JourneySchema()
journeys_schema = JourneySchema(many=True)

#=============================================
position_schema = PositionSchema()
positions_schema = PositionSchema(many=True)