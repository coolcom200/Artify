from dataclasses import dataclass
from typing import List, Callable

from api.models.common_models import FileWithPath


@dataclass
class UserElasticsearch:
    name: str
    email: str
    uid: str
    passwordHash: str

    def __init__(self, elasticsearch_result, get_products: Callable):
        user_data = elasticsearch_result["_source"]
        self.name = user_data["name"]
        self.email = user_data["email"]
        self.uid = elasticsearch_result["_id"]
        self.passwordHash = user_data["password_hash"]
        self.get_products = get_products

    @property
    def products(self):
        return self.get_products(self.uid)


@dataclass
class ProductElasticsearch:
    ownerId: str
    productName: str
    description: str
    isVisible: bool
    price: float
    uid: str
    images: List[FileWithPath]

    def __init__(self, owner_id: str, product_name: str, description: str, is_visible: bool,
                 price: float, uid: str, images: List[FileWithPath], get_owner: Callable):
        self.uid = uid
        self.ownerId = owner_id
        self.productName = product_name
        self.description = description
        self.isVisible = is_visible
        self.price = price
        self.images = images
        self.get_owner = get_owner

    @property
    def owner(self):
        return self.get_owner(self.ownerId)
