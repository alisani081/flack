from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_channels = db.Table('user_channels',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('channel_id', db.Integer, db.ForeignKey('channels.id'), primary_key=True),
    db.Column('date_joined', db.DateTime, nullable=False)
)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Channel(db.Model):
    __tablename__ = "channels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    members = db.relationship('User', backref='channel', lazy=True)