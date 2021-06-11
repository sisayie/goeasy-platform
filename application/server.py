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
#from dashboard import *
#from dash_app import *
from flask import request, redirect

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from dash import Dash
from dash_utilities import *
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

#from dash_funcs import dash_funcs

#from werkzeug.wsgi import DispatcherMiddleware

logger = logging.getLogger(__file__)

@api.documentation
def swagger_ui():
    return apidoc.ui_for(api)
  
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
        try:
            response = add_new()
            return response, 200
        except (ValidationError):
            raise SchemaValidationError
        '''except UniqueViolation:
            raise AlreadyExistsError'''
        '''except Exception as e:
            raise InternalServerError'''

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

@ns.route("/monitor")
class JourneyDash2(Resource):
    def get(self):
        #data = fetch_space_range()
        #return ("data")
        return redirect("http://localhost:8008")
      

      
'''
@ns.route("/dashboard1")
class JourneyDashboard(Resource):
    def get(self):
        #return flask.redirect("http://localhost:8008") #("http://localhost:8009")
        return ("Test text") 
'''        
#####========================


'''
import dash_bootstrap_components as dbc

my_dash_app = Dash(__name__, 
                    server=server, 
                    external_stylesheets=[dbc.themes.BOOTSTRAP], 
                    prevent_initial_callbacks=True, 
                    url_base_pathname='/paib/dashboard/',
                    title='GOEASY Dashboard',
                    update_title='Loading...',
                    suppress_callback_exceptions=True
                   )

dash_app = dash_funcs(my_dash_app)
'''

'''
@server.route('/dashboard')
def render_dashboard():
    return flask.redirect('/paib/dash')

#app = DispatcherMiddleware(server, {
#    '/paib/dash': dash_app1.server,
#})
'''

#====== dashboard APIs =================
'''
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
        positions = fetch_positions(id)
        #positions = getPositions(position)
        return mapping(positions) #(getPositions(getJourney(id)))
'''

'''
def get_path(app):
    app.layout = html.Div(
        [
            html.H1('Routes for journey'),
            html.Div(id="message", children='Select start and end date to get journeys during the date range'),
            dbc.Input(id="journey_id", placeholder="Enter Journey ID ...", type='text'),
            html.Div(id='path_url', style={'display': 'none'}),
            html.Iframe(id="route1", src='http://localhost:5004/routes/27c72c36-09c4-4d3b-8615-dab8b55d8d47', width='100%', height='600'),
        ]
    )
    @app.callback(
            Output("message", "children"), 
            [Input("journey_id", "value")])
    def output_text(value):
        return value
    return app
    
@ns.route("/dash/test", methods=["get"])
class Test(Resource):
    def get(self):
        return get_path(dash_app)
'''        


if __name__ == '__main__':
    db.create_all()
    logger.debug("Starting TPMMD threads !!!!")
    startTPMMD()
    logger.debug("This is just befor running app.run() !!!!")
    server.run(host='0.0.0.0', port=5003, debug=False)

