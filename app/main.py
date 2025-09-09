from fastapi import FastAPI
from app.api.v1 import device_router, rack_router
from app.config import settings


app = FastAPI()

# Include routers
app.include_router(device_router.router, prefix=f"{settings.API_ROUTE}/devices", tags=["devices"])
app.include_router(rack_router.router, prefix=f"{settings.API_ROUTE}/racks", tags=["racks"])


@app.get("/")
async def root():
    return {"message": settings.PROJECT_DESC}