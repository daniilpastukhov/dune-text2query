import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from dune_scraper.spiders import DuneSpider

if __name__ == '__main__':
    settings_file_path = 'dune_scraper.settings'
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

    process = CrawlerProcess(get_project_settings())
    process.crawl(DuneSpider)
    process.start()
