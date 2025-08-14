import uvicorn
from fastapi import FastAPI

from api.v1 import consumables

app = FastAPI()

app.include_router(consumables.router)

if __name__ == "__main__":
    uvicorn.run("main:app")
