from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from app.models import Event, EventOption, Game, Outcome, Team


class OutcomeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Outcome

class EventOptionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EventOption
    outcomes = Nested(OutcomeSchema, many=True)


class TeamSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Team

class EventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Event
    event_option = Nested(EventOptionSchema)
    outcome = Nested(OutcomeSchema)
    team = Nested(TeamSchema)

class GameSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Game
    events = Nested(EventSchema, many=True)
    home_team = Nested(TeamSchema)
    away_team = Nested(TeamSchema)
