# app.py

import flask
from flask import request, jsonify, make_response
import requests
import json

import folium

import webbrowser

app = flask.Flask(__name__)

url = 'https://galileocloud.goeasyproject.eu/GEP/paib/publicstorage'
journey_id = 'ad805ce7-448f-4845-8e38-80840ae5af59' 
journey_ids = ['872cde91-9a77-4293-9e0e-f92c55f217d6', '83b2e78d-51b1-4aa6-980a-7dc38834119d']

outfile = journey_id+".html"

import pandas as pd

df = pd.DataFrame()

#==================== Fetch Journeys using Journey id ==========================
   
def getJourneys():#s_time, e_time):
    url = 'https://galileocloud.goeasyproject.eu/GEP/paib/publicstorage/journey/times?start_time=2021-02-26 09:00:00&end_time=2021-04-28 10:59:23'
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers = headers)
    journey = json.loads(response.content)
    return journey
    
def getJourney(journeyId):
    #url_str = 'https://localhost:5003/paib/publicstorage/'+str(journeyId)
    url_str = 'https://galileocloud.goeasyproject.eu/GEP/paib/publicstorage/'+journeyId
    headers = {"Accept": "application/json"}
    response = requests.get(url_str, headers = headers)
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

def getStartEndPositions(journey):
    lat_list, lon_list = getPositions(journey)
    return lat_list[0], lon_list[0], lat_list[-1], lon_list[-1]
    
def getMobiltiyTypes(journey):
    '''udb = []
    for user_defined_behaviour in journey['user_defined_behaviour']:
        udb.append(user_defined_behaviour)
    return udb'''
    
    '''journey.pop('app_defined_behaviour', None)
    journey.pop('deviceId', None)
    journey.pop('authenticity', None)
    journey.pop('timestamp', None)
    journey.pop('tpmmd', None)
    journey.pop('app_defined_behaviour', None)
    journey.pop('tpv_defined_behaviour', None)
    #journey.pop('user_defined_behaviour', None)
    journey.pop('position', None)
    for element in journey['user_defined_behaviour']:
        json.loads(element).pop('start', None)
        json.loads(element).pop('end', None)'''
    udb = journey.get('user_defined_behaviour')
    
    return jsonify(journey_id = journey.get('journeyId'), 
                   mobility_mode = [u.get('type') for u in udb], 
                   distance = [u.get('meters') for u in udb]
                    )#journey    
    
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
    
    '''
    #routes_map.save('using_folium12.html')
    routes_map.save(outfile)
    webbrowser.open(outfile, new=2)
    #return routes_map
    '''
    html_string = routes_map._repr_html_()
    return html_string


def create_entry():
    req = request.get_json()
    print(req)
    res = make_response(jsonify({"message": "OK"}), 200)
    return res

#==================== APIs ==========================
@app.route('/dash')
def index():
    #m = folium.Map()
    #html_string = m.get_root().render()
    #return html_string
    COORDINATES = (43.7623939, 7.4849723)
    myMap = folium.Map(location=COORDINATES, zoom_start=12)
    html_string = myMap._repr_html_() #.get_root().render()
    return html_string

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
    return mapping(getPositions(getJourney(id))) #flask.render_template_string(html_string) #to feed into a template
    #return 'Ok'
    
@app.route("/modes/<string:id>", methods=["get"])
def get_s_e_position(id):
    journey = getJourney(id)
    start_lat, start_lon, end_lat, end_lon = getStartEndPositions(journey)
    mobility_mode = getMobiltiyTypes(journey)
    return mobility_mode #jsonify(mobility_mode) #jsonify("start":{start_lat, start_lon}, "end": {end_lat, end_lon}, "mobility": mobility_mode)

@app.route("/modes/udb/<string:id>", methods=["get"])
def get_journey_udb(id):
    journey = getJourney(id)
    udb = journey.get('user_defined_behaviour')
    if len(udb)>1:
        return udb
    else:
        return "Journey user_defined_behaviours have one or no value"
        
@app.route("/modes/udb", methods=["get"])
def get_journeys_udb():
    journeys = getJourneys()
    udb = [j.get('user_defined_behaviour') for j in journeys]
    if len(udb)>1:
        return udb
    else:
        return "All user_defined_behaviours have one or no value"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)