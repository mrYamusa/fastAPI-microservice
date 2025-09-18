from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum


class ShipmentStatus(str, Enum):
    placed = "Placed!"
    in_transit = "In Transit"
    out_for_delivery = "Out for Delivery"
    delivered = "Delivered"


class Shipments(SQLModel, table=True):
    __tablename__ = "Shipments"
    id: int = Field(primary_key=True)
    content: str
    weight: float = Field(le=25)
    status: ShipmentStatus = Field(default=ShipmentStatus.placed)
    estimated_delivery: datetime
