# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:37:10 2019

@author: chala
"""

from datetime import datetime
from config import db, ma

from marshmallow import fields, validates_schema, ValidationError

from collections import OrderedDict 

import json

from sqlalchemy.dialects.postgresql import JSONB

from utils import *

import crypt

#Model
#==========================================
'''
class JSONmsg(db.Model):
    __tablename__ = "jsonmsg"
    __table_args__ = {'extend_existing': True} 
    journeyId = db.Column(db.String(40), primary_key = True)
    json = db.Column(db.String(500000))
    def __init__(self, journeyId, json):
        self.journeyId = journeyId
        raw_data = str(json)
        self.json = raw_data[0:JSONmsg.json.property.columns[0].type.length]
'''
#==========================================
class Position(db.Model):
    __tablename__ = "position"
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key = True)
    lat = db.Column(db.Numeric(9,7)) #precision & scale => https://www.postgresql.org/docs/9.6/datatype-numeric.html
    lon = db.Column(db.Numeric(10,7))
    partialDistance = db.Column(db.Numeric())
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) # , onupdate=datetime.utcnow
    authenticity = db.Column(db.Integer)
    
    journey_id = db.Column(db.String(40), db.ForeignKey("journey.journeyId"))
    
    def __init__(self, lat, lon, partialDistance, timestamp, authenticity):
        self.lat = lat
        self.lon = lon
        self.partialDistance = partialDistance
        self.timestamp = timestamp
        self.authenticity = authenticity
#==========================================

class Behaviour(db.Model):
    __tablename__ = "behaviour"
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key = True)
    start = db.Column(JSONB)
    end = db.Column(JSONB)
    meters = db.Column(db.Numeric(9,7))
    accuracy = db.Column(db.Numeric(9,7))
    type = db.Column(db.String(20))
    journey_id = db.Column(db.String(40), db.ForeignKey("journey.journeyId"))
    
    def __init__(self, start, end, meters, type):
        self.start = start
        self.end = end
        self.meters = meters
        self.accuracy = accuracy
        self.type = type
       
class Journey(db.Model):
    __tablename__ = 'journey'
    __table_args__ = {'extend_existing': True} 
    deviceId = db.Column(db.Integer)
    journeyId = db.Column(db.String(40), primary_key=True) #sessionId = db.Column(db.Integer); e.g., 550e8400-e29b-41d4-a716-446655440000
    sourceapp = db.Column(db.String(20))
    company_code = db.Column(db.String(20))
    company_trip_type = db.Column(db.String(20))
    mainTypeSpace = db.Column(db.String()) 
    mainTypeTime = db.Column(db.String()) 
    startdate = db.Column(db.DateTime)
    enddate =  db.Column(db.DateTime)
    distance = db.Column(db.Numeric())
    elapsedtime = db.Column(db.String(40))
    tpv_defined_behaviour = db.Column(JSONB)
    app_defined_behaviour = db.Column(JSONB) 
    user_defined_behaviour = db.Column(JSONB)
    tpmmd = db.Column(db.Integer) # tpmmd detection status (0-done,  1-not_sent, 2-sent, 3-timeout, 100 < error_code)

    positions = db.relationship("Position", cascade="all,delete", backref = "positions", uselist=True)
    #tpv_defined_behaviour = db.relationship('Behaviour', cascade="all, delete", backref = "behaviour", uselist=True)
    
    def __init__(self, deviceId, journeyId, sourceapp, company_code, company_trip_type, mainTypeSpace, mainTypeTime, startdate, enddate, distance, elapsedtime, tpv_defined_behaviour, app_defined_behaviour, user_defined_behaviour, tpmmd=1, positions = None):
        self.deviceId = deviceId
        self.journeyId = journeyId #self.sessionId = sessionId
        self.sourceapp = sourceapp
        self.company_code = company_code
        self.company_trip_type = company_trip_type
        self.mainTypeSpace = mainTypeSpace
        self.mainTypeTime = mainTypeTime
        self.startdate = startdate
        self.enddate = enddate
        self.distance = distance
        self.elapsedtime = elapsedtime
        if positions is None:
            positions = []
        self.positions = positions
        self.tpv_defined_behaviour = tpv_defined_behaviour #json.dumps(tpv_defined_behaviour)
        self.app_defined_behaviour = app_defined_behaviour #json.dumps(app_defined_behaviour)
        self.user_defined_behaviour = user_defined_behaviour #json.dumps(user_defined_behaviour)
        self.tpmmd = tpmmd
        
class EncDB(db.Model):
    __tablename__ = 'encdb'
    __table_args__ = {'extend_existing': True}
    journey_id = db.Column(db.String(40), primary_key=True)
    tp_key = db.Column(db.String())
    
    def __init__(self, journeyId):
        self.journey_id = journeyId
        self.tp_key = crypt.crypt('journey_id', crypt.METHOD_MD5) #self.tp_key = crypt('journey_id', gen_salt('md5'))
    
#==========================================

# Schema
'''
class JSONmsgSchema(ma.ModelSchema):
    journeyId = fields.String(required=True)
    json = fields.String()
    
    class Meta:
        strict = True
'''       
class PositionSchema(ma.ModelSchema):
    lat = fields.Float() #validate=valid_ranges_lat)
    lon = fields.Float() #validate=valid_ranges_lon)
    partialDistance = fields.Float()  
    timestamp = fields.DateTime()
    authenticity = fields.Integer()
    
    class Meta:
        strict = True
        
    @validates_schema
    def valid_ranges_lat(self, data):
        if data<-90 or data>90:
            raise ValidationError("Latitude out of range.")
    '''def valid_ranges_lon(data):
        if data<-180 or data>180:
            raise ValidationError("Longitude out of range.")'''
    
class EncDBSchema(ma.ModelSchema):
    journey_id = fields.String(required=True)
    tp_key = fields.String(required=True)
    
    class Meta:
        strict = True
        
class StartSchema(ma.ModelSchema):
    authenticity = fields.Integer()
    #galileo_auth = fields.Nested()
    #galileo_status = fields.Nested()
    lat = fields.Float() #validate=valid_ranges_lat)
    lon = fields.Float() #validate=valid_ranges_lon)
    start_time =  fields.DateTime()
    #class Meta:
    #    strict = True
class EndSchema(ma.ModelSchema):
    authenticity = fields.Integer()
    #galileo_auth = fields.Nested()
    #galileo_status = fields.Nested()
    lat = fields.Float() #validate=valid_ranges_lat)
    lon = fields.Float() #validate=valid_ranges_lon)
    end_time =  fields.DateTime()
    
class BehaviourSchema(ma.ModelSchema):
    #start = fields.Nested(StartSchema)
    #end = fields.Nested(EndSchema)
    start = fields.Nested(PositionSchema)
    end = fields.Nested(PositionSchema)
    meters = fields.Float()
    type = fields.String()
    accuracy = fields.Float()

class JourneySchema(ma.ModelSchema):
    deviceId = fields.String()
    journeyId = fields.String(required=True) 
    sourceapp = fields.String()
    company_code = fields.String()
    company_trip_type = fields.String()
    mainTypeSpace = fields.String() 
    mainTypeTime = fields.String() 
    startdate = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    enddate =  fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    distance = fields.Float(allow_none=True)
    elapsedtime = fields.String()
    
    positions = fields.List(fields.Nested(PositionSchema))
    
    tpv_defined_behaviour = fields.List(fields.Nested(BehaviourSchema)) 
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
    app_defined_behaviour = fields.List(fields.Nested(BehaviourSchema(many=True)))
    tpv_defined_behaviour = fields.List(fields.Nested(BehaviourSchema(many=True)))
    user_defined_behaviour = fields.List(fields.Nested(BehaviourSchema(many=True))) 
    tpmmd = fields.Integer()  
    
'''jsonmsg_schema = JSONmsgSchema()
jsonmsgs_schema = JSONmsgSchema(many=True)'''

#=============================================

journey_schema = JourneySchema()
journeys_schema = JourneySchema(many=True)

'''journey_schema = BehaviourSchema()
journeys_schema = BehaviourSchema(many=True)
'''
encdb_schema = EncDBSchema()
encdbs_schema = EncDBSchema(many=True)
#=============================================

#start_end_schema = StartEndSchema()

behaviour_schema = BehaviourSchema()
behaviours_schema = BehaviourSchema(many=True)

position_schema = PositionSchema()
positions_schema = PositionSchema(many=True)

caseone_schema = CaseOneSchema()
caseones_schema = CaseOneSchema(many=True)