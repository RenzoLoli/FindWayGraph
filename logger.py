import datetime
from typing import Callable, Any

class Logger:
    logger: Callable[[Any, str], None] = lambda _, __: print("no logger")
    formatter = "{} - {}\t>\t{}"
    silent = False

    @staticmethod
    def set_logger(logger: Callable[[Any, str], None]):
        Logger.logger = logger

    @staticmethod
    def format(log_level: str, msg: str):
        date = datetime.datetime.now().time()
        return Logger.formatter.format(date, log_level, msg)

    @staticmethod
    def info(msg: str):
        if Logger.silent: return
        Logger.logger(Logger.format("INFO", msg), 'info')

    @staticmethod
    def warn(msg: str):
        if Logger.silent: return
        Logger.logger(Logger.format("WARN", msg), 'warn')

    @staticmethod
    def error(msg: str):
        if Logger.silent: return
        Logger.logger(Logger.format("FAIL", msg), 'error')
