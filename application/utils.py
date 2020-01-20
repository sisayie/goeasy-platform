from flask import json

response = current_app.response_class(
    json.dumps(new_sorted, sort_keys=False),
    mimetype=current_app.config['JSONIFY_MIMETYPE'])