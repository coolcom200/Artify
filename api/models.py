from dataclasses import dataclass
from typing import List

@dataclass
class User:
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
class FileWithPath:
    data: dict

    def __init__(self, file_name, file_path):
        self.data = {"file_name": file_name, "file_path": file_path}

    def to_dict(self):
        return self.data


@dataclass
class Product:
    owner_id: str
    product_name: str
    description: str
    is_visible: bool
    price: float
    uid: str
    images: List[FileWithPath]

    def __init__(self, elasticsearch_result):
        product_data = elasticsearch_result["_source"]
        self.uid = elasticsearch_result["_id"]
        self.owner_id = product_data["owner_id"]
        self.product_name = product_data["product_name"]
        self.description = product_data["description"]
        self.is_visible = product_data["is_visible"]
        self.price = product_data["price"]
        self.images = product_data["images"]
