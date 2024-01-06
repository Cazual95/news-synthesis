"""Exports a class for incoming job data validation."""

from dataclasses import dataclass


@dataclass
class ArticleScrapeJob:
    """An incoming job from kafka.

    Attributes:
        url: The url of the article.
        domainTopic: The topic as assigned by the domain.
    """
    url: str
    domainTopic: str