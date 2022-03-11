from flask import jsonify, request, url_for

from app import db
from app.api import bp
from app.api.errors import error_response
from app.models import Event
from marshmallow import Schema, fields

class EventCreationSchema(Schema):
    name = fields.Str(required=True)
    game_id = fields.Int(required=True)
    timestamp = fields.Str(require=True)
    pitchzone  = fields.Str(required=True)
    event_option_id = fields.Int(required=True)
    outcome_id = fields.Int(required=True)

event_creation_schema = EventCreationSchema()

@bp.route('/events', methods=['POST'])
def create_event():
    data = request.get_json() or {}
    errors = event_creation_schema.validate(data)
    if errors:
        return error_response(400, errors)
    e = Event()
    e.from_dict(data)
    print(data)
    db.session.add(e)
    db.session.commit()
    response = jsonify(e.to_dict())
    response.status_code = 201
    return response
