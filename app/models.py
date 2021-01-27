from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float(precision=2))

    stock = relationship("Stock", back_populates="item")

class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)

    stock = relationship("Stock", back_populates="shop")

class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    item_id = Column(Integer, ForeignKey('items.id'))
    shop_id = Column(Integer, ForeignKey('shops.id'))

    item = relationship("Item", back_populates="stock")
    shop = relationship("Shop", back_populates="stock")


