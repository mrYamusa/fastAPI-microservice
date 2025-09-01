from scalar_fastapi import get_scalar_api_reference
from fastapi import FastAPI, HTTPException, status
from typing import Any
from app.schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate, ShipmentStatus
from .database import shipments, save
# from pydantic import BaseModel

app = FastAPI()

# shipments: dict[int, dict[str, Any]] = {
#     123: {
#         "weight": 1.2,
#         "content": "Wooden table",
#         "status": "In Transit",
#     },
#     124: {
#         "weight": 5.7,
#         "content": "M4 Mac Book",
#         "status": "In Transit",
#     },
#     125: {
#         "weight": 3.9,
#         "content": "Furniture",
#         "status": "Delivered",
#     },
#     126: {
#         "weight": 9.4,
#         "content": "Glass Plaque",
#         "status": "In Transit",
#     },
#     127: {
#         "weight": 8.5,
#         "content": "Hover Board",
#         "status": "Delivered",
#     },
# }


class City:
    def __init__(self, name, location) -> None:
        self.name: str = name
        self.location: int = location


@app.post("/shipment")  # , response_model=ShipmentCreate)
def submit_shipment(body: ShipmentCreate) -> dict[str, int]:
    if body.weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Weight is above shipment limits! \nMaximum weight limit is 25",
        )
    new_id: int = max(shipments.keys()) + 1
    # print(dict(body))
    # shipments[new_id] = dict(body)
    # shipments[new_id]["status"] = "Placed!"
    # print(shipments[new_id])
    shipments[new_id] = {
        **body.model_dump(),
        "id": new_id,
        "status": ShipmentStatus.placed,
    }
    save()
    return {"id": new_id}
    # return ShipmentCreate(**shipments[new_id])


@app.get("/shipment/latest")
async def get_latest_shipment() -> dict[str, Any]:
    id = max(shipments.keys())
    print(len(shipments), id)
    return shipments[id]


@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int) -> ShipmentRead:
    print(shipment_dict)
    if id not in shipments.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The ID {id} you provided doesn't exist",
        )
        # return {"Error": f"The ID {id} you provided doesn't exist"}
    return ShipmentRead(**shipments[id])


@app.get("/shipment/{id}/")
async def shipment_fields(id: int, feild: str):
    return shipments[id][feild]


@app.put("/shipment")
def shipment_update(
    id: int, content: str, weight: float, status: str
) -> dict[str, Any]:
    shipments[id] = {"content": content, "weight": weight, "status": status}
    return shipments[id]


# @app.patch("/shipment")
# def shipment_patch(
#     id: int,
#     content: str | None = None,
#     weight: float | None = None,
#     status: str | None = None,
# ) -> dict[str, Any]:
#     shipment = shipments[id]
#     if content:
#         shipment["content"] = content

#     if weight:
#         shipment["weight"] = weight

#     if status:
#         shipment["status"] = status
#     shipments[id] = shipment
#     return shipments[id]
# async def shipment_patch(id: int, body: dict[str, Any]):


@app.patch("/shipment", response_model=ShipmentRead)
async def shipment_patch(id: int, body: ShipmentUpdate):  # dict[str, ShipmentStatus]):
    print("@" * 25)
    # print(f"{shipments[id].update(body)}")
    print(shipments[id].update(body.model_dump(exclude_none=True)))
    shipments[id].update(body.model_dump(exclude_none=True, exclude_defaults=False))
    print("@" * 25)
    save()
    return shipments[id]
    # return ShipmentRead(**shipments[id])


@app.delete("/shipment")
async def delete_shipment(id: int) -> dict[str, str]:
    shipments.pop(id)
    return {"Detail": f"Shipment with #{id} has been deleted Successfully"}


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


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
