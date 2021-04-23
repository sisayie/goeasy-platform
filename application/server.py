# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:37:10 2019

@author: chala
"""
#server
#from database import Database as crud #To organize db funcaions into a class
from database import *
from config import *
from model import Journey
from dashboard import *
from dash_app import *

#from werkzeug.wsgi import DispatcherMiddleware

logger = logging.getLogger(__file__)

#@api.route("/publicstorage/")
@ns.route("/publicstorage")
@ns.route("/anonimizer")
class Publicstorage(Resource):
    def get(self):
        #crud.get_all()
        result = fetch_all()
        return result
    
    @api.expect(Journey) 
    def post(self):
        response = add_new()
        return response

#@api.route("/publicstorage/<int:id>")
@ns.route("/publicstorage/<string:id>")
@ns.route("/anonimizer/<int:id>")
class Publicstorage(Resource):
    def get(self, id):
        data = fetch_one(id)
        return (data)
        
    def put(self, id):
        response = update_one(id)
        return response

    def delete(self, id):
        response = delete_one(id)
        return response

@ns.route("/publicstorage/mobilityRequest/<string:id>")
class MobilityRequest(Resource):
    def get(self, id):
        data = fetch_MM(str(id))
        print("MobilityRequest data: " + str(data))
        return (data)

@ns.route("/publicstorage/journeys/1")
class ExtractionCase1(Resource):
    def get(self):
        data = fetch_case_1()
        return (data)

@ns.route("/publicstorage/journeys/1/<string:id>")
class ExtractionCase1(Resource):
    def get(self, id):
        data = fetch_case_11(id)
        return (data)
        
@ns.route("/publicstorage/journeys/2/<string:id>")
class ExtractionCase2(Resource):
    def get(self, id):
        data = fetch_case_2(id)
        return (data)
     
@ns.route("/publicstorage/journeys/3/<string:id>")
class ExtractionCase2(Resource):
    def get(self, id):
        data = fetch_case_3()
        return (data)
        
@ns.route("/publicstorage/journey/times")
class JourneyDash(Resource):
    def get(self):
        data = fetch_time_range()
        return (data)

@ns.route("/publicstorage/journey/locations")
class JourneyDash1(Resource):
    def get(self):
        data = fetch_space_range()
        return (data)
        
#====== dashboard APIs =================
'''@ns.route("/dash", methods=["get"])
class Route(Resource):
    def get(self):
        return url(http://localhost:5004/dash)

@ns.route("/dash/journey/<string:id>", methods=["get"])
class Route(Resource):
    def get(self, id):
        journey = fetch_one(id)#getJourney(id)
        return (journey)

@ns.route("/dash/positions/<string:id>", methods=["get"])
class Positions(Resource):
    def get(self, id):
        #journey = fetch_one(id) #getJourney(id)
        positions = fetch_positions(id) #getPositions(journey)
        return positions
        #positions_dict = json.loads(positions)
        #lat = positions['lat']
        #return lat

@ns.route("/dash/map/<string:id>", methods = ["get"])
class Map(Resource):
    def get(self, id):
        #TODO: show for multiple journeys
        #for j in journey_ids:
        #    display(mapping(getPositions(getJourney(j))))
        position = fetch_positions(id)
        positions = getPositions(position)
        return mapping(positions) #(getPositions(getJourney(id)))'''
#================================================
'''@ns.route("/dash/time", methods = ["get"])
class Dash(Resource):
    def get(self):
        app = gep_dash()
        return app'''

if __name__ == '__main__':
    logger.debug("Starting TPMMD threads !!!!")
    startTPMMD()
    logger.debug("This is just befor running app.run() !!!!")
    app.run(host='0.0.0.0', port=5003, debug=True)
    '''dash_app = gep_dash()
    application = DispatcherMiddleware(app, {'/dash': dash_app.server})
    
    run(host='0.0.0.0', port=5003, debug=True)'''

