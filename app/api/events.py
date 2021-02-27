
from app.api import bp
from app.models import Event
from app import db
from flask import jsonify
from flask import request
from flask import url_for
from app.api.errors import error_response


@bp.route('/events', methods=['GET'])
def get_events():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Event.to_collection_dict(Event.query, page, per_page, 'api.get_events')
    return jsonify(data)

@bp.route('/events/<int:id>', methods=['GET'])
def get_event_by_id(id):
    return jsonify(Event.query.get_or_404(id).to_dict())

@bp.route('/events/<int:id>/outcomes', methods=['GET'])
def get_event_outcomes(id):
    event = Event.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Event.to_collection_dict(event.outcomes, page, per_page, 'api.get_event_outcomes', id=id)
    return jsonify(data)

@bp.route('/events', methods=['POST'])
def create_event():
    data = request.get_json() or {}
    if 'name' not in data:
        return error_response(400, "Bad request")
    e = Event()
    e.from_dict(data)
    db.session.add(e)
    db.session.commit()
    response = jsonify(e.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_events', id=e.id)
    return response