"""Main module for scraping."""
import json
import logging

import tqdm

from kafka import KafkaConsumer, KafkaProducer
from playwright.sync_api import sync_playwright
import redis

import data_models.job
import web_scraper.scrapers.foxnews

consumer = KafkaConsumer('articles-to-scrape', bootstrap_servers='172.30.22.241:9092',
                         api_version=(0, 11, 5), group_id=None, auto_offset_reset='earliest',
                         value_deserializer=lambda v: data_models.job.ArticleScrapeJob(
                             **json.loads(v.decode('utf-8'))))

producer = KafkaProducer(bootstrap_servers='172.30.22.241:9092', api_version=(0, 11, 5),
                         value_serializer=lambda v: json.dumps(v, default=lambda o: o.__dict__).encode('utf-8'))

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def main():
    print('starting consumption')
    # for job in consumer:
    #     print(job.value.url)
    with sync_playwright() as playwright:
        scraper = web_scraper.scrapers.foxnews.FoxNewsScraper(False, playwright)
        for job in (pbar := tqdm.tqdm(consumer)):
            pbar.set_description(f'Scraping URL: {job.value.url}')
            if not r.get(job.value.url):
                # try:
                article, authors = scraper.scrape(job.value.url)
                producer.send('articles-to-preprocess', article)
                r.set(job.value.url, 'true')
                print('article scrapped successfully!')
                print(json.dumps(article, default=lambda o: o.__dict__, indent=4))
                # except:
                #     print('error scraping url')
            else:
                print('Entry found in redis. Skipping.')

    producer.flush()
    producer.close()


if __name__ == '__main__':
    main()
