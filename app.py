# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:35:51 2019

@author: chala
"""

import json

from flask import request

from . import create_app, database
from .models import Positions

app = create_app()

#CRUD 

@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    lat= data['lat']
    lon = data['lon']
    timestamp = data['timestamp']
    gal_auth = data['gal_auth']

    database.add_instance(Positions, lat=lat, lon=lon, timestamp=timestamp, gal_auth=gal_auth)
    return json.dumps("Added"), 200

@app.route('/', methods=['GET'])
def fetch():
    positions = database.get_all(Positions)
    all_positions = []
    for position in positions:
        new_position = {
            "id": position.id,
            "lat": position.lat,
            "lon": position.lon,
            "timestamp": position.timestamp,
            "gal_auth": position.gal_auth
        }

        all_positions.append(new_position)
    return json.dumps(all_positions), 200

@app.route('/edit/<position_id>', methods=['PATCH'])
def edit(position_id):
    data = request.get_json()
    new_gal_auth = data['gal_auth'] #We only edit Galileo Authentication
    database.edit_instance(Positions, id=position_id, gal_auth=new_gal_auth)
    return json.dumps("Edited"), 200

@app.route('/remove/<position_id>', methods=['DELETE'])
def remove(position_id):
    database.delete_instance(Positions, id=position_id)
    return json.dumps("Deleted"), 200