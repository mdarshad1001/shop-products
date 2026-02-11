import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base
from langchain_openai import OpenAIEmbeddings
from langchain_postgres.v2.async_vectorstore import AsyncPGVectorStore
from langchain_postgres.v2.engine import PGEngine

Base = declarative_base()

# Async Engine
ASYNC_ENGINE: AsyncEngine = create_async_engine(
    os.getenv("DATABASE_URL"),
    pool_pre_ping=True,
    future=True,
)

# PGEngine for vector store
PG_ENGINE = PGEngine.from_engine(ASYNC_ENGINE)

# Async Session
AsyncSessionLocal = sessionmaker(ASYNC_ENGINE, class_=AsyncSession)

# Vector Store #embedding object
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    )

async def get_vector_store() -> AsyncPGVectorStore:
    return await AsyncPGVectorStore.create(
        engine=PG_ENGINE,
        embedding_service=embeddings,
        table_name="langchain_pg_embedding",
    )