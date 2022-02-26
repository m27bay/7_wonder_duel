"""
Fichier de la classe JetonProgres
"""

from src.utils.Affichable import Affichable


class JetonProgres(Affichable):
	"""
	Classe representant un jeton progres.
	"""
	
	def __init__(self, nom, chemin_image, effets):
		"""
		Constructeur de la classe JetonProgres.

		:param nom: nom du jeton.
		:param effets: liste des effets du jeton.
		"""
		super().__init__(nom, chemin_image)
		self.effets = effets
	
	def __str__(self):
		"""
		Renvoie une chaine pour afficher les attributs.

		:return: chaine avec les attributs de la classe.
		"""
		return f"nom : {self.nom}, " \
			f"chemin_image : {self.chemin_image}, " \
			f"effets : {str(self.effets)}"