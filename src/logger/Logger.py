"""
Logger utilisé dans le projet
"""
import logging

class MonLogger:
	def __init__(self):
		logging.basicConfig(filename="src/logger/logger.log", format='%(asctime)s %(message)s', filemode='w')
		self.logger = logging.getLogger()
		self.logger.setLevel(logging.DEBUG)
		
	def log(self, log: str):
		self.logger.debug(log)
	

LOGGER = MonLogger()
