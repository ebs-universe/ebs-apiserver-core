

from uvicorn import Config, Server
from fastapi import FastAPI

from .log import setup_logging

from ebs.apiserver.config import BIND_IP
from ebs.apiserver.config import PORT
from ebs.apiserver.config import LOG_LEVEL

app = FastAPI()


def run_server():
    server = Server(
        Config(
            app,
            host=BIND_IP,
            port=PORT,
            log_level=LOG_LEVEL,
        ),
    )
    # setup logging last, to make sure no library overwrites it
    # (they shouldn't, but it happens)
    setup_logging()
    server.run()
