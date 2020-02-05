from datetime import datetime
from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_telegram_id = db.Column(db.Integer)
    first_name = db.Column(db.String(32))
    second_name = db.Column(db.String(32))
    username = db.Column(db.String(32))
    rosters = db.relationship('Roster', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'


class Roster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text())
    title = db.Column(db.String(128))
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
