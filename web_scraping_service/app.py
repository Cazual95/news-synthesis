"""Define the service API endpoints and run the application.

This module defines the endpoints and runs the server. This service is designed to run periodic scraping jobs.
It scrapes data from news websites and dumps the data into a database.
"""

import flask
from flask_apscheduler import APScheduler

from web_scraping_service.config import ApplicationConfig
from web_scraping_service.scrapers.news import FoxNewsScraper

from web_scraping_service import vector_db

app = flask.Flask(__name__)
app.config.from_object(ApplicationConfig)

scheduler = APScheduler()

scheduler.init_app(app)
scheduler.start()


@scheduler.task('interval', id='scrape_job_1', minutes=5)
def scrape_job_1():
    """Test interval running."""
    print('Running scrape_job_1')
    scraper = FoxNewsScraper(False)
    scraper.scrape(20)


if __name__ == '__main__':
    # app.run(debug=True, use_reloader=False)
    # scraper = FoxNewsScraper(False)
    # scraper.scrape(20)
    vector_db.create_author_schema()
    vector_db.create_article_schema()