from abc import ABC, abstractmethod
from typing import Optional, List

from models import User, Product


class DatabaseInterface(ABC):

    @abstractmethod
    def get_user_by_id(self, id) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_email(self, email) -> Optional[User]:
        pass

    @abstractmethod
    def create_user(self, email, name, password_hash) -> str:
        pass

    @abstractmethod
    def create_product_details(self, owner_id: str, title: str, desc: str,
                               is_visible: bool, price: float,
                               list_image_details) -> Optional[Product]:
        pass

    @abstractmethod
    def get_products(self, query: str, price_min: float,
                     price_max: Optional[float] = None) -> List[Product]:
        pass
