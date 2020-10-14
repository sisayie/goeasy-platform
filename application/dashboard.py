import requests
import json

import folium

import pandas as pd

from database import *

df = pd.DataFrame()

#==================== Fetch Journeys using Journey id ==========================
def getJourney(journeyId):
    journey = fetch_one(journeyId) #Journey.query.filter_by(journeyId =str(journeyId)).first()
    return journey

#==================== Fetch Positions from Journey ==========================
def getPositions(journeyId):
    positions = fetch_position(journeyId)
    return positions
    '''latitude_list = []
    longitude_list = []
    
    for position in positions: # TODO: This is for one route. For multiple routes, use "for route in json_data: for position in route: ..."   
        latitude_list.append(position['lat'])
        longitude_list.append(position['lon'])
    return latitude_list, longitude_list
    '''
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
    
    return routes_map.render()
    
def create_entry():
    req = request.get_json()
    print(req)
    res = make_response(jsonify({"message": "OK"}), 200)
    return res