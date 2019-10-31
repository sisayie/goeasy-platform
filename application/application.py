# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:37:10 2019

@author: chala
"""
from flask import Flask

from flask_restplus import Api, Resource, fields

import json

application = Flask(__name__)
api = Api(application, version='1.0', title='Anonymizer Api', description='GOEASY Api for Anonymizing Journeys')
name_space = api.namespace('journeys', description='Measurements for LBS')

#Sample test data, should be replaced by real one from GAPES
all_journeys = [
{
  "deviceId":123445,
  "timestamp": 1299855909699155,
  "points": [
              {"point": "1", "start": "13.00", "stop": "13.35"},
              {"point": "2", "start": "11.00", "stop": "14.35"}
          ]
        }
]

@application.route("/")
#def hello():
#    return "<h1>Anonymizer Home</h1>"
#TODO: organize it into class
def anonymize(adict, k, v):
    for key in adict.keys():
        if key == k:
            adict[key] = v
        elif type(adict[key]) is dict:
            anonymize(adict[key], k, v)
    return adict
            
points = api.model("Points", {
        "point": fields.Decimal,
        "start": fields.Decimal,
        "stop": fields.Decimal
        })

journey_model = api.model("journey", {
    "deviceId": fields.String("Devices ID."),
    "timestamp": fields.DateTime("Timestamp"),
    "points": fields.ClassName("Points")
})

@name_space.route("/addroute")
class JourneysList(Resource):
    @api.marshal_with(journey_model, envelope='data') 
    def get(self):
        """
        returns a list of journeys
        """
        return all_journeys, 200 
    
    @api.expect(journey_model)    
    def post(self):
        """
        Adds a new journey to the list
        """
        new_journey = anonymize(api.payload, 'deviceId',"testReplaceValue123")
        #anonym_new_journey = 
        #all_journey = json.loads(all_journeys)
        all_journeys.append(new_journey)
        return {'result': 'New journey' + str(new_journey) + ' added'}, 201
        
@name_space.route("/<int:id>")
class Journeys(Resource):
    def get(self, id):
        """
        Displays a journey's details
        """
        return{
        	"status": "Got new data"
        }
        
    def put(self, id):
        """
        Edits a selected journeys
        """
        return {
			"status": "Posted new data with id"
        }

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5003, debug=True)
