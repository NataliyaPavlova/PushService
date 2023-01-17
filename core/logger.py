import logging
import sys


def get_logger(log_filename: str) -> logging.Logger:
    file_handler = logging.FileHandler(filename=log_filename)
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    handlers = [file_handler, stdout_handler]

    logging.basicConfig(
        encoding='utf-8',
        level=logging.INFO,
        handlers=handlers,
    )
    return logging.getLogger(__name__)
