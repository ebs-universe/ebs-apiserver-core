

import os
import logging
import sys
from loguru import logger


# TODO Get these (and other logging controls) from config instead
LOG_LEVEL = logging.getLevelName(os.environ.get("APISERVER_LOG_LEVEL", "INFO"))
JSON_LOGS = True if os.environ.get("APISERVER_JSON_LOGS", "0") == "1" else False
LOGPATH = os.environ.get("APISERVER_LOG_PATH", "/var/log/ebs/apiserver.log")


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging():
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(LOG_LEVEL)

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])

    logdir = os.path.split(LOGPATH)[0]
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    logger.add(LOGPATH, level="INFO",
               rotation="1 week", retention="14 days")
