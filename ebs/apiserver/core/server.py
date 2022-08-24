

import os
from uvicorn import Config, Server
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .log import setup_logging

from ebs.apiserver.config import INSTANCE_ROOT

import logging
logger = logging.getLogger(__name__)


core_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)

app = FastAPI()


def server_basic_options():
    from ebs.apiserver.config import BIND_IP
    from ebs.apiserver.config import PORT
    from ebs.apiserver.config import LOG_LEVEL
    from ebs.apiserver.config import AUTO_RELOAD

    return {
        "host": BIND_IP,
        "port": PORT,
        "log_level": LOG_LEVEL,
        "reload": AUTO_RELOAD,
    }


def _default_certificates():
    return {
        'ssl_keyfile': os.path.join(core_dir, 'resources', 'test_key.pem'),
        'ssl_certfile': os.path.join(core_dir, 'resources', 'test_certificate.pem'),
    }


def server_ssl_options():
    from ebs.apiserver.config import ENABLE_SSL
    if not ENABLE_SSL:
        return {}

    from ebs.apiserver.config import SSL_KEYFILE
    from ebs.apiserver.config import SSL_CERTFILE

    if not SSL_KEYFILE or not SSL_CERTFILE:
        logger.warning("ENABLE_SSL is True but SSL_KEYFILE and/or SSL_CERTFILE not set. "
                       "Falling back to built-in test certificates.")
        return _default_certificates()

    if not os.path.isabs(SSL_KEYFILE):
        SSL_KEYFILE = os.path.join(INSTANCE_ROOT, SSL_KEYFILE)
    if not os.path.isabs(SSL_CERTFILE):
        SSL_CERTFILE = os.path.join(INSTANCE_ROOT, SSL_CERTFILE)

    if not os.path.exists(SSL_KEYFILE) or not os.path.exists(SSL_CERTFILE):
        logger.warning("Configured SSL_KEYFILE and/or SSL_CERTFILE not found. "
                       "Falling back to built-in test certificates.")
        return _default_certificates()

    return {
        'ssl_keyfile': SSL_KEYFILE,
        'ssl_certfile': SSL_CERTFILE
    }


def prepare_app():
    from ebs.apiserver.config import CORS_ORIGINS
    from ebs.apiserver.config import CORS_METHODS
    from ebs.apiserver.config import CORS_HEADERS

    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=CORS_METHODS,
        allow_headers=CORS_HEADERS
    )


def run_server():
    server_opts = server_basic_options()
    server_opts.update(server_ssl_options())

    prepare_app()

    server = Server(
        Config(
            app,
            **server_opts
        ),
    )
    # setup logging last, to make sure no library overwrites it
    # (they shouldn't, but it happens)
    setup_logging()
    server.run()
