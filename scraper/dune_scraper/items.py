from dataclasses import dataclass


@dataclass
class QueryItem:
    name: str
    query: str
