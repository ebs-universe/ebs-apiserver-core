

import os
import logging
from uvicorn import Config, Server

from .log import setup_logging

# TODO Get these (and other server controls) from config instead
PORT = int(os.environ.get("APISERVER_PORT", "8039"))
LOG_LEVEL = logging.getLevelName(os.environ.get("APISERVER_LOG_LEVEL", "INFO"))


def run_server(server_object):
    server = Server(
        Config(
            server_object,
            host="0.0.0.0",
            port=PORT,
            log_level=LOG_LEVEL,
        ),
    )
    # setup logging last, to make sure no library overwrites it
    # (they shouldn't, but it happens)
    setup_logging()
    server.run()
