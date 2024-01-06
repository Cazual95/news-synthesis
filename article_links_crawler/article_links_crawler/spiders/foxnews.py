"""Exports a scrapy crawler for crawling foxnews.com."""
import json
from pathlib import Path
from typing import Iterable, Any

import scrapy
from kafka import KafkaProducer
from scrapy import Request
from scrapy.http import Response

from ..items import ArticleLinkItem

producer = KafkaProducer(bootstrap_servers='172.30.22.241:9092', api_version=(0,11,5),
                         value_serializer=lambda v: json.dumps(v, default=lambda o: o.__dict__).encode('utf-8'))


class FoxNewsSpider(scrapy.Spider):
    """A spider for crawling foxnews.com to capture article links.

    Attributes:
        name: The name of the spider.
        allowed_domains: The domains the spider is allowed to crawl to.
        start_urls: The urls to start crawling from.
    """
    name: str = 'foxnews'
    allowed_domains: list[str] = ['foxnews.com']
    start_urls: list[str] = ['https://www.foxnews.com/']

    def start_requests(self) -> Iterable[Request]:
        """Start starts the initial requests for crawling."""
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={'playwright': True})

    def parse(self, response: Response, **kwargs: Any) -> Any:
        """Parse the request response.

        Args:
            response: The response to parse.
            kwargs: Additional kwargs passed.

        Returns:
            A parsed article_links_crawler.items.ArticleLinkItem.
        """
        links = response.css('article a:link')
        for link in links:
            url = response.urljoin(link.attrib['href'])
            topic = url.split('/')[3]
            if topic != 'video':
                article_link_item = ArticleLinkItem(
                    url=url,
                    domainTopic=topic
                )
                producer.send('articles-to-scrape', article_link_item)
                yield article_link_item
