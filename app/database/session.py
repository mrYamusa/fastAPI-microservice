from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from rich import panel, print
from fastapi import Depends
from typing import Annotated


engine = create_engine(
    url="sqlite:///sqlite.db", connect_args={"check_same_thread": False}, echo=True
)


def create_db_tables():
    from .models import Shipments

    SQLModel.metadata.create_all(bind=engine)
    print(
        panel.Panel(
            renderable="Shipment database created successfully...", style="bold green"
        )
    )


def create_session():
    with Session(bind=engine) as session:
        print(
            panel.Panel(
                renderable="Session started successfully...", style="bold green"
            )
        )
        yield session
        print(
            panel.Panel(renderable="Session stopped successfully...", style="bold red")
        )


SessionDep = Annotated[Session, Depends(create_session)]
# session = Session(bind=engine)
# session.get(Shipments, 4)
# session.add(Shipments(content="Book", weight=2.5, status="Placed"))
# session.commit()
