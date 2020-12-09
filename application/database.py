# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:37:10 2019

@author: chala
"""
# Database
import logging
logger = logging.getLogger(__file__)

from flask import request
from marshmallow import Schema, fields, pprint
from sqlalchemy import func
import json

from privacy_guard import anonymize, rangen
from utils import *

from model import *

from tpmmd import *

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
        
def fetch_positions(id):
    #positions = Position.query.filter_by(journey_id =str(id)).first() # one position returned
    #positions = Position.query.filter_by(journey_id =str(id)).all() # {} returned
    #positions = db.session.query(Position).filter_by(Position.journey_id=str(id)).all() # {} returned
    positions = db.session.query(Position).filter_by(journey_id=str(id)).all()
    
    if positions is not None:
        return position_schema.jsonify(positions)
    else:
        response = {"status": "Error",
                    "message": "Positions do not exist"
                    }
        return response

def fetch_time_range():
    start  = request.args.get('start_time', None)
    end  = request.args.get('end_time', None)
    
    #journey = db.session.query(journey_schema).filter(
    #    journey_schema.startDate >= start and journey_schema.endDate <=end
    #    ).all()
    
    #enddate = datetime.strptime("2020-07-02T08:44:47.241000+00:00", '%Y-%m-%dT%H:%M:%S.%f%z')
    #start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S.%f%z') #Convert str to datetime
    #start = start.strftime('%Y-%m-%dT%H:%M:%S') # extract datetime in specific format
    #end = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S.%f%z')
    #end = end.strftime('%Y-%m-%dT%H:%M:%S')
    
    start = date_format(start) # Convert input date to uniform format
    start = datetime.fromtimestamp(int(start)) #Convert timestamp to datetime
    start = start.strftime('%Y-%m-%dT%H:%M:%S') # extract datetime in specific format that matches date stored in db
    
    end = date_format(end)
    end = datetime.fromtimestamp(int(end)) #Convert timestamp to datetime
    end = end.strftime('%Y-%m-%dT%H:%M:%S') # extract datetime in specific format that matches date stored in db

    journey = Journey.query.filter(Journey.startdate >= start).all() #db.session.query(Journey).filter(
        
        #(func.DATE(start) <= func.DATE(Journey.startDate)) #func.DATE(datetime.strftime(datetime.strptime(str(Journey.startdate), '%Y-%m-%d %H:%M:%S.%f%z'), '%Y-%m-%dT%H:%M:%S')))
        #(func.DATE(start) <= func.DATE(Journey.startdate.strftime('%Y-%m-%dT%H:%M:%S'))) &
        #(func.DATE(Journey.enddate.strftime('%Y-%m-%dT%H:%M:%S')) <= func.DATE(end))
        #(datetime.fromtimestamp(Journey.startdate/1000) >= datetime.fromtimestamp(start))).all()
        #& (datetime.fromtimestamp(Journey.enddate/1000) >= datetime.fromtimestamp(end))
        #(datetime.strptime(start, '%Y-%m-%dT%H:%M:%S') <= datetime.strptime(Journey.startdate,'%Y-%m-%dT%H::%M::%S.%f')) &
        #(datetime.strptime(Journey.startdate, '%Y-%m-%dT%H::%M::%S.%f') <= datetime.strptime(end, '%Y-%m-%dT%H:%M:%S'))
        #).all()
    #logger.debug("Journey start date" + Journey.startdate)
    if journey is not None:
        return journey_schema.jsonify(journey)
    else:
        response = {"status": "Error",
                    "message": "Journey does not exist"
                    }
        return response

def fetch_MM(id):
    print( " fetch_MM for journeyId:" + id)
    journey = Journey.query.filter_by(journeyId=str(id)).first()
    print( "journey extracted from the DB: " + str(journey))

    if journey is not None:
        tpmmd = journey.tpmmd  # tpmmd detection status (0-done,  1-not_sent, 2-sent, 3-timeout, 100 < error_code)
        if tpmmd > 0:
            # not yet done or error 
            print( "journey is done !!!")
            response = {"status":  tpmmd,
                        "message": "Result not available or error"
                    }
            return response
        else:    
            mobilityMode = journey.tpv_defined_behaviour
            
            response = "{ 'tpv_defined' : " + mobilityMode + "}"
            print("response:" + str(response))
            return jsonify(response)
    else:
        print( "journey is None !!!")
        response = {"status": "Error",
                    "message": "Journey does not exist"
                    }
        return response
    
def add_new(): #TODO: Sanitize other conditions
    data = request.get_json()
    if data is not None:
        
        if data['positions']:
            response = {"status": "Success",
                        "message": "New journey registered"
                        }
            ano_id = rangen()             
            anon_journey = anonymize(data, 'deviceId',ano_id) 
      
            new_positions = []
            for element in anon_journey['positions']:
                new_positions.append(Position(lat = element['lat'],
                                              lon = element['lon'],
                                              timestamp = datetime.fromtimestamp(element['time']/1000), 
                                              authenticity = element['authenticity']))
            new_journey = Journey(
                                deviceId = anon_journey['deviceId'], 
                                journeyId = anon_journey['journeyId'], 
                                sourceApp = anon_journey['sourceApp'],
                                company_code = anon_journey['company_code'],
                                company_trip_type = anon_journey['company_trip_type'],
                                startDate = datetime.fromtimestamp(anon_journey['startDate']/1000),
                                endDate = datetime.fromtimestamp(anon_journey['endDate']/1000),
                                distance = anon_journey['distance'],
                                elapsedTime = anon_journey['elapsedTime'],
                                #positions = anon_journey['positions'], 
                                positions = new_positions,
                                #t_behaviour = anon_journey['t_behaviour'], 
                                #a_behaviour = anon_journey['a_behaviour'], 
                                #u_behaviour = anon_journey['u_behaviour'],
                                tpv_defined_behaviour = anon_journey['tpv_defined_behaviour'],
                                app_defined_behaviour = anon_journey['app_defined_behaviour'],
                                user_defined_behaviour = anon_journey['user_defined_behaviour'],
                                tpmmd=1
                                )

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
