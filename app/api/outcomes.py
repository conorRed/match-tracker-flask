
from app.api import bp
from app.models import Outcome
from app import db
from flask import jsonify
from flask import request
from flask import url_for
from app.api.errors import error_response


@bp.route('/outcomes', methods=['GET'])
def get_outcomes():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Outcome.to_collection_dict(Outcome.query, page, per_page, 'api.get_outcomes')
    return jsonify(data)

@bp.route('/outcome/<int:id>', methods=['GET'])
def get_outcome(id):
    return jsonify(Outcome.query.get_or_404(id).to_dict())

@bp.route('/outcomes', methods=['POST'])
def create_outcome():
    data = request.get_json() or {}
    if 'name' not in data or 'event_id' not in data:
        return error_response(400, "Bad request")
    o = Outcome()
    o.from_dict(data)
    db.session.add(o)
    db.session.commit()
    response = jsonify(o.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_outcome', id=o.id)
    return response
