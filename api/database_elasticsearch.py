from elasticsearch import Elasticsearch
from typing import List, Optional
from database_interface import DatabaseInterface
from models import User, Product
from uuid import uuid4 as generate_uuid


class ElasticsearchDatabase(DatabaseInterface):
    USERS_INDEX = "users"
    IMAGES_INDEX = "image-products"

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.es = Elasticsearch([{'host': self.host, 'port': self.port}])

    def create_product_details(self, owner_id: str, title: str, desc: str, is_visible: bool, price: float,
                               list_image_details) -> str:
        if (owner_id == ""):
            return None

        result = self.es.create(self.IMAGES_INDEX, str(generate_uuid()), {
            "owner_id": owner_id,
            "product_name": title,
            "description": desc,
            "is_visible": is_visible,
            "price": price,
            "images": [details.to_dict() for details in list_image_details]
        })

        return result["_id"]

    def create_user(self, email, name, password_hash) -> str:
        result = self.es.create(self.USERS_INDEX, str(generate_uuid()), {
            "email": email, "name": name, "password_hash": password_hash
        })
        return result["_id"]

    def get_user_by_id(self, id) -> Optional[User]:
        search_body = {
            "query": {
                "term": {
                    "_id": id
                }
            }
        }

        result = self.es.search(index=self.USERS_INDEX, body=search_body)
        if result is not None and len(result['hits']['hits']) == 1:
            return User(result['hits']['hits'][0])
        else:
            return None

    def get_user_by_email(self, email) -> Optional[User]:
        search_body = {
            "query": {
                "term": {
                    "email": email
                }
            }
        }
        result = self.es.search(index=self.USERS_INDEX, body=search_body)
        if result is not None and len(result['hits']['hits']) == 1:
            return User(result['hits']['hits'][0])

        else:
            return None

    def get_products(self, query: str, price_min: float, price_max: Optional[float] = None) -> List[Product]:
        search_body = {"query": {"bool": {"must": [{
            "term": {
                "is_visible": True
            }
        }]}}}
        multi_match_query = {
            "query": query,
            "type": "phrase",
            "fields": ["product_name", "description"]
        }

        range_query = {"price": {"gte": price_min}}
        if price_max is not None and price_max >= price_min:
            range_query["price"]["lte"] = price_max

        insertable_search_location = search_body["query"]["bool"]["must"]

        if price_min is not None or price_max is not None:
            insertable_search_location.append({"range": range_query})

        if query is not None and query.strip() != "":
            insertable_search_location.append({"multi_match": multi_match_query})

        result = self.es.search(index=self.IMAGES_INDEX, body=search_body)
        return self.convert_es_to_product(result)

    def convert_es_to_product(self, result) -> List[Product]:
        if result is not None and len(result['hits']['hits']) > 0:
            return [Product(hit) for hit in result['hits']['hits']]
        else:
            return []

    def init_db(self, number_of_replicas=0):
        database: Elasticsearch = self.es
        # Create an index to store the user information including including
        # their name, email and hashed password
        database.indices.create(self.USERS_INDEX, {"mappings": {
            "properties": {
                "name": {
                    "type": "text"
                },
                "email": {
                    "type": "keyword"
                },
                "password": {
                    "type": "text",
                    "index": False
                },
            }},
            "settings": {
                "number_of_replicas": number_of_replicas
        }
        })

        # Create an index to store the image product data
        database.indices.create(self.IMAGES_INDEX, {"mappings": {
            "properties": {
                "product_name": {
                    "type": "keyword"
                },
                "description": {
                    "type": "text"
                },
                "owner_id": {
                    "type": "keyword",
                },
                "is_visible": {
                    "type": "boolean"
                },
                "price": {
                    "type": "double"
                },
                "images": {
                    "type": "nested"
                }
            }},
            "settings": {
                "number_of_replicas": number_of_replicas
        }
        })
