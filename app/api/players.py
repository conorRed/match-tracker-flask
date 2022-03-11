from app.api import bp
from app.models import Player
from app import db
from flask import jsonify
from flask import request
from flask import url_for
from app.api.errors import error_response

@bp.route('/players/<int:id>', methods=['GET'])
def get_player(id):
    return jsonify(Player.query.filter_by(team_id=id).to_dict())

@bp.route('/player', methods=['POST'])
def create_player():
    data = request.get_json() or {}
    if 'team_id' not in data:
        return error_response(400, "Bad request Add the team Id")
    if 'name' not in data or 'number' not in data:
        return error_response(400, "Bad request missing fields")
    p = Player()
    p.from_dict(data)
    db.session.add(p)
    db.session.commit()
    response = jsonify(p.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_player', id=p.id)
    return response

@bp.route('/players', methods=['POST'])
def create_players():
    data = request.get_json() or {}
    team_id = data[0]['team_id']
    for player in data:
        if 'team_id' not in player:
            return error_response(400, "Bad request Add the team Id")
        if 'name' not in player or 'number' not in player:
            return error_response(400, "Bad request missing fields")
        p = Player()
        p.from_dict(player)
        db.session.add(p)
        db.session.commit()
    response = jsonify("players created")
    response.status_code = 201
    return response
