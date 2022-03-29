from flask import jsonify, request
from flask_jwt_extended import current_user, get_jwt_identity, jwt_required

from app import db, jwt
from app.api import bp
from app.api.errors import error_response
from app.api.schemes import GameSchema
from app.models import Game, User
from marshmallow import Schema, fields


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(email=identity).one_or_none()

@bp.route('/games', methods=['GET'])
@jwt_required()
def get_games():
    if current_user is None:
        return error_response(401, "Could not find user for provided token")
    game_schema = GameSchema()
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    data = Game.to_collection_with_scheme(current_user.games, game_schema,page, per_page, 'api.get_games', id=id)
    return jsonify(data)

@bp.route('/games/<int:id>', methods=['GET'])
@jwt_required()
def get_game(id):
    game_schema = GameSchema()
    return game_schema.dump(Game.query.get_or_404(id))
    
class GameCreationSchema(Schema):
    name = fields.Str(required=True)
    home_team_id = fields.Int(required=True)
    away_team_id = fields.Int(required=True)

game_creation_schema = GameCreationSchema()
@bp.route('/games', methods=['POST'])
@jwt_required()
def create_game():
    if current_user is None:
        return error_response(401, "Could not find user for provided token")
    data = request.get_json() or {}
    errors = game_creation_schema.validate(data)
    if errors:
        return error_response(400, errors)
    g = Game()
    from datetime import date
    data["user_id"] = current_user.id
    g.from_dict(data)
    print(data)
    try: 
        db.session.add(g)
        db.session.commit()
    except Exception as error:
        print("ERROR")
        return error_response(500, str(error))
    response = jsonify(g.to_dict())
    response.status_code = 201
    return response

