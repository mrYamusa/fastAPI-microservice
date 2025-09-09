from scalar_fastapi import get_scalar_api_reference
from fastapi import FastAPI, HTTPException, status
from typing import Any
from app.schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate  # , ShipmentStatus
from .database import Database
# from pydantic import BaseModel

app = FastAPI()
db = Database()


class City:
    def __init__(self, name, location) -> None:
        self.name: str = name
        self.location: int = location


@app.post("/shipment")  # , response_model=ShipmentCreate)
def submit_shipment(body: ShipmentCreate):  # -> dict[str, int]:
    if body.weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Weight is above shipment limits! \nMaximum weight limit is 25",
        )
    new_id = db.create_shipment(shipment=body)
    shipment = db.read_shipments(id=new_id)
    db.close()
    return shipment


@app.get("/shipment/latest")
async def get_latest_shipment():  # -> dict[str, Any]:
    id = db.max_id()
    shipment = db.read_shipments(id)
    db.close()
    return shipment


@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int):  # -> ShipmentRead:
    shipment = db.read_shipments(id=id)
    db.close()
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The ID {id} you provided doesn't exist",
        )
    return shipment


# @app.get("/shipment/{id}/")
# async def shipment_fields(id: int, field: str):
#     return shipments[id][field]


@app.put("/shipment")
def shipment_update(id: int, shipment: ShipmentUpdate):  # -> dict[str, Any]:
    # shipments[id] = {"content": content, "weight": weight, "status": status}
    shipment = db.update_shipment(id=id, shipment=shipment)
    # db.close()
    return shipment


@app.patch("/shipment", response_model=ShipmentRead)
async def shipment_patch(id: int, body: ShipmentUpdate):  # dict[str, ShipmentStatus]):
    shipment = db.update_shipment(id=id, shipment=body)
    db.close()
    return shipment
    # print(shipments[id].update(body.model_dump(exclude_none=True)))
    # shipments[id].update(body.model_dump(exclude_none=True, exclude_defaults=False))
    # return shipments[id]
    # return ShipmentRead(**shipments[id])


@app.delete("/shipment")
async def delete_shipment(id: int) -> dict[str, str]:
    db.delete_shipment(id=id)
    return {"Detail": f"Shipment with #{id} has been deleted Successfully"}


"""
def adlibs(adlib: str):
    def no_turning_back(func):
        def wrapper_func():
            print(f"I will never turn back o \n{adlib}")
            func()
            print(f"It's already too late o \n{adlib}")

        return wrapper_func

    return no_turning_back


@app.get("/order")
async def get_new_shipment(id: int | None = None) -> dict[str, Any]:
    print(shipment_dict)

    if not id:
        id = max(shipments.keys())
        return shipments[id]

    if id not in shipments.keys():
        # return {"Error": f"The ID {id} you provided doesn't exist"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given ID Doesn't Exist!"
        )
    return shipments[id]


# Type hinting
async def add(a: int | float, b: int | bool):
    x = 0.5 if a < 5 else a
    return {
        "Answer": f"{x + b}",
    }


# modern python
digits: list[int] = [1, 2, 3, 4, 5, 6]
table_5: tuple[int, ...] = (9, 8, 7, 6, 5, 4, 3)
shipment_dict: dict[str, Any] = {
    "ID": 127609,
    "Weight": 12.5,
    "Content": "Nike AirForce 1 Fiesta Breds",
    "Status": "In Transit",
}
Hampshire = City("Hampshire", 2408664)
city_temp: tuple[City, int] = (Hampshire, 78)


def nuation(nuat: str = "!!"):
    def run(func):
        def wrapper_func():
            print(f"Running...{nuat}")
            func()
            print(f"Running...{nuat}")

        return wrapper_func

    return run


@nuation("??")
def slide():
    print("Slide 🤾‍♂️...")


@app.get("/transit/")
def get_transit():
    slide()
    return {
        "content": "Map",
        "status": "Following --- route...",
    }

"""


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
