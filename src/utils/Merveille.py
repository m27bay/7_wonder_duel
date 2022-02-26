"""
Fichier de la classe Merveille.
"""

from src.utils.Carte import Carte


class Merveille(Carte):
	"""
	Classe representant une merveille, une classe fille de la classe Carte.
	"""
	
	def __init__(self, nom, chemin_image, effets, couts):
		"""
		Constructeur de la classe Merveille.

		:param nom: nom de la merveille.
		:param chemin_image: chemin pour afficher la merveille.
		:param effets: liste d effets que donne la merveille respectant un pattern precis.
		:param couts: liste de couts pour construire la merveille respactant un pattern precis.
		"""
		super().__init__(nom, chemin_image, effets, couts, None, None, None)
		
	def __str__(self):
		"""
		Renvoie une chaine pour afficher les attributs.

		:return: chaine avec les attributs de la classe.
		"""
		return f"nom : {self.nom}, " \
			f"image : {self.chemin_image}, " \
			f"effets : {str(self.effets)}, " \
			f"couts : {str(self.couts)}"
		