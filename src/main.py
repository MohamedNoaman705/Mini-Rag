from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes import base, data, nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from stores.llm.templates.template_parser import TemplateParser
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    # --- Startup ---
    settings = get_settings()

    # 1. Database Connections (Attached to app_instance.state)
    postgres_conn = f"postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_MAIN_DATABASE}"

    app_instance.state.db_engine = create_async_engine(postgres_conn)

    app_instance.state.db_client = sessionmaker(
        app_instance.state.db_engine, class_=AsyncSession, expire_on_commit=False
    )

    # 2. LLM Provider Factory & Clients Setup
    llm_provider_factory = LLMProviderFactory(settings)
    vectordb_provider_factory = VectorDBProviderFactory(settings)

    # Generation Client
    app_instance.state.generation_client = llm_provider_factory.create(
        provider_name=settings.GENERATION_BACKEND
    )
    if app_instance.state.generation_client:
        app_instance.state.generation_client.set_generation_model(
            model_id=settings.GENERATION_MODEL_ID
        )

    # Embedding Client
    app_instance.state.embedding_client = llm_provider_factory.create(
        provider_name=settings.EMBEDDING_BACKEND
    )
    if app_instance.state.embedding_client:
        app_instance.state.embedding_client.set_embedding_model(
            model_id=settings.EMBEDDING_MODEL_ID,
            embedding_size=settings.EMBEDDING_MODEL_SIZE,
        )

    # vectorDB
    app_instance.state.vectordb_client = vectordb_provider_factory.create(
        provider=settings.VECTOR_DB_BACKEND
    )
    app_instance.state.vectordb_client.connect()

    app_instance.state.template_parser = TemplateParser(
        language=settings.DEFAULT_LANG
    )

    yield

    # --- Shutdown ---
    await app_instance.state.db_engine.dispose()
    app_instance.state.vectordb_client.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)