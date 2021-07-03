from app.api import bp
from app import db
from flask import jsonify
from flask import request
from flask import url_for
from app.api.errors import error_response
from flask_security import SQLAlchemyUserDatastore
from app.models import User, Role
from flask_jwt_extended import create_access_token


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
    if user_datastore.get_user(user.email) is not None:
        if user.authenticate(data["password"]):
            access_token = create_access_token(user.email)
            response = jsonify(access_token=access_token)
            response.status_code = 201
        else:
            response = jsonify(message="Forbidden")
            response.status_code = 401
    else:
        response = jsonify(message="User doesn't exist")
        response.status_code = 404
    return response



