# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:37:10 2019

@author: chala
"""
# Database
import logging


from flask import request
from marshmallow import Schema, fields, pprint
from sqlalchemy import func, cast, Numeric
from sqlalchemy.types import Float

import json

from privacy_guard import *
from utils import *

from model import *

from tpmmd import *

logger = logging.getLogger(__file__)

#utilities
'''
get all journeyIds
get all keys corresponding to the journeyIds
update the journeyIds
return the journey'''

#class Database:
def fetch_all():
    journeys = Journey.query.all()
    '''
    enc_keys = EncDB.query.all() 
    enc_j = enc_journey(enc_keys)
    '''
    if journeys is not None:
        '''for d in data:
            [d.__dict__.update(enc_j) for d in journey] #d.journeyId = enc_key.tp_key
        '''
        #return journeys_schema.jsonify(journey)
        #response = journeys_schema.jsonify(journey)
        
        response = journeys_schema.dump(journeys)
    else:
        response = {"status": "Error",
                    "message": "Nothing to query"
                    }
    return response
        
""" def fetch_one(id):
    journey = Journey.query.filter_by(journeyId =str(id)).first()
    
    logger.info("Journey ==> " + str(journey))
    
    if journey is not None:
<<<<<<< Updated upstream
        #journey.app_defined_behaviour = json.dumps(journey.app_defined_behaviour)
        #journey.tpv_defined_behaviour = json.dumps(journey.tpv_defined_behaviour)
        #journey.user_defined_behaviour = json.dumps(journey.user_defined_behaviour)
        mobilityMode = journey.tpv_defined_behaviour
        response = jsonify( tpv_defined_behaviour = mobilityMode)

        return journey_schema.jsonify(journey, tpv_defined_behaviour = mobilityMode)
=======
        udb = journey.user_defined_behaviour
        journey.user_defined_behaviour = udb
        return journey_schema.jsonify(journey)
