import os
import click
from app import db
from app.models import Team, Player, EventOption, Outcome, User, Role
from flask_security import SQLAlchemyUserDatastore
from flask_security import hash_password
from flask.cli import with_appcontext

@click.command('seed')
@with_appcontext
def seed():
    Team.query.delete()
    EventOption.query.delete()
    Player.query.delete()
    Outcome.query.delete()

    galway = Team(name="Galway", colour="maroon")
    cork = Team(name="Cork", colour="red")
    dublin = Team(name="Dublin", colour="blue")
    tipp = Team(name="Tipperary", colour="DarkBlue")
    mon = Team(name="Monaghan", colour="CornflowerBlue")
    db.session.add_all([galway,cork,dublin, tipp, mon])
    db.session.commit()
    for p in range(1, 16): 
        db.session.add(Player(name="Player "+str(p), number=p, team=galway))
    db.session.commit()
    for p in range(1, 16): 
        db.session.add(Player(name="Player "+str(p), number=p, team=dublin))
    db.session.commit()
    for p in range(1, 16): 
        db.session.add(Player(name="Player "+str(p), number=p, team=cork))
    for p in range(1, 16): 
        db.session.add(Player(name="Player "+str(p), number=p, team=mon))
    db.session.commit()
    for p in range(1, 16): 
        db.session.add(Player(name="Player "+str(p), number=p, team=tipp))
    db.session.commit()
    eventsConfig = []
    import json
    with open("./config/events.json", "r") as read_file:
        eventsConfig = json.load(read_file)
    event_ids = []
    for event in eventsConfig:
        e = EventOption(name=event["event"])
        db.session.add(e)
        db.session.commit()
        for outcome in event["outcomes"]:
            db.session.add(Outcome(name=outcome, event_option_id=e.id))
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
