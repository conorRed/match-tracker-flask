from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    # Jsonify will set it to 200 so need to manually set status code
    response = jsonify(payload)
    response.status_code = status_code
    return response