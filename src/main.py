from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    settings = get_settings()
    app.state.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.state.db_client = app.state.mongo_conn[settings.MONGODB_DATABASE]

    yield

    app.state.mongo_conn.close()
    # --- Shutdown (Optional: Close connection here if needed) ---
    # app.mongo_conn.close()


app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)
