"""Exports classes for scraping articles from foxnews.com.

Typical usage example:
```python
from web_scraping_service.scrapers.news import FoxNews

fox_news_scraper = FoxNewsScraper()
fox_news_scraper.scrape()
```
"""
import base64
import logging
import random

import playwright.sync_api
import requests

import data_models.article
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
        pw: The sync playwright instance to use.
        logged_in_context: A playwright context that has already gone through the login process.
        logged_in_page: A playwright page that has already been logged in.
    """
    use_vpn: bool = False
    pw: playwright.sync_api.Playwright
    logged_in_context: playwright.sync_api.BrowserContext
    logged_in_page: playwright.sync_api.Page
    logger: logging.Logger

    def __init__(self, use_vpn: bool, pw: playwright.sync_api.Playwright):
        """Initialize the scraper based on vpn preference."""
        self.use_vpn = use_vpn
        self.pw = pw
        self.logged_in_context, self.logged_in_page = self._login()
        self.logger = logging.getLogger(self.__class__.__name__)

    def _login(self) -> (playwright.sync_api.BrowserContext, playwright.sync_api.Page):
        """Login to the website.

        Returns:
            The post login page.
        """
        print('logging in...')
        browser = self.pw.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context(user_agent=random.choice(USER_AGENT_STRINGS))
        page = context.new_page()
        page.set_default_timeout(60000)
        page.goto('https://www.foxnews.com/', wait_until='domcontentloaded')
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
        page.goto('https://www.foxnews.com/', wait_until='domcontentloaded')
        print('login complete!')
        return context, page

    def _get_article_links(self, page: playwright.sync_api.Page) -> list[playwright.sync_api.Locator]:
        """Get a list of article links on the current page.

        Args:
            page: The page to look for article links on.

        Returns:
            A list of links to articles.
        """
        return page.locator('css=.title').all()

    def _scrape_article_title(self, page: playwright.sync_api.Page) -> str:
        """Scrape the title of the article.

        Contains multiple attempts to get the title based on different page layouts.

        Args:
            page: The page to scrape the title from.

        Returns:
            The scraped title.
        """
        try:
            return page.locator('css=.page-content h1').inner_text()
        except TimeoutError as e:
            self.logger.error('Timeout when scraping title.', e)

    def _scrape_article_publication_date(self, page: playwright.sync_api.Page) -> str:
        """Scrape the publication date of the article.

        Contains multiple attempts to get the publication date based on different page layouts.

        Args:
            page: The page to scrape the date from.

        Returns:
            The scraped publication date.
        """
        try:
            return page.locator(
                'css=.article-date time').inner_text()
        except TimeoutError as e:
            self.logger.error('Timeout when scraping publication date.', e)

    def _scrape_article(self, page: playwright.sync_api.Page) -> (
            data_models.article.SourceArticle, list[data_models.article.SourceArticle]):
        """Scrape the article and authors from an article page.

        Args:
            page: The page the link to the article is on.

        Returns:
            An article object and a list of author objects.
        """
        # print('scraping author information...')
        # author_loc = page.locator('css=.author-byline')
        # try:
        #     thumbnail = base64.b64encode(
        #         requests.get(author_loc.locator('css=img').get_attribute('src')).content)
        # except:
        #     thumbnail = None
        # author_info = author_loc.locator('css=a').all()[0]
        # author = data_models.article.SourceAuthor(
        #     name=author_info.inner_text(),
        #     profilePage=author_info.get_attribute('href'),
        #     profileImage=thumbnail
        # )
        # print('authors scrape complete!')
        content_list = list()
        print('scraping article...')
        for section in page.locator('css=.article-body p').all():
            try:
                content_list.append(section.inner_text())
            except:
                print('error gathering content list')
        content = '\n'.join(content_list)
        article = data_models.article.SourceArticle(
            url=page.url,
            title=self._scrape_article_title(page),
            publicationDate=self._scrape_article_publication_date(page),
            authors=list(),
            content=content
        )
        print('article scrape complete!')
        return article, list()  # , [author]

    def scrape(self, url: str) -> (data_models.article.SourceArticle, list[data_models.article.SourceAuthor]):
        """Scrape the foxnews.com home page of articles.

        Args:
            url: The url to scrape.

        Returns:
            A scraped article and a collection of article authors.
        """
        page = self.logged_in_page
        page.goto(url, wait_until='domcontentloaded')
        article, authors = self._scrape_article(page)
        return article, authors
