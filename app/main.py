from fastapi import FastAPI
from app.api.v1.endpoints import device, rack
from app.config import settings


app = FastAPI()

# Include routers
app.include_router(device.router, prefix=f"{settings.API_V1_STR}/devices", tags=["devices"])
app.include_router(rack.router, prefix=f"{settings.API_V1_STR}/racks", tags=["racks"])


@app.get("/")
async def root():
    return {"message": "Data Center Infrastructure Management API"}