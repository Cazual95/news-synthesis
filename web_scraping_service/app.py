"""Define the service API endpoints and run the application.

This module defines the endpoints and runs the server. This service is designed to run periodic scraping jobs.
It scrapes data from news websites and dumps the data into a database.
"""

import flask
from flask_apscheduler import APScheduler
from werkzeug.local import LocalProxy

from web_scraping_service.db import get_db

app = flask.Flask(__name__)

scheduler = APScheduler()

scheduler.init_app(app)
scheduler.start()

db = LocalProxy(get_db)

@scheduler.task('interval', id='scrape_job_1', seconds=5)
def scrape_job_1():
    """Test interval running."""
    print('Running scrape_job_1')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)