from dataclasses import dataclass
from typing import List

from api.models.common_models import FileWithPath


@dataclass
class UserElasticsearch:
    name: str
    email: str
    uid: str
    password_hash: str

    def __init__(self, elasticsearch_result):
        user_data = elasticsearch_result["_source"]
        self.name = user_data["name"]
        self.email = user_data["email"]
        self.uid = elasticsearch_result["_id"]
        self.password_hash = user_data["password_hash"]


@dataclass
class ProductElasticsearch:
    owner_id: str
    product_name: str
    description: str
    is_visible: bool
    price: float
    uid: str
    images: List[FileWithPath]

    def __init__(self, owner_id: str, product_name: str, description: str, is_visible: bool,
                 price: float, uid: str, images: List[FileWithPath]):
        self.uid = uid
        self.owner_id = owner_id
        self.product_name = product_name
        self.description = description
        self.is_visible = is_visible
        self.price = price
        self.images = images
