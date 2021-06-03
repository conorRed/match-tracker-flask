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
    data = Team.to_collection_dict(team.players, page, per_page, 'api.get_players', id=id)
    return data

@bp.route('/teams', methods=['GET'])
def get_teams():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    data = Team.to_collection_dict(Team.query, page, per_page, 'api.get_teams')
    return jsonify(data)
    
@bp.route('/teams', methods=['POST'])
def create_team():
    data = request.get_json() or {}
    if 'name' not in data:
        return error_response(400, "Bad request")
    t = Team()
    t.from_dict(data)
    try: 
        db.session.add(t)
        db.session.commit()
    except Exception as error:
        response = jsonify(str(error.orig) + "for parameters " + str(error.params))
        response.status_code = 500
        return response
    response = jsonify(t.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_team', id=t.id)
    return response


@bp.route('/teams/<int:id>', methods=['PUT'])
def update_team(id):
    data = request.get_json() or {}
    team = Team.query.get_or_404(id)
    if 'name' not in data:
        return error_response(400, "Bad request")
    team.from_dict(data)
    db.session.commit()
    response = jsonify(team.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_team', id=id)
    return response