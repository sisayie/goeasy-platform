# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:37:10 2019

@author: chala
"""
# Database
from flask import request

from privacy_guard import anonymize

from model import *


#class Database:
def fetch_all():
    data = Journey.query.all()
    if data is not None:
        response = {"status": "Success",
                    "message": "New journey registered"
                    }
        return data
    else:
        response = {"status": "Error",
                    "message": "Nothing to query"
                    }
        return response
        
def fetch_one(id):
    journey = Journey.query.filter_by(id=id).first()
    if journey is not None:
        return journey_schema.jsonify(journey)
    else:
        response = {"status": "Error",
                    "message": "Journey does not exist"
                    }
        return response

    deviceId = db.Column(db.Integer)
    sessionId = db.Column(db.Integer)
    sourceApp = db.String(20)
    
def add_new(): #TODO: Sanitize other conditions
    data = request.get_json()
    if data is not None:
        if data['positions']:
            response = {"status": "Success",
                        "message": "New journey registered"
                        }
                         
            anon_journey = anonymize(data, 'deviceId',987654) #TODO: 
      
            #new_address = Address(telephone = data['address']['tel'], email = data['address']['email'])
            new_positions = []
            for element in anon_journey['positions']:
                new_positions.append(Position(lat = element['lat'],
                                        lon = element['lon'],
                                        timestamp = datetime.fromtimestamp(element['time']/1000), #https://stackoverflow.com/questions/10286224/javascript-timestamp-to-python-datetime-conversion
                                        authenticity = element['authenticity']))
            
            new_journey = Journey(
                                deviceId = anon_journey['deviceId'], 
                                sessionId = anon_journey['sessionId'],
                                sourceApp = anon_journey['sourceApp'],
                                #positions = anon_journey['positions'], 
                                positions = new_positions,
                                t_behaviour = anon_journey['t_behaviour'], 
                                a_behaviour = anon_journey['a_behaviour'], 
                                u_behaviour=anon_journey['u_behaviour']
                                )
            #new_journey = Journey(common = data['common'], positions = data['positions'], t_behaviour = data['t_behaviour'], a_behaviour = data['a_behaviour'], u_behaviour=data['u_behaviour'])

            db.session.add(new_journey)
            db.session.commit()
        else:
            response = {"status": "Error",
                        "message": "Bad request body"
                        }
    else:
        response = {"status": "Error",
                    "message": "Bad request body"
                    }    
    return response
    
def update_one(id):
    new_behaviour = request.json["t_behaviour"]
    if new_behaviour is not None:
        journey = Journey.query.filter_by(id=id).first()
        if journey is not None:
            journey.t_behaviour = new_behaviour
            response = {"status": "Success",
                        "message": "Journey updated successfully"
                        }    
            db.session.commit()
        else:
            response = {"status": "Error",
                        "message": "Journey does not exist"
                        }
    else:
        response = {"status": "Error",
                    "message": "Bad request body"
                    }
    return response

    
def delete_one(id):
    del_journey = Journey.query.filter_by(id=id).first() 
    if del_journey is not None:
        db.session.delete(del_journey)
        db.session.commit()
        response = {"status": "Success",
                    "message": "Journey deleted successfully"
                    }
    else:
        response = {"status": "Error",
                    "message": "Journey does not exist"
                    }
    return response
