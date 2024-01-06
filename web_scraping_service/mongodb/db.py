"""Exports actions to take against mongoDB."""

import uuid

from flask import g, current_app
from flask_pymongo import PyMongo
from werkzeug.local import LocalProxy

import web_scraping_service.mongodb.models


def get_db():
    """Configure and return db."""
    database = getattr(g, "_database", None)

    if database is None:
        database = g._database = PyMongo(current_app).db

    return database

database = LocalProxy(get_db)

def add_article(new_article: web_scraping_service.mongodb.models.SourceArticle) -> None:
    """Add an Article object to the 'sourceArticles' table.

    Args:
        new_article: The article to add.
    """
    database.sourceArticles.insert_one(new_article.__dict__)

def add_author(new_author: web_scraping_service.mongodb.models.SourceAuthor) -> None:
    """Add an Author object to the 'sourceAuthors' table.

    Args:
        new_author: The author to add.
    """
    database.sourceAuthors.insert_one(new_author.__dict__)

def add_authors(new_authors: list[web_scraping_service.mongodb.models.SourceAuthor]) -> None:
    """Add a list of authors to the 'sourceAuthors' table.

    Args:
        new_authors: The new authors to add.
    """
    database.sourceAuthors.insert_many([auth.__dict__ for auth in new_authors])