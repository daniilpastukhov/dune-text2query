# Dune.com text2query
```
Capacity's team project for ETHBerlin 2022 hackathon
```

Machine learning on the way to to crypto analytics mass adoption. 

> .env file is required to run the code

You can run scraper via Docker using `docker-compose up` command.

## Tech stack:
 ⁃ Python
 ⁃ OpenAI’s GPT-3
 ⁃ Scrapy framework
 ⁃ MongoDB (cloud)

## .env file
Template for storing environment variables:
```bash
PROJECT_NAME="dune"

SCRAPY_PROJECT="./"

MONGO_URI=YOUR_MONGO_CLOUD_URI
OPENAI_API_KEY=YOUR_OPENAI_KEY
```
