import os
import click
from app import db
from app.models import Team, Player, EventOption, Outcome, User, Role, Game
from flask_security import SQLAlchemyUserDatastore
from flask_security import hash_password
from flask.cli import with_appcontext

@click.command('seed')
@with_appcontext
def seed():
    eventsConfig = []
    import json
    with open("./config/events.json", "r") as read_file:
        eventsConfig = json.load(read_file)
    event_ids = []
    for team in eventsConfig["teams"]:
        t = Team(name=team["name"], colour=team["colour"])
        db.session.add(t)
        for p in range(1, 16): 
            db.session.add(Player(name="Player "+str(p), number=p, team=t))
        db.session.commit()

    for outcome in eventsConfig["outcomes"]:
        db.session.add(Outcome(name=outcome["name"]))
    db.session.commit()   
    for event in eventsConfig["event_options"]:
        e = EventOption(name=event["name"])
        for outcome in event["outcomes"]:
            o = db.session.query(Outcome).filter_by(name=outcome).first()
            e.outcomes.append(o)
        db.session.add(e)
        db.session.commit()   
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    user_datastore.find_or_create_role(
        name="admin",
        permissions={"admin-read", "admin-write", "user-read", "user-write"},
    )
    if not user_datastore.find_user(email="admin@me.com"):
        user_datastore.create_user(
            email="admin@me.com", password=hash_password("password"), roles=["admin"]
        )
    db.session.commit()

def register_seed(app):
    app.cli.add_command(seed)
