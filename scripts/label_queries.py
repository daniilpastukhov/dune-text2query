import json
import os
import openai
from scripts.templates import LABEL_QUERY_TEMPLATE
from scraper.src.db import MongoDatabase
from dotenv import load_dotenv
from tqdm import tqdm
from joblib import Parallel, delayed

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
    return response['choices'][0]['text'].strip()


def label_queries(queries):
    """Label queries with the help of GPT3 API."""

    set_queries = set()
    for query in tqdm(queries):
        text_query = query['query']
        if len(text_query.split()) > 200 or text_query in set_queries:
            continue
        query_label = label_query(text_query)
        set_queries.add(text_query)
        db.update_label(query['_id'], query_label)


if __name__ == '__main__':
    db = MongoDatabase()
    queries = db.get_n_queries()
    labels = Parallel(n_jobs=8)(delayed(label_query)(q['_id']) for q in queries if len(q['_id'].split()) < 200)
    for query, label in zip(queries, labels):
        db.update_label(query['_id'], label)
    # label_queries_test()
