"""Exports classes defining objects created by web scraping"""
import datetime
import typing
import uuid
from dataclasses import dataclass, field


def create_uuid():
    return str(uuid.uuid4())


def timestamp():
    return str(datetime.datetime.now().isoformat())


@dataclass
class SourceAuthor:
    """An author writing for a primary source such as a domain like foxnews.com.

    Attributes:
        _id: The unique id of the object.
        name: The authors name.
        profilePage: The URL of the authors profile page.
        profileImage: An image of the author.
        createdOn: The date the author was scraped.
    """
    name: str
    profilePage: str
    profileImage: typing.Union[str, None]
    _id: str = field(default_factory=lambda: create_uuid())
    createdOn: str = field(default_factory=lambda: timestamp())

    def get_id(self):
        """Get this objects id."""
        return self._id


@dataclass
class SourceArticle:
    """An article pulled directly from a primary source such as a scrape of foxnews.com.

    Attributes:
        _id: The unique id of the object.
        url: The url the article was sourced from.
        publicationDate: The date the article was published.
        content: The content of the article.
        title: The title of the article.
        authors: A list of ids referencing web_scraping_service.mongodb.models.SourceAuthor objects.
        createdOn: The date the article was scraped.
    """
    url: str
    publicationDate: str
    content: str
    title: str
    authors: list[str]
    _id: str = field(default_factory=create_uuid)
    createdOn: str = field(default_factory=lambda: timestamp())

    def get_id(self):
        """Get this objects id."""
        return self._id
