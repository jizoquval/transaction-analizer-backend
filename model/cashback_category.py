from dataclasses import dataclass
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, Float
from model.database import Base


@dataclass
class Category(Base):
    id: int
    name: str
    cashback: float

    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cashback = Column(Float)

    def __repr__(self):
        return f'Category: {self.name} Cashback: {self.cashback}'