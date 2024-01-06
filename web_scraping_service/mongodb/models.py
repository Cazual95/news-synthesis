"""Exports classes defining objects in mongoDB."""
import typing
import uuid
from dataclasses import dataclass, field


def create_uuid():
    return str(uuid.uuid4())


@dataclass
class SourceAuthor:
    """An author writing for a primary source such as a domain like foxnews.com.

    Attributes:
        _id: The unique id of the object.
        name: The authors name.
        profilePage: The URL of the authors profile page.
        profileImage: An image of the author.
    """
    name: str
    profilePage: str
    profileImage: typing.Union[str, None]
    _id: str = field(default_factory=create_uuid)

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
    """
    url: str
    publicationDate: str
    content: str
    title: str
    authors: list[str]
    _id: str = field(default_factory=create_uuid)

    def get_id(self):
        """Get this objects id."""
        return self._id
