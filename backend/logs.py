import logging
import sys


def create_logger(name, level=logging.INFO):
    LOGGER = logging.getLogger(name)
    LOGGER.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter('%(asctime)s * %(name)s * %(levelname)s * %(message)s'))
    LOGGER.addHandler(stream_handler)
    return LOGGER