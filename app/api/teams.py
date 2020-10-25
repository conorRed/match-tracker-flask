from app.api import bp
from app.models import Team
from app import db
from flask import jsonify
from flask import request
from flask import url_for
from app.api.errors import error_response


@bp.route('/teams/<int:id>', methods=['GET'])
def get_team(id):
    return jsonify(Team.query.get_or_404(id).to_dict())

@bp.route('/teams/<int:id>/players', methods=['GET'])
def get_players(id):
    team = Team.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    data = Team.to_collection_dict(team.players, page, per_page, 'api.get_players')
    return data

@bp.route('/teams', methods=['GET'])
def get_teams():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Team.to_collection_dict(Team.query, page, per_page, 'api.get_teams')
    return jsonify(data)


@bp.route('/teams', methods=['POST'])
def create_team():
    data = request.get_json() or {}
    if 'name' not in data:
        return error_response(400, "Bad request")
    t = Team()
    t.from_dict(data)
    db.session.add(t)
    db.session.commit()
    response = jsonify(t.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_team', id=t.id)
    return response