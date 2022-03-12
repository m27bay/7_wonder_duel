"""
Logger utilisé dans le projet
"""

import logging


mode = "run"
# mode = "test"

chemin_logger = ""
if mode == "run":
	# chemin_logger = "../logger/logger.log"
	chemin_logger = "../../logger/logger.log"
elif mode == "test":
	chemin_logger = "../../src/logger/logger_test.log"

logging.basicConfig(filename=chemin_logger, format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
