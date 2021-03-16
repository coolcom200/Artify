import uuid

from sqlalchemy.dialects.postgresql import UUID

from . import sql_alchemy_db

MAX_NAME_LENGTH = 255
MAX_EMAIL_LENGTH = 255


class UserPg(sql_alchemy_db.Model):
    __tablename__ = "user"
    uid = sql_alchemy_db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = sql_alchemy_db.Column(sql_alchemy_db.String(MAX_NAME_LENGTH), nullable=False)
    email = sql_alchemy_db.Column(sql_alchemy_db.String(MAX_EMAIL_LENGTH), nullable=False,
                                  unique=True, index=True)
    passwordHash = sql_alchemy_db.Column("product_hash", sql_alchemy_db.String, nullable=False)

    products = sql_alchemy_db.relationship("ProductPg", back_populates="owner", lazy=True)


class ProductPg(sql_alchemy_db.Model):
    __tablename__ = "product"
    uid = sql_alchemy_db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    ownerUid = sql_alchemy_db.Column("owner_uid", UUID(as_uuid=True),
                                     sql_alchemy_db.ForeignKey("user.uid"), nullable=False)
    productName = sql_alchemy_db.Column("product_name", sql_alchemy_db.String(MAX_NAME_LENGTH),
                                        nullable=False, index=True)
    description = sql_alchemy_db.Column(sql_alchemy_db.Text, nullable=False, index=True)
    isVisible = sql_alchemy_db.Column("is_visible", sql_alchemy_db.Boolean, nullable=False)
    price = sql_alchemy_db.Column(sql_alchemy_db.Float, nullable=False)

    owner = sql_alchemy_db.relationship("UserPg", back_populates="products", lazy=True)
    images = sql_alchemy_db.relationship("FilePg", back_populates="products", lazy=True)


class FilePg(sql_alchemy_db.Model):
    __tablename__ = "file"
    fileUid = sql_alchemy_db.Column("file_uid", UUID(as_uuid=True), nullable=False,
                                    primary_key=True, default=uuid.uuid4())
    productUid = sql_alchemy_db.Column("product_uid", UUID(as_uuid=True),
                                       sql_alchemy_db.ForeignKey("product.uid"), nullable=False)
    fileName = sql_alchemy_db.Column("file_name", sql_alchemy_db.String(MAX_NAME_LENGTH),
                                     nullable=False)
    filePath = sql_alchemy_db.Column("file_path", sql_alchemy_db.Text, nullable=False)

    products = sql_alchemy_db.relationship("ProductPg", back_populates="images", lazy=True)
