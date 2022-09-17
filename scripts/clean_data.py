from scraper.src.db import MongoDatabase

if __name__ == '__main__':
    db = MongoDatabase()
    all_queries = list(db.get_n_queries(-1))
    set_queries = set()
    for q in all_queries:
        query_text = q['query']
        if query_text in set_queries:


    print(len(queries), len(all_queries))