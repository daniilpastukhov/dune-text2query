import json
import os
import openai
from scripts.templates import LABEL_QUERY_TEMPLATE
from scraper.src.db import MongoDatabase
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def label_query(query: str) -> str:
    """Label a query with the help of GPT3 API.

    Args:
        query (str): A query.

    Returns:
        str: The query type.
    """
    gpt_prompt = LABEL_QUERY_TEMPLATE.format(query)
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=gpt_prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['text']


def get_queries(mongo_client: MongoDatabase):
    collection = mongo_client.collection
    return collection.find('{}')


def label_queries(n=-1):
    """Label queries with the help of GPT3 API."""
    db = MongoDatabase()
    queries = db.get_n_queries(n)
    for query in tqdm(queries):
        query_label = label_query(query)
        print(query_label)
        query.update_one({'_id': query['_id']}, {'$set': {'query_label': query_label}})


if __name__ == '__main__':
    label_queries()
    # label_queries_test()
