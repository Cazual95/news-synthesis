import uuid

from flask import g, current_app
from flask_pymongo import PyMongo
from werkzeug.local import LocalProxy


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        db = g._database = PyMongo(current_app).db

    return db

db = LocalProxy(get_db)

def add_article(name: str, obj_id: str = str(uuid.uuid4())) -> None:
    new_article = {
        'id': obj_id,
        'name': name
    }
    db.articles.insert_one(new_article)