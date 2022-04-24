import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import logging
from api import apiv1
from classes import logger, configger

conf_path = "config/base.conf"
main_logger = logger.load_logger(conf_path, _name=__name__)
server = configger.Configger(conf_path, "Server", _logger=main_logger)


app = FastAPI()
app.include_router(apiv1.api_v1_router)


@app.get("/")
async def root():
    return RedirectResponse(apiv1.api_v1_router.prefix)


if __name__ == "__main__":
    uvicorn.run(app, host=server.get("listen", "127.0.0.1"), port=server.get_int("port", "8080"))