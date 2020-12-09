# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:37:10 2019

@author: chala
"""

from datetime import datetime
from config import db, ma

from marshmallow import fields


from collections import OrderedDict 

import json


#Model
#==========================================
class JSONmsg(db.Model):
    __tablename__ = "jsonmsg"
    __table_args__ = {'extend_existing': True} 
    journeyId = db.Column(db.String(40), primary_key = True)
    json = db.Column(db.String(50000))
    def __init__(self, journeyId, json):
        self.journeyId = journeyId
        self.json = str(json)

#==========================================
class Position(db.Model):
    __tablename__ = "position"
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key = True)
    lat = db.Column(db.Numeric(9,7)) #precision & scale => https://www.postgresql.org/docs/9.6/datatype-numeric.html
    lon = db.Column(db.Numeric(9,7))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) # , onupdate=datetime.utcnow
    authenticity = db.Column(db.Integer)
    
    journey_id = db.Column(db.String(40), db.ForeignKey("journey.journeyId"))
    
    def __init__(self, lat, lon, timestamp, authenticity):
        self.lat = lat
        self.lon = lon
        self.timestamp = timestamp
        self.authenticity = authenticity
#==========================================
 
class Journey(db.Model):
    __tablename__ = 'journey'
    __table_args__ = {'extend_existing': True} 
    deviceId = db.Column(db.Integer)
    journeyId = db.Column(db.String(40), primary_key=True) #sessionId = db.Column(db.Integer); e.g., 550e8400-e29b-41d4-a716-446655440000
    sourceapp = db.Column(db.String(20))
    company_code = db.Column(db.String(20))
    company_trip_type = db.Column(db.String(20))
    startdate = db.Column(db.DateTime)
    enddate =  db.Column(db.DateTime)
    distance = db.Column(db.Numeric())
    elapsedtime = db.Column(db.String(40))
    tpv_defined_behaviour = db.Column(db.String(50000))
    app_defined_behaviour = db.Column(db.String(50000)) 
    user_defined_behaviour = db.Column(db.String(50000))
    tpmmd = db.Column(db.Integer) # tpmmd detection status (0-done,  1-not_sent, 2-sent, 3-timeout, 100 < error_code)

    positions = db.relationship("Position", cascade="all,delete", backref = "positions", uselist=True)
    
    def __init__(self, deviceId, journeyId, sourceapp, company_code, company_trip_type, startdate, enddate, distance, elapsedtime, tpv_defined_behaviour, app_defined_behaviour, user_defined_behaviour, tpmmd=1, positions = None):
        self.deviceId = deviceId
        self.journeyId = journeyId #self.sessionId = sessionId
        self.sourceapp = sourceapp
        self.company_code = company_code
        self.company_trip_type = company_trip_type
        self.startdate = startdate
        self.enddate = enddate
        self.distance = distance
        self.elapsedtime = elapsedtime
        if positions is None:
            positions = []
        self.positions = positions #An address object
        self.tpv_defined_behaviour = json.dumps(tpv_defined_behaviour)
        self.app_defined_behaviour = json.dumps(app_defined_behaviour)
        self.user_defined_behaviour = json.dumps(user_defined_behaviour)
        self.tpmmd = tpmmd
#==========================================

class JSONmsgSchema(ma.ModelSchema):
    journeyId = fields.String(required=True)
    json = fields.String()
    

class PositionSchema(ma.ModelSchema):
    lat = fields.Float()
    lon = fields.Float()
    timestamp = fields.DateTime()
    authenticity = fields.Integer()

class JourneySchema(ma.ModelSchema):
    deviceId = fields.String()
    journeyId = fields.String(required=True) #sessionId = fields.String()
    sourceapp = fields.String()
    company_code = fields.String()
    company_trip_type = fields.String()
    startdate = fields.DateTime()
    enddate =  fields.DateTime()
    distance = fields.Float(allow_none=True)
    elapsedtime = fields.String()
    
    positions = fields.List(fields.Nested(PositionSchema))
    
    tpv_defined_behaviour = fields.String()
    app_defined_behaviour = fields.String()
    user_defined_behaviour = fields.String()
    
    tpmmd = fields.Integer()        

jsonmsg_schema = JSONmsgSchema()
jsonmsgs_schema = JSONmsgSchema(many=True)

#=============================================

journey_schema = JourneySchema()
journeys_schema = JourneySchema(many=True)

#=============================================
position_schema = PositionSchema()
positions_schema = PositionSchema(many=True)