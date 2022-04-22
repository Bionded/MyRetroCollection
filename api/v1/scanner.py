from fastapi import APIRouter

scan_router = APIRouter(prefix="/scanner")


@scan_router.get("/")
@scan_router.get("")
async def root():
    return {"message": "Hello scanner"}