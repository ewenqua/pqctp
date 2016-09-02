#-*- coding=utf-8 -*-

import os
import logging.handlers
from datetime import datetime
from Constant import LOGS_DIR

class FinalLogger:
    logger = None

    levels = {"n": logging.NOTSET,
              "d": logging.DEBUG,
              "i": logging.INFO,
              "w": logging.WARN,
              "e": logging.ERROR,
              "c": logging.CRITICAL}

    log_level = "d"
    today = datetime.today()

    log_file = LOGS_DIR + "final_logger_" + datetime.now().strftime('%Y-%m-%d') +".log"
    log_max_byte = 10 * 1024 * 1024;
    log_backup_count = 5

    @staticmethod
    def getLogger():
        if FinalLogger.logger is not None:
            return FinalLogger.logger

        FinalLogger.logger = logging.Logger("ctp.FinalLogger")
        log_handler = logging.handlers.RotatingFileHandler(filename=FinalLogger.log_file, \
                                                           maxBytes=FinalLogger.log_max_byte, \
                                                           backupCount=FinalLogger.log_backup_count)
        log_fmt = logging.Formatter("[%(asctime)s][%(filename)s][%(funcName)s][%(levelname)s]%(message)s")
        log_handler.setFormatter(log_fmt)
        FinalLogger.logger.addHandler(log_handler)
        FinalLogger.logger.setLevel(FinalLogger.levels.get(FinalLogger.log_level))
        return FinalLogger.logger

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

#if __name__ == "__main__":
logger = FinalLogger.getLogger()
    #logger.debug("this is a debug msg!")

