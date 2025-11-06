from fastapi import FastAPI
from app.db import Base, engine
from app.models import *
from app.routers import receipts, customers, products


app = FastAPI(title="Sales Receipt Backend")

# create tables
Base.metadata.create_all(bind=engine)

app.include_router(receipts.router)
app.include_router(customers.router)
app.include_router(products.router)

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok", "message": "Backend + DB running successfully"}
