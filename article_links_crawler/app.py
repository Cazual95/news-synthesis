import json

from kafka import KafkaProducer
from scrapy.crawler import CrawlerProcess

from article_links_crawler.spiders.foxnews import FoxNewsSpider, producer


# Definition of a Kafka Producer with SSL authentication
# and JSON serialization for value and key


def main():
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                "items.json": {"format": "json"},
            },
        }
    )
    process.crawl(FoxNewsSpider)
    process.start()
    producer.flush()
    producer.close()


if __name__ == '__main__':
    main()
