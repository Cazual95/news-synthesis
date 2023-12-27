"""Define the service API endpoints and run the application.

This module defines the endpoints and runs the server. This service is designed to run periodic scraping jobs.
It scrapes data from news websites and dumps the data into a database.
"""

import flask
from flask_apscheduler import APScheduler

from web_scraping_service.config import ApplicationConfig
from web_scraping_service.db import add_article

app = flask.Flask(__name__)
app.config.from_object(ApplicationConfig)

scheduler = APScheduler()

scheduler.init_app(app)
scheduler.start()


@scheduler.task('interval', id='scrape_job_1', seconds=5)
def scrape_job_1():
    """Test interval running."""
    with app.app_context():
        add_article('article')
    print('Running scrape_job_1')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)