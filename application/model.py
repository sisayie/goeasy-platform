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

from sqlalchemy.dialects.postgresql import JSONB


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
'''class Behaviour(db.Model):
    __tablename__ = "behaviour"
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key = True)
    start = db.Column(JSONB)
    end = db.Column(JSONB)
    meters = db.Column(db.Numeric(9,7))
    #accuracy = db.Column(db.Numeric(9,7))
    type = db.Column(db.String(20))
    journey_id = db.Column(db.String(40), db.ForeignKey("journey.journeyId"))
    
    def __init__(self, start, end, meters, type):
        self.start = start
        self.end = end
        self.meters = meters
        #self.accuracy = accuracy
        self.type = type
        '''
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
    '''tpv_defined_behaviour = db.Column(db.String(50000))
    app_defined_behaviour = db.Column(db.String(50000)) 
    user_defined_behaviour = db.Column(db.String(50000))'''
    tpv_defined_behaviour = db.Column(JSONB)
    app_defined_behaviour = db.Column(JSONB) 
    user_defined_behaviour = db.Column(JSONB)
    tpmmd = db.Column(db.Integer) # tpmmd detection status (0-done,  1-not_sent, 2-sent, 3-timeout, 100 < error_code)

    positions = db.relationship("Position", cascade="all,delete", backref = "positions", uselist=True)
    #tpv_defined_behaviour = db.relationship('Behaviour', cascade="all, delete", backref = "behaviour", uselist=True)
    
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
        self.tpv_defined_behaviour = tpv_defined_behaviour #json.dumps(tpv_defined_behaviour)
        self.app_defined_behaviour = app_defined_behaviour #json.dumps(app_defined_behaviour)
        self.user_defined_behaviour = user_defined_behaviour #json.dumps(user_defined_behaviour)
        self.tpmmd = tpmmd
#==========================================

# Schema

class JSONmsgSchema(ma.ModelSchema):
    journeyId = fields.String(required=True)
    json = fields.String()
    

class PositionSchema(ma.ModelSchema):
    lat = fields.Float()
    lon = fields.Float()
    timestamp = fields.DateTime()
    authenticity = fields.Integer()

class StartEndSchema(ma.ModelSchema):
    #authenticity = fields.Integer()
    #galileo_auth = fields.List()
    lat = fields.Float()
    lon = fields.Float()
    time =  fields.DateTime()

class BehaviourSchema(ma.ModelSchema):
    start = fields.Nested(StartEndSchema)
    end = fields.Nested(StartEndSchema)
    meters = fields.Float()
    type = fields.String()
    accuracy = fields.Float()
    
class JourneySchema(ma.ModelSchema):
    deviceId = fields.String()
    journeyId = fields.String(required=True) 
    sourceapp = fields.String()
    company_code = fields.String()
    company_trip_type = fields.String()
    startdate = fields.DateTime()
    enddate =  fields.DateTime()
    distance = fields.Float(allow_none=True)
    elapsedtime = fields.String()
    
    positions = fields.List(fields.Nested(PositionSchema))
    
    tpv_defined_behaviour = fields.List(fields.Nested(BehaviourSchema)) #fields.String()
    app_defined_behaviour = fields.List(fields.Nested(BehaviourSchema))
    user_defined_behaviour = fields.List(fields.Nested(BehaviourSchema))
    
    tpmmd = fields.Integer()
    
class CaseOneSchema(ma.ModelSchema):
    journeyId = fields.String(required=True)
    startdate = fields.DateTime()
    enddate =  fields.DateTime()
    distance = fields.Float(allow_none=True)
    elapsedtime = fields.String()
    #start_lat, start_lon, end_lat, end_lon, meters, type, accuracy
    tpv_defined_behaviour = fields.List(fields.Nested(BehaviourSchema)) #fields.String()
    tpmmd = fields.Integer()  
    
jsonmsg_schema = JSONmsgSchema()
jsonmsgs_schema = JSONmsgSchema(many=True)

#=============================================

journey_schema = JourneySchema()
journeys_schema = JourneySchema(many=True)

'''journey_schema = BehaviourSchema()
journeys_schema = BehaviourSchema(many=True)
'''
#=============================================

behaviour_schema = BehaviourSchema()
behaviours_schema = BehaviourSchema(many=True)

position_schema = PositionSchema()
positions_schema = PositionSchema(many=True)

caseone_schema = CaseOneSchema()
caseones_schema = CaseOneSchema(many=True)