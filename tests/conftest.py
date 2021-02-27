from app import create_app, db
import tempfile
import os
import pytest
from app.models import Team, Event, Outcome
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

app = create_app(TestConfig)

with app.app_context():
    db.create_all()

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

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
