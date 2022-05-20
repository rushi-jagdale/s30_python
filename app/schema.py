from typing import Optional
from pydantic import BaseModel


class AddressCreate(BaseModel):
    name: str
    address: str  
    latitude: float   
    longitude: float
    

class AddressUpdate(BaseModel):
    name: str
    address: str  
    latitude: float   
    longitude: float
 


class Address(BaseModel):
    name: str
    address: str  
    latitude: float   
    longitude: float
    id: int
    class Config:
        orm_mode = True
