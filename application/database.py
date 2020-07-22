# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:37:10 2019

@author: chala
"""
# Database
from flask import request

from privacy_guard import anonymize, rangen

from model import *

from marshmallow import Schema, fields, pprint
import json

from tpmmd import *

#logger = logging.getLogger(__file__)

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
    journey = Journey.query.filter_by(journeyId =str(id)).first()

    if journey is not None:
        return journey_schema.jsonify(journey)
    else:
        response = {"status": "Error",
                    "message": "Journey does not exist"
                    }
        return response

    #deviceId = db.Column(db.Integer)
    #journeyId = db.Column(db.String(40)) #sessionId = db.Column(db.Integer)
    #sourceApp = db.String(20)

def fetch_MM(id):
    print( " fetch_MM for journeyId:" + id)
    journey = Journey.query.filter_by(journeyId=str(id)).first()
    print( "journey extracted from the DB: " + str(journey))

    if journey is not None:
        tpmmd = journey.tpmmd  # tpmmd detection status (0-done,  1-not_sent, 2-sent, 3-timeout, 100 < error_code)
        if tpmmd > 0:
            # not jet done or error 
            print( "journey is done !!!")
            response = {"status":  tpmmd,
                        "message": "Result not available or error"
                    }
            return response
        else:    
            #mobilityMode = json.loads(journey).get("t_behaviour") #json.loads(json.dumps(journey)).get("t_behaviour")
            mobilityMode = journey.tpv_defined_behaviour
            #print("Mobility Mode\n")	    
            #print(mobilityMode)
            response = "{ 'tpv_defined' : " + mobilityMode + "}"
            print("response:" + str(response))
            return jsonify(response)
            #return journey_schema.jsonify(json.loads(response))
            #return response
    else:
        print( "journey is None !!!")
        response = {"status": "Error",
                    "message": "Journey does not exist"
                    }
        return response

    #deviceId = db.Column(db.Integer)
    #journeyId = db.Column(db.String(40)) #sessionId = db.Column(db.Integer)
    #sourceApp = db.String(20)
    
def add_new(): #TODO: Sanitize other conditions
    data = request.get_json()
    if data is not None:
        
        if data['positions']:
            response = {"status": "Success",
                        "message": "New journey registered"
                        }
            ano_id = rangen()             
            anon_journey = anonymize(data, 'deviceId',ano_id) 
      
            #new_address = Address(telephone = data['address']['tel'], email = data['address']['email'])
            new_positions = []
            for element in anon_journey['positions']:
                new_positions.append(Position(lat = element['lat'],
                                              lon = element['lon'],
                                              timestamp = datetime.fromtimestamp(element['time']/1000), #https://stackoverflow.com/questions/10286224/javascript-timestamp-to-python-datetime-conversion
                                              authenticity = element['authenticity']))
            new_journey = Journey(
                                deviceId = anon_journey['deviceId'], 
                                journeyId = anon_journey['journeyId'], #sessionId = anon_journey['sessionId'],
                                sourceApp = anon_journey['sourceApp'],
                                #positions = anon_journey['positions'], 
                                positions = new_positions,
                                t_behaviour = anon_journey['t_behaviour'], 
                                a_behaviour = anon_journey['a_behaviour'], 
                                u_behaviour = anon_journey['u_behaviour'],
                                tpv_defined_behaviour = anon_journey['tpv_defined_behaviour'],
                                app_defined_behaviour = anon_journey['app_defined_behaviour'],
                                user_defined_behaviour = anon_journey['user_defined_behaviour'],
                                tpmmd=1
                                )
            #new_journey = Journey(common = data['common'], positions = data['positions'], t_behaviour = data['t_behaviour'], a_behaviour = data['a_behaviour'], u_behaviour=data['u_behaviour'])

            db.session.add(new_journey)

            new_jsonmsg = JSONmsg(
                                journeyId = anon_journey['journeyId'],
                                json = data
            )

            db.session.add(new_jsonmsg)

            db.session.commit()
            sendQueue.put(data)
        else:
            response = {"status": "Error",
                        "message": "Bad request body"
                        }
    else:
        response = {"status": "Error",
                    "message": "Bad request body"
                    }    
    return response
    
def update_tpv_behaviour(id, new_behaviour):
    if new_behaviour is not None:
        journey = Journey.query.filter_by(journeyId =str(id)).first()
        if journey is not None:
            journey.tpv_defined_behaviour = str(new_behaviour)
            journey.tpmmd = 0  # tpmmd detection status (0-done,  1-not_sent, 2-sent, 3-timeout, 100 < error_code)
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


def update_tpmmd(id, value=1):
    if value >= 0:
        journey = Journey.query.filter_by(journeyId =str(id)).first()
        if journey is not None:
            journey.tpmmd = value
            response = {"status": "Success",
                        "message": "tpmmd updated successfully"
                        }    
            db.session.commit()
        else:
            response = {"status": "Error",
                        "message": "Journey does not exist"
                        }
    else:
        response = {"status": "Error",
                    "message": "Bad tpmmd value"
                    }
    return response

def update_one(id):
    new_behaviour = request.json["t_behaviour"]
    if new_behaviour is not None:
        journey = Journey.query.filter_by(journeyId =str(id)).first()
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
    del_journey = Journey.query.filter_by(journeyId=str(id)).first() 
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
