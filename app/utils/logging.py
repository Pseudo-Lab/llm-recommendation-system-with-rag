import logging

def setup_logging():
    logging.basicConfig(
        filename="./log_file.txt",
        level=logging.DEBUG,
        format="[ %(asctime)s | %(levelname)s ] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def get_logger(name=None):
    setup_logging()
    return logging.getLogger(name)
