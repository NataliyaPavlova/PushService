import logging


def get_logger(log_filename: str) -> logging.Logger:
    logging.basicConfig(
        filename=log_filename,
        encoding='utf-8',
        level=logging.INFO
    )
    return logging.getLogger(__name__)
