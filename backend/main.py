import uvicorn
from fastapi import FastAPI

from app.models.database import database
from app.routers import tasks, users


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(users.router)
app.include_router(tasks.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
