import sys
import logging
from settings import APP_NAME, LOGGERLEVEL

APP_LOGGER_NAME = APP_NAME


def setup_logger(logger_name=APP_LOGGER_NAME, level: int = LOGGERLEVEL, file_name=None, mode: str = 'a'):
    """
    Create a logger with a given name, level, file name, and mode.
    
    :param logger_name: The name of the logger
    :param level: The level of the logger. This is the minimum level that the logger will log
    :type level: int
    :param file_name: The name of the file to which you want to log
    :param mode: a = append, w = overwrite, defaults to a
    :type mode: str (optional)
    :return: A logger object.
    """
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
    """
    Create a child logger for the given module name
    
    :param module_name: The name of the module that will be used to identify the log messages
    :return: A logger object.
    """
    return logging.getLogger(APP_LOGGER_NAME).getChild(module_name)

setup_logger()