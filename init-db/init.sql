-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the embeddings table for LangChain
CREATE TABLE IF NOT EXISTS langchain_pg_embedding (
    langchain_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),  -- Auto-generate UUIDs
    content text,                                             -- Raw text chunk
    embedding vector(1536),                                    -- Vector dimension matches embedding model
    langchain_metadata jsonb                                        -- Optional human-readable ID
);


-- Create the products table
CREATE TABLE IF NOT EXISTS products (
    id VARCHAR PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price NUMERIC,
    category TEXT,
    image_url TEXT
);