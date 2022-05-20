from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from google.protobuf.json_format import MessageToDict, ParseDict
from . import models, crud, schema
from .db import engine, SessionLocal

# Auto creation of database tables
#   If tables already exist, this command does nothing. This allows to
#   safely execute this command at any restart of the application.
#   For a better management of the database schema
models.Base.metadata.create_all(bind=engine)

# Application bootstrap
app = FastAPI()


# This function represents a dependency that can be injected in the endpoints of the API.
# Dependency injection is very smart, as it allows to declaratively require some service.
# This function models the database connection as a service, so that it can be required
# just when needed.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# LIST
# This endpoint returns a list of objects of type `Address` serialized using the `Address` schema that
# we defined in schemas.py. The objects exposed are instances of `models.Address` that are
# validated and serialized as of the definition of the schema `schemas.Address`
@app.get("/address", response_model=List[schema.Address])
def address_action_list(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    address = crud.list_Address(db, offset, limit)
    return address

# RETRIEVE
# This endpoint returns a specific `Address`, given the value of its `id` field,


@app.get("/address/{address_id}", response_model=schema.Address)
def addresss_action_retrieve(address_id: int, db: Session = Depends(get_db)):
    address = crud.get_Address(db, address_id)
    if address is None:
        raise HTTPException(status_code=404)
    return address


# RETRIEVE
# This endpoint returns a specific `Address`, given the value of its `distance` field,

@app.get("/distance/{distance}/{lat}/{long}")
def addresss_distance_retrieve(distance: float, lat:float, long:float, db: Session = Depends(get_db)):    
    address = crud.get_address_by_distance(distance, lat, long, db)   
    print(address)
    if address is None:
        raise HTTPException(status_code=404)
    # print(address.distance)     
    return address

# CREATE
# This endpoint creates a new `Address`. The necessary data is read from the request


@app.post("/address", response_model=schema.AddressCreate)
def address_action_create(data: schema.AddressCreate, db: Session = Depends(get_db)):
    print(data)
    response_dic = {}
    address_object = crud.create_Address(db, data)
    response_dic = {"name": address_object.name,  "address": address_object.address, "latitude": address_object.latitude,  "longitude": address_object.longitude}
    return response_dic


# UPDATE
# This endpoint allows to update an existing `Address`, identified by its primary key passed as a
# path parameter in the url. The necessary data is read from the request
# body, which is parsed and validated according to the AddressUpdate schema defined beforehand
@app.put("/address/{address_id}", response_model=schema.Address)
def address_action_retrieve(address_id: int, data: schema.AddressUpdate,  db: Session = Depends(get_db)):
    address = crud.update_Address(db, address_id, data)
    if address is None:
        raise HTTPException(status_code=404)
    return address


# DELETE
# This endpoint allows to delete an `Address`, identified by its primary key passed as a
# path parameter in the url. It's worth observing that the status code of the response is
# HTTP 204 No Content, since the response body is empty
@app.delete("/address/{address_id}", status_code=204)
def Address_action_delete(address_id: int,  db: Session = Depends(get_db)):
    crud.drop_Address(db, address_id)
    return None
