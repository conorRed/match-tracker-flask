from flask_sqlalchemy import SQLAlchemy
from app import db
from flask import url_for


class PaginatedAPIMixin(object):
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

class Event(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    outcomes = db.relationship('Outcome', backref='event', lazy='dynamic')
    def __repr__(self):
        return '<Event %r>' % (self.name)

    def to_dict(self):
        data = {
            "id" : self.id,
            "name" : self.name
        }
        return data
    
    def from_dict(self, data):
        for field in ["name"]:
            if field in data:
                setattr(self, field, data[field])

class Outcome(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    def __repr__(self):
        return '<Outcome %r>' % (self.name)

    def to_dict(self):
        data = {
            "id":         self.id,
            "name":       self.name,
            "event_id":   self.event_id
        }
        return data
        
    def from_dict(self, data):
        for field in ["name", "event_id"]:
            if field in data:
                setattr(self, field, data[field])