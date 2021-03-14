import uuid
from typing import Optional

from flask_sqlalchemy import SQLAlchemy

from api.models.sql_models import UserPg, FilePg, ProductPg
from .database_interface import DatabaseInterface


class PostgresDatabase(DatabaseInterface):
    def __init__(self, sql_alchemy: SQLAlchemy):
        self.sql_alchemy = sql_alchemy

    def get_user_by_id(self, id) -> Optional[UserPg]:
        user = UserPg.query.get(id)
        return user

    def get_user_by_email(self, email) -> Optional[UserPg]:
        return UserPg.query.filter_by(email=email).first()

    def create_user(self, email, name, password_hash) -> str:
        new_user = UserPg(email=email, name=name, passwordHash=password_hash)
        self.sql_alchemy.session.add(new_user)
        self.sql_alchemy.session.commit()
        return new_user.uid

    def create_product_details(self, owner_id: str, title: str, desc: str, is_visible: bool,
                               price: float, list_image_details) -> Optional[ProductPg]:
        new_product = ProductPg(uid=uuid.uuid4(), ownerUid=owner_id, productName=title,
                                description=desc, isVisible=is_visible, price=price)
        for image in list_image_details:
            imageFile = FilePg(productUid=new_product.uid, fileName=image.fileName,
                               filePath=image.filePath)
            self.sql_alchemy.session.add(imageFile)
            new_product.images.append(imageFile)
        self.sql_alchemy.session.add(new_product)
        self.sql_alchemy.session.commit()
        return new_product

    def get_products(self, query: Optional[str], price_min: Optional[float],
                     price_max: Optional[float] = None):
        conditions = []
        if query is not None:
            conditions.append(ProductPg.productName.contains(query))
        if price_min is not None:
            conditions.append(ProductPg.price >= price_min)
        if price_max is not None:
            conditions.append(ProductPg.price <= price_max)

        return ProductPg.query.filter(*conditions).all()
