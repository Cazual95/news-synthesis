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
            },
            {
                "dataType": ["blob"],
                "description": "The thumbnail image of the author.",
                "name": "thumbnail"
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
                "dataType": ["uuid"],
                "description": "The unique identifier of the article.",
                "name": "id",
            },
            {
                "dataType": ["text"],
                "description": "The content of the article.",
                "name": "content",
            },
            {
                "dataType": ["text"],
                "description": "The url of the article.",
                "name": "url",
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
            },
            {
                "dataType": ["date"],
                "description": "Publication date.",
                "name": "publicationDate",
            },
        ]
    }
    client.schema.create_class(article_obj)

def add_articles(articles: list[dict]) -> None:
    """Add a collection of articles to weaviate.

    Args:
        articles: The articles to add.
    """
    with client.batch as batch:
        for article in articles:
            batch.add_data_object(article, 'Article')


def add_authors(authors: list[dict]) -> None:
    """Add a collection of authros to weaviate.

    Args:
        authors: The authors to add.
    """
    with client.batch as batch:
        for author in authors:
            batch.add_data_object(author, 'Author')
