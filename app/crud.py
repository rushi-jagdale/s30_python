from sqlalchemy.orm import Session

from .models import Address
from .schema import AddressCreate, AddressUpdate
from typing import Union
from math import sin, cos, sqrt, atan2

R = 6373.0


def list_Address(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Address).offset(skip).limit(limit).all()


def get_Address(db: Session, id: int):
    return db.query(Address).get(id)

def closest(lst, K):      
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

def get_address_by_distance(actual_distance: float, lat:float, long:float, db: Session):
    # print(db.query(Address).filter(Address.distance == distance))
    print(actual_distance) 
    lat_long_lst=[]
    distance_lst=[]
    lat1 = lat
    lon1 = long
    # lat2 = 52.406374
    # lon2 = 16.9251681
    obj = db.query(Address.latitude, Address.longitude)
    dis = db.execute(obj).fetchall()
    print(dis)  
    for i in range(len(dis)): 
        latlong =dis[i]
        for j in range(len(latlong)):
            lat_long_lst.append(latlong[j])

        # print(latlong)      
    lat2 = lat_long_lst[::2]
    lon2 = lat_long_lst[1::2] 
    print(lat2)
    print(lon2)
    for i in range(len(lat2)):
        dlon = lon2[i] - lon1
        dlat = lat2[i] - lat1
        a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2[i]) * (sin(dlon/2))**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        distance_lst.append(distance)
    closest_distance=closest(distance_lst, actual_distance) 
    print(f"clsd{closest_distance}")  
    # data = db.query(Address).all()
    
    # obj = db.query(Address.distance, Address.address).where(Address.distance==distance)
    # dis = db.execute(obj).fetchone()
  
    # print(db.query(Address.address).where(Address.distance))           
    return None


def create_Address(db: Session, data: AddressCreate):
    db_Address = Address(**data.dict())
    db.add(db_Address)
    db.commit()
    db.refresh(db_Address)
    return db_Address


def drop_Address(db: Session, Address_id: int):
    db.query(Address).filter(Address.id == Address_id).delete()
    db.commit()
    return None


def update_Address(db: Session, Address: Union[int, Address], data: AddressUpdate):
    if isinstance(Address, int):
        Address = get_Address(db, Address)
    if Address is None:
        return None
    for key, value in data:
        setattr(Address, key, value)
    db.commit()
    return Address
