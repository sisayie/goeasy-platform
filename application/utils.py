#from flask import json
import datetime as dtm
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