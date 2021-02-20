
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
