

from uvicorn import Config, Server

from .log import setup_logging

# TODO Should an empty Application Object be created here instead of leaving it to the client?

from ebs.apiserver.config import BIND_IP
from ebs.apiserver.config import PORT
from ebs.apiserver.config import LOG_LEVEL


def run_server(server_object):
    server = Server(
        Config(
            server_object,
            host=BIND_IP,
            port=PORT,
            log_level=LOG_LEVEL,
        ),
    )
    # setup logging last, to make sure no library overwrites it
    # (they shouldn't, but it happens)
    setup_logging()
    server.run()
