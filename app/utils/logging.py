import logging
from logging.handlers import TimedRotatingFileHandler
import os
import glob
import datetime

LOG_DIR = "./log"


def setup_logging():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # TimedRotatingFileHandler 설정
    handler = TimedRotatingFileHandler(
        filename=os.path.join(LOG_DIR, "log_file.txt"),
        when="midnight",
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    handler.suffix = "%Y%m%d"
    handler.setFormatter(logging.Formatter("[ %(asctime)s | %(levelname)s ] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def get_logger(name=None):
    setup_logging()
    return logging.getLogger(name)


def clean_old_logs(days=30):
    now = datetime.datetime.now()
    cutoff = now - datetime.timedelta(days=days)

    log_files = glob.glob(os.path.join(LOG_DIR, "log_file_*.txt"))
    for log_file in log_files:
        # Extract the date from the filename
        try:
            date_str = os.path.basename(log_file).split('_')[-1].split('.')[0]
            file_date = datetime.datetime.strptime(date_str, "%Y%m%d")
            if file_date < cutoff:
                os.remove(log_file)
                print(f"Deleted old log file: {log_file}")
        except ValueError:
            continue


# Example usage
if __name__ == "__main__":
    clean_old_logs(days=30)
