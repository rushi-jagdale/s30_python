from tokenize import Double
from sqlalchemy import Column, Float, Integer, String
from .db import Base


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address= Column(String)    
    latitude = Column(Float)
    longitude = Column(Float)
   
