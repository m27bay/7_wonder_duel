"""
Fichier de la classe JetonMilitaire.
"""

from src.utils.Affichable import Affichable


class JetonMilitaire(Affichable):
	"""
	Classe representant un jeton militaire.
	"""
	
	def __init__(self, nom, chemin_image, pieces, points_victoire):
		super().__init__(nom, chemin_image)
		self.est_utilise = False
		self.pieces = pieces
		self.points_victoire = points_victoire
		