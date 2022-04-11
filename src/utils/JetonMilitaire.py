"""
Fichier de la classe JetonMilitaire.
"""


class JetonMilitaire:
	"""
	Classe representant un jeton militaire.
	"""
	
	def __init__(self, nom, pieces, points_victoire):
		self.nom = nom
		self.est_utilise = False
		self.pieces = pieces
		self.points_victoire = points_victoire
		
	def __eq__(self, other):
		if isinstance(other, JetonMilitaire):
			return self.nom == other.nom
		else:
			return False
		
	def __str__(self):
		return f"JetonMilitaire({self.nom}, {self.pieces}, {self.points_victoire}), " \
			f"est_utilise : {self.est_utilise}"
		