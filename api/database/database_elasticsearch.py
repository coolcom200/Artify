from typing import List, Optional
from uuid import uuid4 as generate_uuid

from elasticsearch import Elasticsearch

from api.database.database_interface import DatabaseInterface
from api.models.common_models import FileWithPath
from api.models.elasticsearch_models import ProductElasticsearch, UserElasticsearch


class ElasticsearchDatabase(DatabaseInterface):
    USERS_INDEX = "users"
    IMAGES_INDEX = "image-products"

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.es = Elasticsearch([{"host": self.host, "port": self.port}])

    def create_product_details(self, owner_id: str, title: str, desc: str, is_visible: bool,
                               price: float, list_image_details) -> Optional[ProductElasticsearch]:
        if owner_id == "":
            return None

        item = {"owner_id": owner_id, "product_name": title, "description": desc,
                "is_visible": is_visible, "price": price,
                "images": [{"file_path": details.filePath, "file_name": details.fileName} for
                           details in list_image_details]}

        result = self.es.create(self.IMAGES_INDEX, str(generate_uuid()), item)

        if result is not None and result["result"] == "created":
            return ProductElasticsearch(owner_id, title, desc, is_visible, price, result["_id"],
                                        list_image_details, self.get_user_by_id)

    def create_user(self, email, name, password_hash) -> str:
        result = self.es.create(self.USERS_INDEX, str(generate_uuid()),
                                {"email": email, "name": name, "password_hash": password_hash})
        return result["_id"]

    def get_user_by_id(self, user_id) -> Optional[UserElasticsearch]:
        search_body = {"query": {"term": {"_id": user_id}}}

        result = self.es.search(index=self.USERS_INDEX, body=search_body)
        if result is not None and len(result["hits"]["hits"]) == 1:
            return UserElasticsearch(result["hits"]["hits"][0], self.get_users_products)
        else:
            return None

    def get_user_by_email(self, email) -> Optional[UserElasticsearch]:
        search_body = {"query": {"term": {"email": email}}}
        result = self.es.search(index=self.USERS_INDEX, body=search_body)
        if result is not None and len(result["hits"]["hits"]) == 1:
            return UserElasticsearch(result["hits"]["hits"][0], self.get_users_products)

        else:
            return None

    def get_users_products(self, user_id) -> List[ProductElasticsearch]:
        search_body = {"query": {"term": {"owner_id": user_id}}}

        result = self.es.search(index=self.IMAGES_INDEX, body=search_body)
        if result is not None and len(result["hits"]["hits"]) >= 1:
            return self.convert_es_to_product(result)
        else:
            return []

    def get_products(self, query: Optional[str], price_min: Optional[float],
                     price_max: Optional[float] = None) -> List[ProductElasticsearch]:
        search_body = {"query": {"bool": {"must": [{"term": {"is_visible": True}}]}}}
        multi_match_query = {"query": query, "type": "phrase",
                             "fields": ["product_name", "description"]}

        if price_min is None:
            price_min = 0.0

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

    def _convert_one_to_product(self, elasticsearch_result):
        product_data = elasticsearch_result["_source"]
        images = [FileWithPath(product_image["file_name"], product_image["file_path"]) for
                  product_image in product_data["images"]]
        return ProductElasticsearch(product_data["owner_id"], product_data["product_name"],
                                    product_data["description"], product_data["is_visible"],
                                    product_data["price"], elasticsearch_result["_id"], images,
                                    self.get_user_by_id)

    def convert_es_to_product(self, result) -> List[ProductElasticsearch]:
        if result is not None and len(result["hits"]["hits"]) > 0:
            return [self._convert_one_to_product(hit) for hit in result["hits"]["hits"]]
        else:
            return []

    def init_db(self, number_of_replicas=0):
        database: Elasticsearch = self.es
        if not database.indices.exists(self.USERS_INDEX):
            # Create an index to store the user information including including
            # their name, email and hashed password
            database.indices.create(self.USERS_INDEX, {"mappings": {
                "properties": {"name": {"type": "text"}, "email": {"type": "keyword"},
                               "password": {"type": "text", "index": False}, }},
                "settings": {"number_of_replicas": number_of_replicas}})
        if not database.indices.exists(self.IMAGES_INDEX):
            # Create an index to store the image product data
            database.indices.create(self.IMAGES_INDEX, {"mappings": {
                "properties": {"product_name": {"type": "keyword"}, "description": {"type": "text"},
                               "owner_id": {"type": "keyword", }, "is_visible": {"type": "boolean"},
                               "price": {"type": "double"}, "images": {"type": "nested"}}},
                "settings": {"number_of_replicas": number_of_replicas}})
