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
name_space = api.namespace('anonymizer', description='Measurements for LBS')

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

all_journeys2 = [
    {
        "common": { 
            "deviceId": 123445,
            "sessionID": 456789,
            "sourceApp": "ApesMobility"
        },  
        "positions": [
            {"lat":43.4541819, "lon":11.8679015, "time":1570390750300, "authenticity": 1},
            {"lat":43.4541711, "lon":11.8679564, "time":1570390752305, "authenticity": 0},
            {"lat":43.4542047, "lon":11.8679665, "time":1570390757171, "authenticity": 1},
            {"lat":43.4541974, "lon":11.8679352, "time":1570390770173, "authenticity": 1},
            {"lat":43.4541987, "lon":11.8679016, "time":1570390806175, "authenticity": -1},
            {"lat":43.4541867, "lon":11.8679515, "time":1570390812154, "authenticity": -1},
            {"lat":43.4541729, "lon":11.8679809, "time":1570390813172, "authenticity": -1},
            {"lat":43.4541361, "lon":11.8680513, "time":1570390815164, "authenticity": -1},
            {"lat":43.4541128, "lon":11.8680922, "time":1570390816218, "authenticity": -1}
        ],
        "tpv_defined_behaviour":[
            {"start_time":1570390750300, "end_time":1570391081178, "mode": "walk"},
            {"start_time":1570391082220, "end_time":1570391333188, "mode": "drive"}
        ],
        "app_defined_behaviour":[
            {"start_time":1570390750300, "end_time":1570391081178, "mode": "walk"},
            {"start_time":1570391082220, "end_time":1570391333188, "mode": "drive"}
        ],
        "user_defined_behaviour":[
            {"start_time":1570390750300, "end_time":1570391081178, "mode": "walk"},
            {"start_time":1570391082220, "end_time":1570391333188, "mode": "drive"}
        ],
        "sensordata":[
            {"data":5.0,"name":"proximity","time":1570390749231},
            {"data":{"x":-2.0,"y":0.0,"z":8.0},"name":"accellerometer","time":1570390749233},
            {"data":{"x":15.363352,"y":-29.060678,"z":-69.23764},"name":"magnetometer","time":1570390749320},
            {"data":{"x":22.490746,"y":-43.714897,"z":-103.77774},"name":"magnetometer","time":1570390750221},
            {"data":{"x":26.39621,"y":-51.00329,"z":-121.21308},"name":"magnetometer","time":1570390751287},
            {"data":{"x":29.422604,"y":-56.587624,"z":-134.03339},"name":"magnetometer","time":1570390753288},
            {"data":{"x":35.883057,"y":-46.446068,"z":-138.07208},"name":"magnetometer","time":1570390865175},
            {"data":{"x":36.672806,"y":-35.711693,"z":-137.7186},"name":"magnetometer","time":1570390867176},
            {"data":{"x":27.774622,"y":-25.288143,"z":-139.21454},"name":"magnetometer","time":1570390892173},
            {...}
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

        
positions = api.model("Positions", {
        "lat": fields.Float,
        "lon": fields.Float,
        "time": fields.Float,
        "authenticity": fields.Integer
        })

common = api.model("Common", {
        "tockenID": fields.String,
        "sessionID": fields.String,
        "sourceApp": fields.String
        })

behaviour = api.model("Behaviour_Description", {
        "strt_time": fields.Float,
        "end_time": fields.Float,
        "mode": fields.String
        })
        
#journey_model = api.model("journey", {
#    "deviceId": fields.String("Devices ID."),
#    "timestamp": fields.DateTime("Timestamp"),
#    "points": fields.ClassName("Points")
#})

journey_model = api.model("trip", {
    "common": fields.Nested(common),
    "positions": fields.List(fields.Nested(positions)),
    "tpv_defined_behaviour": fields.List(fields.Nested(behaviour)),
    "app_defined_behaviour": fields.List(fields.Nested(behaviour)),
    "user_defined_behaviour": fields.List(fields.Nested(behaviour)),
    "sensordata": fields.String    
})

@name_space.route("/publicstorage")
@name_space.route("/encryptedstorage")
class JourneysList(Resource):
    @api.marshal_with(journey_model, envelope='data') 
    def get(self):
        """
        returns a list of journeys
        """
        return all_journeys2, 200 
    
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
        
#@name_space.route("/<int:id>")
#class Journeys(Resource):
#    def get(self, id):
#        """
#        Displays a journey's details
#        """
#        return{
#        	"status": "Got new data"
#        }
#        
#    def put(self, id):
#        """
#        Edits a selected journeys
#        """
#        return {
#			"status": "Posted new data with id"
#        }

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5003, debug=True)
