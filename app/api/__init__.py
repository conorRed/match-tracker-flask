from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import teams, errors, players, events, outcomes, auth
