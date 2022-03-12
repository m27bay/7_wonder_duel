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
		