"""
Fichier de la classe JetonProgres
"""



class JetonProgres:
	"""
	Classe representant un jeton progres.
	"""
	
	def __init__(self, nom, effets):
		"""
		Constructeur de la classe JetonProgres.

		:param nom: nom du jeton.
		:param effets: liste des effets du jeton.
		"""
		self.nom = nom
		self.effets = effets
	
	def __str__(self):
		"""
		Renvoie une chaine pour afficher les attributs.

		:return: chaine avec les attributs de la classe.
		"""
		return f"nom : {self.nom}, " \
			f"effets : {str(self.effets)}"