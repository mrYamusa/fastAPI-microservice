from scalar_fastapi import get_scalar_api_reference
from fastapi import FastAPI, HTTPException, status, Depends
from typing import Any
from app.database.session import SessionDep, create_db_tables
from sqlmodel import Session
from app.schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate  # , ShipmentStatus
from rich import panel, print

# from pydantic import BaseModel
from app.database.models import Shipments
from contextlib import asynccontextmanager  # for lifespan event handler


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Starting up shipment server...", style="bold green"))
    create_db_tables()
    yield
    print(panel.Panel("Shutting down shipment server...", style="bold red"))


app = FastAPI(lifespan=lifespan_handler, title="Yamusa's Shipment API", version="0.1.0")
# db = Database()


class City:
    def __init__(self, name, location) -> None:
        self.name: str = name
        self.location: int = location


@app.post("/shipment")  # , response_model=ShipmentCreate)
def submit_shipment(body: ShipmentCreate, session: SessionDep):
    if body.weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Weight is above shipment limits! \nMaximum weight limit is 25",
        )
    body_content = Shipments(**body.model_dump(exclude_none=False))
    session.add(body_content)
    session.commit()
    session.refresh(body_content)
    return body_content


# @app.get("/shipment/latest")
# async def get_latest_shipment():  # -> dict[str, Any]:
#     id = db.max_id()
#     shipment = db.read_shipments(id)
#     db.close()
#     return shipment


# @app.get("/shipment", response_model=ShipmentRead)
# def get_shipment(id: int):  # -> ShipmentRead:
#     shipment = db.read_shipments(id=id)
#     db.close()
#     if shipment is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"The ID {id} you provided doesn't exist",
#         )
#     return shipment


# @app.put("/shipment")
# def shipment_update(id: int, shipment: ShipmentUpdate):  # -> dict[str, Any]:
#     # shipments[id] = {"content": content, "weight": weight, "status": status}
#     shipment = db.update_shipment(id=id, shipment=shipment)
#     # db.close()
#     return shipment


# @app.patch("/shipment", response_model=ShipmentRead)
# async def shipment_patch(id: int, body: ShipmentUpdate):  # dict[str, ShipmentStatus]):
#     shipment = db.update_shipment(id=id, shipment=body)
#     db.close()
#     return shipment


# @app.delete("/shipment")
# async def delete_shipment(id: int) -> dict[str, str]:
#     db.delete_shipment(id=id)
#     return {"Detail": f"Shipment with #{id} has been deleted Successfully"}


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
