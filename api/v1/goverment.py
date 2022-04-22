from fastapi import APIRouter

gover_router = APIRouter(prefix="/goverment")


class goverment():
    def __init__(self):
        self.tasks = ["tsadf","fdsaf"]



gover = goverment()
@gover_router.get("/")
@gover_router.get("")
async def root():
    return {"message": gover.tasks}