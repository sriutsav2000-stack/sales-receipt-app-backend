from fastapi import FastAPI
from app.database import Base, engine
from app.models import *
from app.routers import receipts, customers, products, dashboard, upload
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Sales Receipt Backend")

# origins = [
#     "http://localhost:8100",
#     "http://127.0.0.1:8100"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create tables
Base.metadata.create_all(bind=engine)

app.include_router(receipts.router)
app.include_router(customers.router)
app.include_router(products.router)
app.include_router(dashboard.router)
app.include_router(upload.router)

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok", "message": "Backend + DB running successfully"}
