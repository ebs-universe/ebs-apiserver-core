

import os
import logging
import sys
from loguru import logger

from ebs.apiserver.config import LOG_LEVEL
from ebs.apiserver.config import JSON_LOGS
from ebs.apiserver.config import LOG_PATH


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

    logdir = os.path.split(LOG_PATH)[0]
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    logger.add(LOG_PATH, level="INFO",
               rotation="1 week", retention="14 days")
