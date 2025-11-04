
---

# backend/README.md
# Sales Receipt App – Backend

FastAPI backend for the Sales Receipt App.

## Tech Stack
- FastAPI
- PostgreSQL (via SQLAlchemy)
- Docker (PostgreSQL container)
- Pydantic & Alembic

## Setup
1. Run PostgreSQL (see docker-compose.yml in root project)
2. Create virtual environment and install dependencies  
   ```bash
   pip install -r requirements.txt
3. To start the backen project
    uvicorn app.main:app --reload