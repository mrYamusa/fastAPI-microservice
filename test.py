from fastapi import FastAPI
from contextlib import asynccontextmanager
from rich import panel, print


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Starting up Yamusa's server...", border_style="green"))
    yield
    print(panel.Panel("Shutting down Yamusa's server...", border_style="red"))


app = FastAPI(title="Mr Yamusa's FastAPI Shipment Service", lifespan=lifespan_handler)


@app.get("/{word}")
def read_root(word: str):
    return {"Hello": word}
