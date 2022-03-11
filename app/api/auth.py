from flask import jsonify, request, url_for
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required,
                                set_access_cookies)

from app import db
from app.api import bp
from app.api.errors import error_response
from app.models import Role, User

from flask_security import SQLAlchemyUserDatastore


@bp.route('/signup', methods=['POST'])
def create_user():
    user = User()
    data = request.get_json() or {}
    if 'email' not in data:
        return error_response(400, "Bad request Add the team Id")
    if 'password' not in data:
        return error_response(400, "Bad request missing fields")
    user.from_dict(data)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    user_datastore.create_user(email=data['email'], password=data["password"])
    access_token = create_access_token(user.email)
    db.session.commit()
    response = jsonify(access_token=access_token)
    response.status_code = 201
    return response

@bp.route('/login', methods=['POST'])
def login():
    user = User()
    data = request.get_json() or {}
    if 'email' not in data:
        return error_response(400, "Bad request Add the team Id")
    if 'password' not in data:
        return error_response(400, "Bad request missing fields")
    user.from_dict(data)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    if user_datastore.find_user(email=user.email) is not None:
        if user.verify_and_update_password(data["password"]):
            access_token = create_access_token(identity=user.email)
            response = jsonify(access_token=access_token)
            response.status_code = 201
        else:
            response = jsonify(message="Forbidden")
            response.status_code = 401
    else:
        return error_response(404, "User doesn't exist")
    return response

@bp.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)

