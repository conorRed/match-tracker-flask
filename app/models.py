from flask_sqlalchemy import SQLAlchemy
from flask_security import (
    Security,
    SQLAlchemyUserDatastore,
    hash_password,
)
from flask_security.models import fsqla_v2 as fsqla
from app import db
from app import metadata
from flask import url_for


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_with_scheme(query, scheme, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items' : [scheme.dump(item) for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs)
            }
        }
        return data
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items' : [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs)
            }
        }
        return data

fsqla.FsModels.set_db_info(db)

class Role(db.Model, fsqla.FsRoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    def to_dict(self):
        data = {
            "name" :      self.email,
            "description" : self.active,
        }
        return data
    
    def from_dict(self, data):
        for field in ["name"]:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return '<Role %r>' % (self.name)

class User(db.Model, fsqla.FsUserMixin, PaginatedAPIMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    games = db.relationship('Game', backref='game', lazy='dynamic')

    def to_dict(self):
        data = {
            "id": self.id,
            "email" :      self.email,
            "active" : self.active,
            "create_time": self.create_datetime
        }
        return data
    
    def from_dict(self, data):
        for field in ["email", "password"]:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return '<User %r>' % (self.email)

class Game(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    events = db.relationship('Event', backref='game', lazy='dynamic')
    home_team = db.relationship('Team', lazy='select', foreign_keys=[home_team_id])
    away_team = db.relationship('Team', foreign_keys=[away_team_id])

    def __repr__(self):
        return '<Game %r>' % (self.name)

    def to_dict(self):
        data = {
            "id" : self.id,
            "name" : self.name,
            "user_id" : self.user_id, 
            "home_team": self.home_team_id,
        }
        return data

    def from_dict(self, data):
        for field in ["name", "timestamp", "user_id", "home_team_id", "away_team_id"]:
            if field in data:
                setattr(self, field, data[field])

class Team(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    colour = db.Column(db.String(50), unique=False)
    players = db.relationship('Player', backref='team', lazy='dynamic')

    def __repr__(self):
        return '<Team %r>' % (self.name)

    def to_dict(self):
        data = {
            "id" : self.id,
            "name" : self.name,
            "colour" : self.colour
        }
        return data

    def from_dict(self, data):
        for field in ["name", "colour"]:
            if field in data:
                setattr(self, field, data[field])

class Player(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    number = db.Column(db.Integer) 
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def to_dict(self):
        data = {
            "id" :      self.id,
            "name" :   self.name,
            "number" : self.number
        }
        return data
    
    def from_dict(self, data):
        for field in ["name", "number", "team_id"]:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return '<Player %r>' % (self.name)

association_table = db.Table('outcome_to_event_option', 
    db.Column('outcome_id', db.ForeignKey('outcome.id')),
    db.Column('event_option_id', db.ForeignKey('event_option.id'))
)
class Outcome(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return '<Outcome %r>' % (self.name)

    def to_dict(self):
        data = {
            "id":         self.id,
            "name":       self.name,
            "event_id":   self.event_option_id
        }
        return data
        
    def from_dict(self, data):
        for field in ["name", "event_option_id"]:
            if field in data:
                setattr(self, field, data[field])

class EventOption(PaginatedAPIMixin, db.Model):
    __tablename__ = 'event_option'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    outcomes = db.relationship('Outcome', secondary=association_table, backref="event_options")
    def __repr__(self):
        return '<EventOutcome %r>' % (self.name)

    def to_dict(self):
        data = {
            "id" : self.id,
            "name" : self.name,
            "outcomes" : self.outcomes
        }
        return data
    
    def from_dict(self, data):
        for field in ["name", "game_id"]:
            if field in data:
                setattr(self, field, data[field])


class Event(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    event_option_id = db.Column(db.Integer, db.ForeignKey('event_option.id'))
    outcome_id = db.Column(db.Integer, db.ForeignKey('outcome.id'))
    timestamp = db.Column(db.String(10), unique=False)
    pitchzone = db.Column(db.String(10))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    outcome = db.relationship("Outcome")
    event_option = db.relationship("EventOption")
    team = db.relationship("Team")

    def __repr__(self):
        return '<Event %r>' % (self.name)

    def to_dict(self):
        data = {
            "id" : self.id,
            "name" : self.name
        }
        return data
    
    def from_dict(self, data):
        for field in ["name", "game_id", "team_id", "event_option_id", "outcome_id", "timestamp", "pitchzone"]:
            if field in data:
                setattr(self, field, data[field])

