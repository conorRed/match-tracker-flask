import os
from flask import Flask, json
from flask import jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate(compare_type=True)

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
    migrate.init_app(app, db, compare_type=True)
    from app.models import Team, Player, Event, Outcome
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
