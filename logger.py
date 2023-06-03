import datetime
from typing import Callable, Any

class Logger:
    logger: Callable[[Any], None] = lambda _: print("no logger")
    formatter = "{} - {}\t>\t{}"
    silent = False

    @staticmethod
    def set_logger(logger: Callable[[Any], None]):
        Logger.logger = logger

    @staticmethod
    def format(log_level: str, msg: str):
        date = datetime.datetime.now().time()
        return Logger.formatter.format(date, log_level, msg)

    @staticmethod
    def info(msg: str):
        if Logger.silent: return
        Logger.logger(Logger.format("INFO", msg))

    @staticmethod
    def success(msg: str):
        if Logger.silent: return
        Logger.logger(Logger.format("SUCCESS", msg))

    @staticmethod
    def failure(msg: str):
        if Logger.silent: return
        Logger.logger(Logger.format("FAILURE", msg))
