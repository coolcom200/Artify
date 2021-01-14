from abc import ABC, abstractmethod
from api.user import User


class DatabaseInterface(ABC):

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def init_db(self):
        pass

    @abstractmethod
    def get_user_by_id(self, id) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, email) -> User:
        pass

    @abstractmethod
    def create_user(self, email, name, password_hash) -> str:
        pass

    @abstractmethod
    def create_product_details(self, owner_id: str, title: str, desc: str, is_visible: bool, price: float, list_image_details):
        pass

    @abstractmethod
    def get_visible_products(self, page=1, size=25):
        pass

    @abstractmethod
    def search(self, query: str, price_min: float, price_max: float):
        pass