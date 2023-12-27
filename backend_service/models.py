import uuid

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_uuid_hex():
    return uuid.uuid4().hex

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid_hex)
    email = db.Column(db.String(345), unique=True)
    password = db.Column(db.Text, nullable=False)