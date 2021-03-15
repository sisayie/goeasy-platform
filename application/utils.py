#from flask import json
import datetime as dtm
from datetime import datetime

'''
response = current_app.response_class(
    json.dumps(new_sorted, sort_keys=False),
    mimetype=current_app.config['JSONIFY_MIMETYPE'])
'''
def date_format(value: str) -> int:
    if str.isdigit(value):
        return value
    else:
        dt = dtm.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return int(dt.timestamp())
        
def date_format1(value: str) -> int:
    if str.isdigit(value):
        return value
    else:
        dt = dtm.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S%z')
        return int(dt.timestamp())
    
def date_format2(value: str) -> int:
    d = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f%z')
    dt = dtm.datetime.strptime(d, '%Y-%m-%dT%H:%M:%S.%f%z')
    return int(dt.timestamp())