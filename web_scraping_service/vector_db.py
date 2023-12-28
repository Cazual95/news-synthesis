"""Exports functions for working with the weaviate vector database."""

import weaviate

import web_scraping_service.config

client = weaviate.Client(web_scraping_service.config.WEAVIATE_URL)


def create_author_schema() -> None:
    """Create a schema for authors."""
    author_obj = {
        "class": "Author",
        "description": "An author of an article, publication, etc.",
        "properties": [
            {
                "dataType": ["text"],
                "description": "Name of the author.",
                "name": "name",
            },
            {
                "dataType": ["text"],
                "description": "The profile page of the author.",
                "name": "profilePage"
            }
        ]
    }
    client.schema.create_class(author_obj)


def create_article_schema() -> None:
    """Create a schema for news articles."""
    article_obj = {
        "class": "Article",
        "description": "A news article.",
        "properties": [
            {
                "dataType": ["text"],
                "description": "The content of the article.",
                "name": "content",
            },
            {
                "dataType": ["text"],
                "description": "The title of the article.",
                "name": "title"
            },
            {
                "dataType": ["Author"],
                "description": "The author of the article.",
                "name": "author"
            }
        ]
    }
    client.schema.create_class(article_obj)
