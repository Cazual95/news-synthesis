"""Main module for scraping."""
import json
import tqdm

from kafka import KafkaConsumer, KafkaProducer
from playwright.sync_api import sync_playwright

import data_models.job
import web_scraper.scrapers.foxnews

consumer = KafkaConsumer('articles-to-scrape', bootstrap_servers='172.30.22.241:9092',
                         api_version=(0, 11, 5), group_id=None, auto_offset_reset='earliest',
                         value_deserializer=lambda v: data_models.job.ArticleScrapeJob(
                             **json.loads(v.decode('utf-8'))))

producer = KafkaProducer(bootstrap_servers='172.30.22.241:9092', api_version=(0, 11, 5),
                         value_serializer=lambda v: json.dumps(v, default=lambda o: o.__dict__).encode('utf-8'))


def main():
    print('starting consumption')
    # for job in consumer:
    #     print(job.value.url)
    with sync_playwright() as playwright:
        scraper = web_scraper.scrapers.foxnews.FoxNewsScraper(False, playwright)
        for job in tqdm.tqdm(consumer):
            print(job.value.url)
            article, authors = scraper.scrape(job.value.url)
            producer.send('scraped-articles', article)


if __name__ == '__main__':
    main()
