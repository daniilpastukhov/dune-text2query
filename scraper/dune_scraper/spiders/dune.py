import json
import re
from dataclasses import asdict

from scrapy import Spider, Request
from scrapy_playwright.page import PageMethod

from dune_scraper.items import QueryItem
from dune_scraper.db import MongoDatabase

BASE_URL = 'https://dune.com/browse/queries?page=%d'

# These selectors mean "class starts with"
TITLE_LINK_SELECTOR = '[class^="QueriesList_queryName"]::attr(href)'
TITLE_TEXT_SELECTOR = '[class^="QueriesList_queryName"]::text'
ROWS_SELECTOR = '[class^="QueriesList_table"] tr'

LIMIT = 2000  # required number of items
ITEMS_PER_PAGE = 20  # number of items per page

# Connect to the database and retrieve number of properties
db = MongoDatabase()
n = db.get_total_queries()


class DuneSpider(Spider):
    name: str = 'dune'
    total_parsed_items: int = n
    current_page_number: int = total_parsed_items // ITEMS_PER_PAGE + 1

    def start_requests(self):
        yield Request(
            url=BASE_URL % self.current_page_number,
            callback=self.parse,
            meta={
                'playwright': True,
                'playwright_context': self.current_page_number,
                'playwright_page_methods': [PageMethod('wait_for_selector', ROWS_SELECTOR)],
                'errback': self.errback
            }
        )

    async def parse(self, response, **kwargs):
        rows = response.css(ROWS_SELECTOR)

        # Iterate over all rows and select required data per property
        for row in rows:
            if self.total_parsed_items >= LIMIT:
                break

            url = row.css(TITLE_LINK_SELECTOR)

            yield Request(url='https://dune.com' + url.get(),
                          callback=self.parse_query,
                          meta={
                              'playwright': True,
                              'playwright_context': self.current_page_number,
                              "playwright_include_page": True,
                              'errback': self.errback
                          })

            self.total_parsed_items += 1

        # Continue to the next page if limit is not reached, stop otherwise
        if self.total_parsed_items < LIMIT:
            self.current_page_number += 1
            yield Request(
                url=BASE_URL % self.current_page_number,
                callback=self.parse,
                meta={
                    'playwright': True,
                    'playwright_context': self.current_page_number,
                    'playwright_page_methods': [PageMethod('wait_for_selector', ROWS_SELECTOR)],
                    'errback': self.errback
                }
            )

    async def parse_query(self, response, **kwargs):
        page = response.meta["playwright_page"]
        page.on("response", self.handle_response)

    async def handle_response(self, response):
        if response.url == 'https://core-hsr.dune.com/v1/graphql':
            body = await response.body()
            json_body = json.loads(body.decode('utf-8'))
            if 'queries' in json_body['data']:
                query_body = json_body['data']['queries'][0]
                db.insert_one(asdict(QueryItem(
                    name=query_body['name'],
                    query=query_body['query']
                )))

    async def errback(self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()
