from fastapi import APIRouter
from _Old.Base.Backend import scanner

scan_router = APIRouter(prefix="/scanner")
scanner = scanner.Rom_scanner()

@scan_router.get("/")
@scan_router.get("")
@scan_router.get("/send/{message}")
async def root(message=''):

    return {"message": scanner.send(message)}


@scan_router.get("/import/{folder}")
async def start_import(folder):
    test = '/Volumes/Bionded/Roms/gba/gamelist.xml'
    ret = scanner.import_collection(test, folder)


@scan_router.get("/files")
async def start_scan():
    return scanner.files_dict