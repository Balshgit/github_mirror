import importlib.util
import logging
import sys
import time
from collections import Counter
from threading import Thread
from typing import List

# use loguru if it is possible for color output
if importlib.util.find_spec('loguru') is not None:
    from loguru import logger
    logger.remove()
    logger.add(sink=sys.stdout, colorize=True, level='DEBUG',
               format="<cyan>{time:DD.MM.YYYY HH:mm:ss}</cyan> | <level>{level}</level> | "
                      "<magenta>{message}</magenta>")

# use standard logging
else:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    log_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    console_handler.setFormatter(log_formatter)

    logger.addHandler(console_handler)


def threads_ready_statistic(threads: List[Thread]):
    """
    Getting information how many threads are running right now

    :param threads: List of active threads
    """
    while True:
        threads_statistic = [thread.is_alive() for thread in threads]
        statistic = Counter(threads_statistic)
        ready_count = statistic.get(False, 0)
        percent = int(ready_count / len(threads) * 100)
        time.sleep(1)
        if 0 < percent < 100:
            logger.info(f'Ready: {percent}%')
        if not any(threads_statistic):
            logger.info(f'Ready: 100%')
            break
