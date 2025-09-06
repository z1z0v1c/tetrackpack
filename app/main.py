from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Data Center Infrastructure Management API"}