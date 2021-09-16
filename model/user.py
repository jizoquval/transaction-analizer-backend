from dataclasses import dataclass
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer
from model.database import Base


@dataclass
class User(Base):
    party_rk: int

    __tablename__ = "user"

    party_rk = Column(Integer, primary_key=True)

    def __repr__(self):
        return f'User: {self.party_rk}'