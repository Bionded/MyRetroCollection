from fastapi import APIRouter
from Base.Backend import scanner

scan_router = APIRouter(prefix="/scanner")
scanner = scanner.Rom_scanner()

@scan_router.get("/")
@scan_router.get("")
@scan_router.get("/send/{message}")
async def root(message=''):

    return {"message": scanner.send(message)}


@scan_router.get("/start")
async def start_scan():
    scanner.start_scan()
    return "Done"

@scan_router.get("/start/{folder}")
async def start_scan(folder):
    test = '/Volumes/Bionded/Roms/' + folder

    scanner.start_scan(test)
    return "Done"

@scan_router.get("/returns")
async def start_scan():
    return scanner.governor.get_result()


@scan_router.get("/files")
async def start_scan():
    return scanner.files_dict