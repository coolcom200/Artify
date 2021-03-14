from abc import ABC, abstractmethod
from typing import Optional


class DatabaseInterface(ABC):

    @abstractmethod
    def get_user_by_id(self, id):
        pass

    @abstractmethod
    def get_user_by_email(self, email):
        pass

    @abstractmethod
    def create_user(self, email, name, password_hash):
        pass

    @abstractmethod
    def create_product_details(self, owner_id: str, title: str, desc: str, is_visible: bool,
                               price: float, list_image_details):
        pass

    @abstractmethod
    def get_products(self, query: Optional[str], price_min: Optional[float],
                     price_max: Optional[float] = None):
        pass
