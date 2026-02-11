# 🧠 SmartFind: AI-Powered Product Search with Flask, LangChain, and pgvector

SmartFind is a full-stack AI application that enables intelligent product search using vector embeddings. Upload a CSV of products, and let the app store their embeddings in PostgreSQL with `pgvector`. Then, use OpenAI-powered semantic search to find the most relevant products based on natural language queries.

---

## 🚀 Features

- Upload and parse product CSVs with metadata
- Generate embeddings using OpenAI models
- Store data and vectors in PostgreSQL (`pgvector`)
- Perform semantic vector search with LangChain
- Run using Docker and Docker Compose

---

## 📁 Project Structure

```
smartfind/
├── app/
│   ├── __init__.py              # App factory
│   ├── api/
│   │   ├── search.py            # Search API
│   │   └── vectorization.py     # File upload + embedding logic
│   ├── config.py                # Flask + environment configs
│   ├── database.py              # SQLAlchemy + PGVector init
│   ├── models.py                # SQLAlchemy models
│   ├── utils.py                 # Helpers (e.g., file type check)
│   └── templates/
│       └── index.html           # Frontend template
├── init-db/
│   └── init.sql                 # DB schema and index creation
├── product_real_data.csv        # Sample product data
├── .env                         # Secrets (OpenAI key, DB URL)
├── Dockerfile                   # Flask app Docker config
├── docker-compose.yml           # Multi-container setup
├── requirements.txt             # Python dependencies
└── run.py                       # Entrypoint for Flask app
```

---

## 🧪 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/yourname/smartfind.git
cd smartfind
```

### 2. Add Your API Key

Update `.env`:
```env
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/postgres
```

### 3. Start the App with Docker

```bash
docker-compose up --build
```

The app will be available at: [http://localhost:5000](http://localhost:5000)

---

## 📄 CSV Format

Ensure your uploaded CSV follows this format:

| id | name         | description             | price | category  | image_url           |
|----|--------------|--------------------------|-------|-----------|----------------------|
| 1  | Apple Watch  | Smart wearable device    | 299   | Electronics| http://example.com/1 |
| 2  | Leather Bag  | Stylish and durable bag  | 150   | Fashion   | http://example.com/2 |

---

## 🔍 How It Works

- **Upload Page**: Upload a CSV → parses data → generates embeddings
- **Database**: Vectors and metadata stored in `product_embeddings` table
- **Search**: Uses OpenAI + LangChain’s `PGVector` to return top results

---

## 🧱 Built With

- [Flask](https://flask.palletsprojects.com/)
- [LangChain](https://www.langchain.com/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [PostgreSQL](https://www.postgresql.org/) + [pgvector](https://github.com/pgvector/pgvector)
- [Docker](https://www.docker.com/)

---

## 🧠 Future Improvements

- Add authentication
- Advanced filtering (price range, category)
- Switch to `langchain_postgres` PGVector store
- UI polish and error handling

---