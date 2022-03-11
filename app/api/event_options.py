from flask import jsonify, request, url_for

from app import db
from app.api import bp
from app.api.errors import error_response
from app.api.schemes import EventOptionSchema
from app.models import EventOption


@bp.route('/event_options/<int:id>', methods=['GET'])
def get_event_by_id(id):
    event_option_schema = EventOptionSchema()
    event_option = EventOption.query.get_or_404(id)
    return event_option_schema.dump(event_option)

@bp.route('/event_options', methods=['GET'])
def get_events():
    event_option_schema = EventOptionSchema()
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = EventOption.to_collection_with_scheme(EventOption.query,event_option_schema, page, per_page, 'api.get_events', id=id) 
    return jsonify(data)

@bp.route('/event_options/<int:id>/outcomes', methods=['GET'])
def get_event_outcomes(id):
    event_option_schema = EventOptionSchema()
    event_option = EventOption.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = EventOption.to_collection_with_scheme(event_option.outcomes, event_option_schema, page, per_page, 'api.get_event_outcomes', id=id)
    return jsonify(data)
