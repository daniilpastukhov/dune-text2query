FROM ubuntu

COPY ./scraper /app
WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y python3-pip libpq-dev

RUN pip install -r requirements.txt && \
    pip install -e .

RUN playwright install-deps && \
    playwright install chromium

CMD ["scrapy", "crawl", "dune"]