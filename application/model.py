# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:37:10 2019

@author: chala
"""

from datetime import datetime
from config import db, ma

from marshmallow import fields


from collections import OrderedDict #TODO: TEST


#Model
#==========================================
class JSONmsg(db.Model):
    __tablename__ = "jsonmsg"
    journeyId = db.Column(db.String(40), primary_key = True)
    json = db.Column(db.String(4000))
    def __init__(self, journeyId, json):
        self.journeyId = journeyId
        self.json = str(json)

#==========================================
class Position(db.Model):
    __tablename__ = "position"
    id = db.Column(db.Integer, primary_key = True)
    lat = db.Column(db.Numeric(9,7)) #precision & scale => https://www.postgresql.org/docs/9.6/datatype-numeric.html
    lon = db.Column(db.Numeric(9,7))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) # , onupdate=datetime.utcnow
    authenticity = db.Column(db.Integer)
    
    journey_id = db.Column(db.String(40), db.ForeignKey("journey.journeyId"))
    
    def __init__(self, lat, lon, timestamp, authenticity):
        #self.id = id
        self.lat = lat
        self.lon = lon
        self.timestamp = timestamp
        self.authenticity = authenticity
#==========================================
 
class Journey(db.Model):
    __tablename__ = 'journey'
    #id = db.Column(db.Integer, primary_key=True)
    deviceId = db.Column(db.Integer)
    journeyId = db.Column(db.String(40), primary_key=True) #sessionId = db.Column(db.Integer); e.g., 550e8400-e29b-41d4-a716-446655440000
    sourceApp = db.String(20)
    #common = db.Column(db.String(40))
    #positions = db.Column(db.String(10))
    t_behaviour = db.Column(db.String(500)) 
    tpv_defined_behaviour = db.Column(db.String(500))
    a_behaviour = db.Column(db.String(500)) 
    app_defined_behaviour = db.Column(db.String(500))
    u_behaviour = db.Column(db.String(500)) 
    user_defined_behaviour = db.Column(db.String(500))
    tpmmd = db.Column(db.Integer) # tpmmd detection status (0-done,  1-not_sent, 2-sent, 3-timeout, 100 < error_code)

    positions = db.relationship("Position", cascade="all,delete", backref = "positions", uselist=True)
    
    def __init__(self, deviceId, journeyId, sourceApp,  t_behaviour, a_behaviour, u_behaviour, tpv_defined_behaviour, app_defined_behaviour, user_defined_behaviour, tpmmd=1, positions = None):
        #self.id = id
        self.deviceId = deviceId
        self.journeyId = journeyId #self.sessionId = sessionId
        self.sourceApp = sourceApp
        if positions is None:
            positions = []
        self.positions = positions #An address object
        self.t_behaviour = str(t_behaviour)
        self.a_behaviour = str(a_behaviour)
        self.u_behaviour = str(u_behaviour)
        self.tpv_defined_behaviour = str(tpv_defined_behaviour)
        self.app_defined_behaviour = str(app_defined_behaviour)
        self.user_defined_behaviour = str(user_defined_behaviour)
        self.tpmmd = tpmmd
#==========================================

class JSONmsgSchema(ma.ModelSchema):
    journeyId = fields.String()
    json = fields.String()
    

class PositionSchema(ma.ModelSchema):
    lat = fields.Float()
    lon = fields.Float()
    timestamp = fields.DateTime()
    authenticity = fields.Integer()
    
    """class Meta:
        model = Position
        db_session = db.session"""


class JourneySchema(ma.ModelSchema):
    deviceId = fields.String()
    journeyId = fields.String() #sessionId = fields.String()
    
    positions = fields.List(fields.Nested(PositionSchema))
    
    t_behaviour = fields.String()
    a_behaviour = fields.String()
    u_behaviour = fields.String()
    
    tpmmd = fields.Integer()
    
    #fields = ("deviceId", "sessionId", "sourceApp", "positions", "a_behaviour", "t_behaviour", "u_behaviour")
    #ordered = True #present result in the oder given in fields tuple
    
    """class Meta:
        model = Journey
        db_session = db.session"""
        
        #fields = ("deviceId", "sessionId", "sourceApp", "positions") #TODO: TEST
        #ordered = True #TODO: TEST
        

jsonmsg_schema = JSONmsgSchema()
jsonmsgs_schema = JSONmsgSchema(many=True)

#=============================================

journey_schema = JourneySchema()
journeys_schema = JourneySchema(many=True)

#=============================================
position_schema = PositionSchema()
positions_schema = PositionSchema(many=True)