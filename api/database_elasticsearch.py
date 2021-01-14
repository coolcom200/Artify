from elasticsearch import Elasticsearch
from api.database_interface import DatabaseInterface
from api.user import User
from uuid import uuid4 as generate_uuid


class ElasticsearchDatabase(DatabaseInterface):
    USERS_INDEX = "users"
    IMAGES_INDEX = "image-products"

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.es = Elasticsearch([{'host': self.host, 'port': self.port}])

    def create_product_details(
            self, owner_id: str, title: str, desc: str, is_visible: bool, price: float, list_image_details):
        if (owner_id == ""):
            return None
        return self.es.create(self.IMAGES_INDEX, str(generate_uuid()), {
            "owner_id": owner_id,
            "product_name": title,
            "description": desc,
            "is_visible": is_visible,
            "price": price,
            "images": [details.to_dict() for details in list_image_details]
        })

    def create_user(self, email, name, password_hash) -> str:
        result = self.es.create(self.USERS_INDEX, str(generate_uuid()), {
            "email": email, "name": name, "password_hash": password_hash
        })
        return result["_id"]

    def get_user_by_id(self, id) -> User:
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

    def get_user_by_email(self, email) -> User:
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

    def search(self, query: str, price_min: float, price_max: float):
        search_body = {"query": {}}
        multi_match_query = {
            "query": query,
            "fields": ["product_name", "description"]
        }

        price_min = 0 if price_min is None else float(price_min)
        range_query = {"price": { "gte" : price_min }}

        if price_max is not None and float(price_max) >= price_min:
            range_query["price"]["lte"] = float(price_max)

        if price_min is not None or price_max is not None:
            search_body["query"]["range"] = range_query

        if query is not None and query.strip() != "":
            search_body["query"]["multi_match"] = multi_match_query

        return self.es.search(index=self.IMAGES_INDEX, body=search_body)

    def close(self):
        self.es.close()

    def get_visible_products(self, page=1, size=25):
        search_body = {
            # "from": page,
            # "size": size,
            "query": {"match_all": {}}
        }
        return self.es.search(index=self.IMAGES_INDEX, body=search_body)

    def init_db(self):
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
            }}})

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
            }}})
