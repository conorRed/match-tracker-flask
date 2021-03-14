import os
import click
from app import db
from app.models import Team, Player, Event, Outcome
from flask.cli import with_appcontext

@click.command('seed')
@with_appcontext
def seed():
    Team.query.delete()
    Event.query.delete()
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
        e = Event(name=event["event"])
        db.session.add(e)
        db.session.commit()
        for outcome in event["outcomes"]:
            db.session.add(Outcome(name=outcome, event_id=e.id))
            db.session.commit()   


def register_seed(app):
    app.cli.add_command(seed)
