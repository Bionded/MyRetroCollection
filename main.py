import uvicorn
from fastapi import FastAPI
from api import apiv1
app = FastAPI(prefix="/api/v1")
app.include_router(apiv1.api_v1_router)


@app.get("/")
async def root():
    bash = "fdsafd"
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)