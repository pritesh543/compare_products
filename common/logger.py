"""
This is logger file which produce
logger object to write into log files
"""

import logging
import logging.config

from .logconfig import LOGGING
logging.config.dictConfig(LOGGING)

# how to use log
# first import CustomLogger  and then call  CustomLogger.get_get_logger(__main__)
# from common.logger import CustomLogger
# logger = CustomLogger.get_logger(__name__)
# use logger.log(msg)

class CustomLogger(object):
    @classmethod
    def get_logger(cls, name=__name__):
        return logging.getLogger(name)
