import os

from src.db import MongoDatabase


class MongoPipeline:
    def __init__(self):
        self.db = None

    def open_spider(self, spider):
        self.db = MongoDatabase()
        spider.logger.info('Connected to MongoDB.')

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        spider.logger.info('Processing item...')
        self.db.insert_one(item)
        spider.logger.info('Processed item.')
        return item
