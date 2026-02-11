from sqlalchemy import Column, String, Text, Numeric
import uuid

from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric(10, 2))
    category = Column(Text)
    image_url = Column(Text)