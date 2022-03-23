import os
from sqlalchemy import MetaData
from flask import Flask, json
from flask import jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_security import Security, SQLAlchemyUserDatastore
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


migrate = Migrate()


jwt = JWTManager()
convention = {
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

def create_app(config=Config):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    CORS(app)
    
    app.config.from_object(config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    jwt.init_app(app)
    from app.models import Team, Player, Event, Outcome, User, Role, Game
    migrate.init_app(app, db, render_as_batch=True)
    from app.api import bp as api_bp
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    app.register_blueprint(api_bp, url_prefix='/api')

    return app
