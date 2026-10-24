from fastapi import APIRouter, Depends, Request
from helpers.config import get_settings, Settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api"],
)

@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):
    app_name = app_settings.APP_NAME
    return {
        "welcome": app_name,
    }

@base_router.get("/models/status")
async def check_models_status(request: Request):
    generation_client = getattr(request.app.state, "generation_client", None)
    embedding_client = getattr(request.app.state, "embedding_client", None)

    return {
        "generation_provider": type(generation_client).__name__ if generation_client else None,
        "generation_model_id": getattr(generation_client, "generation_model_id", None),

        "embedding_provider": type(embedding_client).__name__ if embedding_client else None,
        "embedding_model_id": getattr(embedding_client, "embedding_model_id", None),
        "embedding_size": getattr(embedding_client, "embedding_size", None),
    }