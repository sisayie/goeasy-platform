# app.py

import flask
from flask import request, jsonify, make_response
import requests
import json

import folium

import webbrowser

app = flask.Flask(__name__)

url = 'https://galileocloud.goeasyproject.eu/GEP/paib/publicstorage'
journey_id = '872cde91-9a77-4293-9e0e-f92c55f217d6' #'83b2e78d-51b1-4aa6-980a-7dc38834119d'
journey_ids = ['872cde91-9a77-4293-9e0e-f92c55f217d6', '83b2e78d-51b1-4aa6-980a-7dc38834119d']

outfile = journey_id+".html"

import pandas as pd

df = pd.DataFrame()

#==================== Fetch Journeys using Journey id ==========================
def getJourney(journeyId):
    url = 'https://galileocloud.goeasyproject.eu/GEP/paib/publicstorage/'+journeyId
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers = headers)
    journey = json.loads(response.content)
    return journey

#==================== Fetch Positions from Journey ==========================
def getPositions(journey):
    #print(json_data)
    latitude_list = []
    longitude_list = []
    for position in journey['positions']: # TODO: This is for one route. For multiple routes, use "for route in json_data: for position in route: ..."
        #print(position)
        latitude_list.append(position['lat'])
        longitude_list.append(position['lon'])
    return latitude_list, longitude_list

def get_route():
    #create a map
    routes_map = folium.Map(prefer_canvas=True)

    lats, lons = getPositions(getJourney(journey_id))

    def plotDot(point):
        folium.CircleMarker(location=[point.latitude, point.longitude],
                            radius=2,
                            weight=10).add_to(routes_map)
    data = pd.DataFrame(zip(lats,lons), columns = ['latitude', 'longitude'])
    data.apply(plotDot, axis = 1)

    #Set the zoom
    routes_map.fit_bounds(routes_map.get_bounds())
        
    display(routes_map) # Or save it to file using routes_map.save('using_folium12.html')

def mapping(positions):
    routes_map = folium.Map(prefer_canvas=True)
    lats, lons = positions #getPositions(getJourney(journey_id))
    def plotDot(point):
        '''input: series that contains a numeric latitude and a numeric longitude
        this function creates a CircleMarker and adds it to routes_map'''
        folium.CircleMarker(location=[point.latitude, point.longitude],
                            radius=2,
                            weight=10).add_to(routes_map)
    data = pd.DataFrame(zip(lats,lons), columns = ['latitude', 'longitude'])
    data.apply(plotDot, axis = 1)

    #Set the zoom
    routes_map.fit_bounds(routes_map.get_bounds())
    
    #routes_map.save('using_folium12.html')
    routes_map.save(outfile)
    webbrowser.open(outfile, new=2)
    #return routes_map

def create_entry():
    req = request.get_json()
    print(req)
    res = make_response(jsonify({"message": "OK"}), 200)
    return res

#==================== APIs ==========================
@app.route('/dash')
def index():
    return 'GEP Dashboard'

@app.route("/journey/<string:id>", methods=["get"])
def get_routes(id):
    return getJourney(id)
    #return 'OK'

@app.route("/positions/<string:id>", methods=["get"])
def get_positions(id):
    #return getPositions(getJourney(id))
    #return 'OK'
    journey = getJourney(id)
    '''lat, lon = getPositions(journey)
    p = {}
    for i in range len(lat):
        p['lat'] = lat[i]
        p['lon'] = lon[i]'''
    '''return {"lat":lat, "lon": lon}'''
    #positions = getPositions(journey)
    #return json.dumps(positions)
    '''positions = {}'''
    #pos = list(zip(lat, lon))
    #positions[id] = json.dumps(pos) #json string
    '''positions['journey_id'] = id'''
    #position_lat_lon = list(zip(lat, lon))
    #positions['latitude'] = lat
    #positions['longitude'] = lon
    '''positions['positions'] = p #position_lat_lon'''
    
    journey.pop('app_defined_behaviour', None)
    journey.pop('deviceId', None)
    journey.pop('authenticity', None)
    journey.pop('timestamp', None)
    journey.pop('tpmmd', None)
    journey.pop('tpv_defined_behaviour', None)
    journey.pop('user_defined_behaviour', None)
    for element in journey['positions']:
        element.pop('timestamp', None)
        element.pop('authenticity', None)

    return journey


@app.route("/routes/<string:id>", methods = ["get"])
def get_route(id):
    #TODO: show for multiple journeys
    '''for j in journey_ids:
        display(mapping(getPositions(getJourney(j))))'''
    #display(mapping(getPositions(getJourney(id))))
    mapping(getPositions(getJourney(id)))
    return 'Ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)