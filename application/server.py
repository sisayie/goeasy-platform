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

logger = logging.getLogger(__file__)

#@api.route("/publicstorage/")
@ns.route("/publicstorage")
@ns.route("/anonimizer")
class Publicstorage(Resource):
    def get(self):
        #crud.get_all()
        all_data = fetch_all()
        
        result = journeys_schema.jsonify(all_data)
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

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    logger.debug("Starting TPMMD threads !!!!")
    startTPMMD()
    logger.debug("This is just befor running app.run() !!!!")
    app.run(host='0.0.0.0', port=5003, debug=True)

