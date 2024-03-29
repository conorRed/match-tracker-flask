from app import create_app, db
import tempfile
import os
import pytest
from app.models import Team, Event, Outcome, Player, User, Role, Game
from config import Config
from flask_jwt_extended import create_access_token
from flask_security.utils import get_hmac
from flask_security import SQLAlchemyUserDatastore

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    JWT_SECRET_KEY = "test secret"
    SECURITY_PASSWORD_SALT='salt'

app = create_app(TestConfig)

with app.app_context():
    db.create_all()

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def get_token():
    from flask_jwt_extended import create_access_token
    with app.test_request_context():
        access_token = create_access_token("username")

    return access_token

def make_headers(jwt):
    return {"Authorization": "Bearer {}".format(jwt)}

@pytest.fixture(scope="function")
def access_token_for_email():
    def _create_token(email):
        return create_access_token(email)

    yield _create_token

@pytest.fixture(scope="class")
def add_verified_user():
    with app.app_context():
            e = "username"
            password = "password"
            user_datastore = SQLAlchemyUserDatastore(db, User, Role)
            user = User(email=e, password=password)
            user_datastore.create_user(email=e, password=password)
            user_datastore.commit()
            yield user
            user_datastore.delete_user(user_datastore.find_user(email=user.email))
            user_datastore.commit()


@pytest.fixture(scope="function")
def add_user():
    with app.app_context():
            removals = []
            user_datastore = SQLAlchemyUserDatastore(db, User, Role)
            def _add_user(e, p):
                password = get_hmac(p)
                user = User(email=e, password=password)
                user_datastore.create_user(email=e, password=password)
                return user

            yield _add_user

@pytest.fixture(scope="function")
def add_team():
    with app.app_context():
            removals = []
            def _add_team(n, c):
                team_added = Team(name=n, colour=c)
                removals.append(team_added)
                db.session.add(team_added)
                db.session.commit()
                return team_added

            yield _add_team

            db.session.delete(removals[0])
            db.session.commit()

@pytest.fixture(scope="function")
def add_game():
    with app.app_context():
            removals = []
            def _add_game(n, t):
                game_added = Game(name=n, timestamp=t)
                removals.append(game_added)
                db.session.add(game_added)
                db.session.commit()
                return game_added

            yield _add_game

            db.session.delete(removals[0])
            db.session.commit()

@pytest.fixture(scope="function")
def add_player():
    with app.app_context():
            removals = []
            def _add_player(team_id, n, no):
                # now add outcome to that event
                player = Player(name=n, number=no, team_id=team_id)
                db.session.add(player)
                db.session.commit()
                removals.append(player)
                return player

            yield _add_player

            for removal in removals:
                db.session.delete(removal)
                db.session.commit()

@pytest.fixture(scope="function")
def add_event():
    with app.app_context():
            removals = []
            def _add_event(n):
                event = Event(name=n)
                removals.append(event)
                db.session.add(event)
                db.session.commit()
                return event

            yield _add_event

            db.session.delete(removals[0])
            db.session.commit()

@pytest.fixture(scope="function")
def add_outcome():
    with app.app_context():
            removals = []
            def _add_outcome(event_name, n):
                # add mock event first
                event = Event(name=event_name)
                db.session.add(event)
                db.session.commit()
                removals.append(event)

                # now add outcome to that event
                outcome = Outcome(name=n, event_id=event.id)
                db.session.add(outcome)
                db.session.commit()
                return outcome

            yield _add_outcome

            db.session.delete(removals[0])
            db.session.commit()
