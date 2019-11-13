import datetime
import os
import json

import requests

from flask import Flask, render_template, redirect, url_for

from models import Journeys
from db import db_session

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def journey():
    if request.is_json: 
        data = request.get_json()
        journey = Journeys(attributes)
        db_session.add(journey)
        db_session.commit()
        return redirect(url_for('success'))

@app.route("/success")
def success():
    return "Data sent successfully!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
