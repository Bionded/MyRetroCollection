from fastapi import APIRouter
from _Old.api.v1 import scanner, goverment

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(scanner.scan_router)
api_v1_router.include_router(goverment.gover_router)

@api_v1_router.get("/")
@api_v1_router.get("")
async def root():

    return {"message": "Hello fdsafd"}