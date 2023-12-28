"""Exports classes for scraping articles from foxnews.com.

Typical usage example:
```python
from web_scraping_service.scrapers.news import FoxNews

fox_news_scraper = FoxNewsScraper()
fox_news_scraper.scrape()
```
"""
import base64
import json
import random
import time
from datetime import datetime

import flask_pymongo
import playwright.sync_api
import requests
from playwright.sync_api import sync_playwright

from web_scraping_service import config

USER_AGENT_STRINGS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.3497.92 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
]


class FoxNewsScraper:
    """A web scraper for foxnews.com

    Attributes:
        use_vpn: A flag to determine if a vpn should be used.
    """
    use_vpn: bool = False

    def __init__(self, use_vpn: bool):
        """Initialize the scraper based on vpn preference."""
        self.use_vpn = use_vpn

    def _login(self, page: playwright.sync_api.Page) -> playwright.sync_api.Page:
        """Login to the website.

        Args:
            page: The page to begin the login process on.

        Returns:
            The post login page.
        """
        page.locator('css=#account > div > a').click()
        page.wait_for_url('https://my.foxnews.com/')
        email_input = page.get_by_placeholder('name@mydomain.com')
        email_input.fill(config.FOXNEWS_USERNAME)
        page.locator(
            'css=#wrapper > div > div.page-content > main > section > div > form > div:nth-child(2) > button').click()
        page.wait_for_load_state('domcontentloaded')
        page.get_by_text('Click here to sign in with password.').click()
        page.wait_for_load_state('domcontentloaded')
        page.get_by_placeholder('Enter your email').fill(config.FOXNEWS_USERNAME)
        page.get_by_placeholder('Enter your password').fill(config.FOXNEWS_PASSWORD)
        page.get_by_role("button", name="Sign In").click()
        page.wait_for_load_state('domcontentloaded')
        page.locator("#wrapper").get_by_role("link", name="Fox News").click()
        page.wait_for_load_state('domcontentloaded')
        return page

    def _get_article_links(self, page: playwright.sync_api.Page) -> list[playwright.sync_api.Locator]:
        """Get a list of article links on the current page.

        Args:
            page: The page to look for article links on.

        Returns:
            A list of links to articles.
        """
        return page.locator('css=.title').all()

    def _scrape_article(self, page: playwright.sync_api.Page) -> (dict, list[dict]):
        """Scrape the article and authors from an article page.

        Args:
            page: The page the link to the article is on.

        Returns:
            An article object and a list of author objects.
        """
        author ={
            'name': page.locator('css=#wrapper > div.page-content > div.row.full > main > article > header > div.author-byline > span:nth-child(2) > span > a').inner_text(),
            'profilePage': page.locator('css=#wrapper > div.page-content > div.row.full > main > article > header > div.author-byline > span:nth-child(2) > span > a').get_attribute('href'),
            'thumbnail': base64.b64encode(requests.get(page.locator('css=#wrapper > div.page-content > div.row.full > main > article > header > div.author-byline > span.author-headshot > img').get_attribute('src')).content)
        }
        article ={
            'url': page.url,
            'title': page.locator('css=#wrapper > div.page-content > div.row.full > main > article > header > div.article-meta.article-meta-upper > h1').inner_text(),
            'publicationDate': page.locator('css=#wrapper > div.page-content > div.row.full > main > article > header > div:nth-child(3) > span > time').inner_text(),
            'authors': [author],
            'content': '\n'.join([section.inner_text() for section in page.locator('css=p .speakable').all()])
        }
        return article, [author]

    def scrape(self, max_articles: int) -> None:
        """Scrape the foxnews.com home page of articles.

        Args:
            max_articles: The maximum number of articles to scrape before stopping.
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=50)
            context = browser.new_context(user_agent=random.choice(USER_AGENT_STRINGS))
            page = context.new_page()
            page.set_default_timeout(30000)
            page.goto('https://www.foxnews.com/', wait_until='domcontentloaded')
            page = self._login(page)
            page.goto('https://www.foxnews.com/', wait_until='domcontentloaded')
            article_links = self._get_article_links(page)
            articles, authors_list = list(), list()
            for link in article_links:
                with context.expect_page() as new_page_info:
                    link.click(button='middle')  # Opens a new tab
                new_page = new_page_info.value
                new_page.wait_for_load_state('domcontentloaded')
                article, authors = self._scrape_article(new_page)
                articles.append(article)
                authors_list.append(authors)
            print(json.dumps(articles[0], indent=4))

            time.sleep(5000)
