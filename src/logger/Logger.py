"""
Logger utilisé dans le projet
"""
import logging

class MonLogger:
	def __init__(self, chemin_fichier, nom):
		self.chemin_fichier = chemin_fichier
		self.nom = nom
		logging.basicConfig(filename=self.chemin_fichier + self.nom, format='%(asctime)s %(message)s', filemode='w')
		self.logger = logging.getLogger(self.nom)
		self.logger.setLevel(logging.DEBUG)
		
	def log(self, log: str):
		logger = logging.getLogger(self.nom)
		logger.debug(log)
	

# LOGGER RUN
# LOGGER = MonLogger("src/logger/", "logger.log")
# LOGGER_MINIMAX = MonLogger("src/logger/", "logger_minimax.log")

# LOGGER TEST
# LOGGER = MonLogger("../../src/logger/", "logger.log")
# LOGGER_MINIMAX = MonLogger("../../src/logger/", "logger_minimax.log")
