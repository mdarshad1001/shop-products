from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import asyncio
import time
import traceback

from .search import search_products_async
from .vectorization import run_vectorize_async

# Create FastAPI app directly
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Track vectorize concurrency
_vectorize_lock = asyncio.Lock()

class SearchQuery(BaseModel):
    query: str
    category: str = None

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search")
def search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.post("/vectorize")
async def vectorize():
    start = time.perf_counter()
    async with _vectorize_lock:
        try:
            stats = await run_vectorize_async()
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)

    elapsed = time.perf_counter() - start
    print(f"⏱️ /vectorize execution took {elapsed:.2f} seconds")

    return {
        "message": "Products vectorized successfully!",
        "stats": stats
    }

@app.post("/search")
async def search(q: SearchQuery):
    start = time.perf_counter()
    try:
        answer, products, contexts = await search_products_async(q.query)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)

    elapsed = time.perf_counter() - start
    print(f"⏱️ /search execution took {elapsed:.2f} seconds")

    return {
        "answer": answer,
        "products": products,
        "contexts": contexts
    }