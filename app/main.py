from fastapi import FastAPI
from app.db import Base, engine

app = FastAPI(title="Sales Receipt Backend")

# Just ensure DB engine can connect
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database connected successfully")
except Exception as e:
    print("❌ Database connection failed:", e)

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok", "message": "Backend is running successfully!"}
