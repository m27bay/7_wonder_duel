"""
Logger utilisé dans le projet
"""

import logging


logging.basicConfig(filename="logger_test.log", format='%(asctime)s %(message)s', filemode='w')
logger_test = logging.getLogger()
logger_test.setLevel(logging.DEBUG)

logging.basicConfig(filename="logger.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
