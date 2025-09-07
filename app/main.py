from fastapi import FastAPI
from app.api.v1.endpoints import device
from app.config import settings


app = FastAPI()

# Include routers
app.include_router(device.router, prefix=f"{settings.API_V1_STR}/devices", tags=["devices"])

@app.get("/")
async def root():
    return {"message": "Data Center Infrastructure Management API"}