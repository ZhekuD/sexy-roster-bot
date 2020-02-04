from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    rosters = db.relationship('Roster', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'


class Roster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roster = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
