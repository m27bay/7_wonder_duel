"""
Logger utilisé dans le projet
"""

import logging


logging.basicConfig(filename="logger_test.log", format='%(asctime)s %(message)s', filemode='w')
_logger_test = logging.getLogger()
_logger_test.setLevel(logging.DEBUG)

logging.basicConfig(filename="logger.log", format='%(asctime)s %(message)s', filemode='w')
_logger_run = logging.getLogger()
_logger_run.setLevel(logging.DEBUG)

logger = _logger_test
