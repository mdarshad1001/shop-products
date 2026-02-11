import os
import pandas as pd
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy.dialects.postgresql import insert
from langchain_postgres.v2.indexes import HNSWIndex, DistanceStrategy

from .database import get_vector_store
from .models import Product

UPLOAD_DIR = os.getenv('UPLOAD_FOLDER', 'uploads')

#step1: Load docs
def _load_csv(filepath: str) -> pd.DataFrame:
    """Load and validate CSV file"""
    df = pd.read_csv(filepath, dtype={"id": str})
    
    required_columns = ['id', 'name', 'description', 'price', 'category', 'image_url']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    return df

def _prepare_documents(df: pd.DataFrame) -> tuple:
    """Prepare texts and metadata for vectorization"""
    product_texts = []
    metadatas = []
    
    for _, row in df.iterrows():
        product_texts.append(f"{row['name']} {row['description']}")
        metadatas.append({
            "product_id": str(row["id"]),
            "category": str(row["category"])})
    
    return product_texts, metadatas

# step 2: chunk
def _chunk_documents(texts, metadatas):
    """Split texts into chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.create_documents(texts, metadatas=metadatas)

async def _store_products(df: pd.DataFrame):
    """Store products in database"""
    from .database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        for _, row in df.iterrows():
            stmt = (
                insert(Product)
                .values(
                    id=row["id"],
                    name=row["name"],
                    description=row["description"],
                    price=row["price"],
                    category=row["category"],
                    image_url=row["image_url"],
                )
            )
            await db.execute(stmt)
        await db.commit()

async def _create_index(store):
    """Create vector index"""
    #TODO

async def run_vectorize_async() -> dict:
    """Main vectorization function"""
    # Load CSV from uploads folder
    csv_files = list(Path(UPLOAD_DIR).glob("*.csv"))
    if not csv_files:
        raise ValueError("No CSV files found in uploads folder")
    
    filepath = csv_files[0]  # Use first CSV file found
    df = _load_csv(str(filepath))
    
    # Store products in database
    await _store_products(df)
    
    # Prepare documents for vectorization
    texts, metadatas = _prepare_documents(df)
    #Chunk and get documents
    #Get Vector Store
    documents = _chunk_documents(texts, metadatas)

    #Store Docs
    # Store vectors
    store = await get_vector_store()
    await store.aadd_documents(documents)

   #Return products and chunks
    return {
        "products": len(df),
        "chunks": len(documents)
    }
