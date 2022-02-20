import sys
import logging
from settings import APP_NAME, LOGGERLEVEL

APP_LOGGER_NAME = APP_NAME


def setup_logger(logger_name=APP_LOGGER_NAME, level: int = LOGGERLEVEL, file_name=None, mode: str = 'a'):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    _formater = logging.Formatter(
        fmt='[%(name)s - %(asctime)s: %(levelname)s] %(message)s')
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(_formater)
    logger.handlers.clear()
    logger.addHandler(handler)

    if file_name:
        file_handler = logging.FileHandler(file_name, mode=mode)
        file_handler.setFormatter(_formater)
        logger.addHandler(file_handler)

    return logger


def get_logger(module_name):
    return logging.getLogger(APP_LOGGER_NAME).getChild(module_name)
