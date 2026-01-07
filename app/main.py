from fastapi import FastAPI
from app.database import Base, engine
from app.models import *
from app.routers import receipts, customers, products, dashboard, upload, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Sales Receipt Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(auth.router)
app.include_router(receipts.router)
app.include_router(customers.router)
app.include_router(products.router)
app.include_router(dashboard.router)
app.include_router(upload.router)

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok", "message": "Backend + DB running successfully"}
