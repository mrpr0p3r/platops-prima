from sqlalchemy import Column, String, Integer, Date
from base import Base


class People(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    def __init__(self, name, age):
        self.name = name
        self.age = age