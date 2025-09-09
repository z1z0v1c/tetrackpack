from fastapi import FastAPI
from api.v1 import device_router, rack_router
from config import settings


app = FastAPI()

# Include routers
app.include_router(device_router.router, prefix=f"{settings.API_V1_STR}/devices", tags=["devices"])
app.include_router(rack_router.router, prefix=f"{settings.API_V1_STR}/racks", tags=["racks"])


@app.get("/")
async def root():
    return {"message": "Data Center Infrastructure Management API"}