>>>>>>> Stashed changes
    else:
        response = {"status": "Error",
                    "message": "Journey does not exist"
                    }
        return response """

def fetch_one(id):
    '''
    enc_key = EncDB.query.filter_by(tp_key = str(id)).first()
    journey_id = None
    journey = None
    if enc_key is not None:
        journey_id = enc_key.journey_id
    '''
    journey = Journey.query.filter_by(journeyId =str(id)).first()
    #print(json.dumps(journey.user_defined_behaviour))
    #logger.info("Journey ==> " + str(journey))
    if journey is not None:
        response = journey_schema.jsonify(journey)
        '''response = jsonify( 
                company_code = journey.company_code,
                company_trip_type = journey.company_trip_type,
                deviceId = str(journey.deviceId),
                distance = int(journey.distance),
                elapsedtime = journey.elapsedtime,
                enddate = int(journey.enddate.timestamp()*1000),
                journeyId = journey.journeyId,
                #journeyId = enc_key.tp_key,
                mainTypeSpace = journey.mainTypeSpace,
                mainTypeTime = journey.mainTypeTime,
                positions = [{'lat':float(e.lat), 'lon':float(e.lon), 'partialDistance':int(e.partialDistance), 
                                'timestamp':int(e.timestamp.timestamp()*1000), 'authenticity':int(e.authenticity) 
                            } for e in journey.positions],
                sourceapp = journey.sourceapp,
                startdate = int(journey.startdate.timestamp()*1000),
                tpmmd = int(journey.tpmmd),
                app_defined_behaviour = journey.app_defined_behaviour,
                user_defined_behaviour = journey.user_defined_behaviour,
                tpv_defined_behaviour = journey.tpv_defined_behaviour
                )''' 
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

'''from sqlalchemy import create_engine
from config import DB_URI

db = create_engine(DB_URI)
'''
def fetch_time_range():
    start  = request.args.get('start_time', None)
    end  = request.args.get('end_time', None)
    
    start = date_format(start) # Convert input date to uniform format
    start = datetime.fromtimestamp(int(start)) # Convert timestamp to datetime
    start = start.strftime('%Y-%m-%dT%H:%M:%S') # extract datetime in specific format that matches date stored in db
    
    end = date_format(end)
    end = datetime.fromtimestamp(int(end)) #Convert timestamp to datetime
    end = end.strftime('%Y-%m-%dT%H:%M:%S') # extract datetime in specific format that matches date stored in db

    journey = db.session.query(Journey).filter(
        (func.DATE(start) <= func.DATE(Journey.startdate)) &
        (func.DATE(Journey.enddate) <= func.DATE(end))
        ).all()

    if journey is not None:
        response = journeys_schema.jsonify(journey)
        #return caseones_schema.jsonify(journey)
        
    else:
        response = {"status": "Error",
                    "message": "Journey does not exist"
                    }
    return response

from sqlalchemy.sql import column
        
def fetch_space_range():
    start_lat  = request.args.get('start_lat', None)
    start_lat = float(start_lat)
    start_lon  = request.args.get('start_lon', None)
    start_lon = float(start_lon)
    radius = request.args.get('radius', None)
    radius = float(radius)

    '''logger.info("Lat ==> " + str(start_lat))   
    logger.info("Lon ==> " + str(start_lon))
    logger.info("Radius ==> " + str(radius))
    logger.info("Lat from DB ==> " + str(Journey.tpv_defined_behaviour["start"]["lat"].astext))
    logger.info("Lat, lon from DB ==> " + str((Journey.tpv_defined_behaviour.contains([{"start": {"lat": float(start_lat), "lon": float(start_lon)}}]))))
    logger.info("Lon from DB ==> " + str(Journey.tpv_defined_behaviour["start"]["lon"].astext.cast(Float)))
    logger.info("Meters from DB ==> " + str(Journey.tpv_defined_behaviour["meters"].astext.cast(Float)))
    '''
    try:
        journey = db.session.query(Journey).filter(
            Journey.tpv_defined_behaviour.contains([{"start": {"lat": float(start_lat), "lon": float(start_lon)}}])
            ).all()
        logger.info("Journey ==> " + str(journey))
        
        for j in journey:
            for t in j.tpv_defined_behaviour:
                if t['meters'] > radius:
                    journey.remove(j)
                    logger.info("Journey start_lat ==> " + str(t['start']['lat']))
                    logger.info("Journey start_lon ==> " + str(t['start']['lon']))
                    logger.info("Journey start_radius ==> " + str(t['meters']) + str(type(t['meters'])))
                    logger.info("Journey start_type ==> " + str(t['type']))
                
    except Exception as e:
        print("Error" + str(e))
    if journey is not None:
        
        return caseones_schema.jsonify(journey)
    else:
        response = {"status": "Error",
                    "message": "Journey does not exist"
                    }
        return response

def fetch_MM(id):
    logger.debug( " fetch_MM for journeyId:" + id)
    journey = Journey.query.filter_by(journeyId=str(id)).first()
    #logger.debug( "journey extracted from the DB: " + str(journey))

    if journey is not None:
        tpmmd = journey.tpmmd  # tpmmd detection status (0-done,  1-not_sent, 2-sent, 3-timeout, 100 < error_code)
        if tpmmd > 0:
            # not yet done or error 
            logger.debug( "journey is not done !!!")
            response = {"status":  tpmmd,
                        "message": "Result not available or error"
                    }
            return response
        else:    
            mobilityMode = journey.tpv_defined_behaviour
            
            response = jsonify( tpv_defined_behaviour = mobilityMode) 
            logger.debug("response: " + str(response))
            return response
    else:
        logger.debug( "journey is None !!!")
        response = {"status": "Error",
                    "message": "Journey does not exist"
                    }
        return response
    
def add_new(): #TODO: Sanitize other conditions
    data = request.get_json()
    if data is not None: 
        if data['positions']:
            ano_id = rangen()             
            anon_journey = anonymize(data, 'deviceId',ano_id) 
      
            new_positions = []
            for element in anon_journey['positions']:
                new_positions.append(Position(lat = element['lat'],
                                              lon = element['lon'],
                                              partialDistance = element['partialDistance'],
                                              timestamp = datetime.fromtimestamp(element['time']/1000), 
                                              authenticity = element['authenticity']))
                                              
            new_journey = Journey(
                                deviceId = anon_journey['deviceId'], 
                                journeyId = anon_journey['journeyId'], 
                                sourceapp = anon_journey['sourceApp'],
                                company_code = anon_journey['company_code'],
                                company_trip_type = anon_journey['company_trip_type'],
                                mainTypeSpace = anon_journey['mainTypeSpace'],
                                mainTypeTime = anon_journey['mainTypeTime'],
                                startdate = datetime.fromtimestamp(anon_journey['startDate']/1000),
                                enddate = datetime.fromtimestamp(anon_journey['endDate']/1000),
                                distance = anon_journey['distance'],
                                elapsedtime = anon_journey['elapsedTime'],
                                positions = new_positions,   
                                tpv_defined_behaviour = anon_journey['tpv_defined_behaviour'],
                                app_defined_behaviour = anon_journey['app_defined_behaviour'],
                                user_defined_behaviour = anon_journey['user_defined_behaviour'],
                                tpmmd=1
                                )

            db.session.add(new_journey)
            new_enc = EncDB(journeyId = anon_journey['journeyId'])
            db.session.add(new_enc)

            '''
            new_jsonmsg = JSONmsg(
                                journeyId = anon_journey['journeyId'],
                                json = data
            )

            db.session.add(new_jsonmsg)
            '''
            try:
                db.session.commit()
                response = {"status": "Success",
                            "message": "New journey registered"
                            }
                sendQueue.put(data)
            except Exception as e:
                db.session.rollback()
                response = {
                            "status": "Error",
                            "message": str(e.message)
                        } 
        else:
            response = {
                        "status": "Error",
                        "message": "Bad request body"
                        }
    else:
        response = {
                    "status": "Error",
                    "message": "Bad request body"
                    }    
    return response
    
def update_tpv_behaviour(id, new_behaviour):
    if new_behaviour is not None:
        journey = Journey.query.filter_by(journeyId =str(id)).first()
        if journey is not None:
            journey.tpv_defined_behaviour = new_behaviour #str(new_behaviour)
            journey.tpmmd = 0  # tpmmd detection status (0-done,  1-not_sent, 2-sent, 3-timeout, 100 < error_code)   
            try:
                db.session.commit()
                response = {"status": "Success",
                        "message": "Journey updated successfully"
                        } 
            except Exception as e:
                db.session.rollback()
                response = {"status": "Error",
                        "message": str(e)
                        }
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
                
            try:
                db.session.commit()
                response = {"status": "Success",
                        "message": "tpmmd updated successfully"
                        }
            except Exception as e:
                db.session.rollback()
                response = {"status": "Error",
                    "message": str(e)
                    }
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
            try:
                db.session.commit()
                response = {"status": "Success",
                        "message": "Journey updated successfully"
                        }
            except Exception as e:
                db.session.rollback()
                response = {"status": "Error",
                        "message": str(e)
                        }
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
        try:
            db.session.commit()
            response = {"status": "Success",
                    "message": "Journey deleted successfully"
                    }
        except Exception as e:
            db.session.rollback()
            response = {"status": "Error",
                    "message": str(e)
                    }
    else:
        response = {"status": "Error",
                    "message": "Journey does not exist"
                    }
    return response
