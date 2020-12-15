import logging


def init_logger():
    root_logger = logging.getLogger(__name__)
    logging.getLogger().setLevel("INFO")
    return root_logger


logger = init_logger()
