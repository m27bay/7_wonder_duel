"""
Fichier de la classe CarteFille.
"""

from src.utils.Carte import Carte


class CarteFille(Carte):
	"""
	Classe representant une CarteFille, une merveille ou un carte guilde
	elle ont ni de carte de chainage, ni couleur, ni d age.
	"""
	
	def __init__(self, nom, effets, couts):
		"""
		Constructeur de la classe CarteFille.

		:param nom: nom de la CarteFille.
		:param effets: liste d effets que donne la CarteFille respectant un pattern precis.
		:param couts: liste de couts pour construire la CarteFille respactant un pattern precis.
		"""
		super().__init__(nom, effets, couts, None, None, None)
		
	def __str__(self):
		"""
		Renvoie une chaine pour afficher les attributs.

		:return: chaine avec les attributs de la classe.
		"""
		return f"nom : {self.nom}, " \
			f"effets : {str(self.effets)}, " \
			f"couts : {str(self.couts)}"
	
	def constructeur_par_copie(self):
		carte_fille = CarteFille(None, None, None)
		
		carte_fille.nom = self.nom
		
		if self.effets is not None:
			carte_fille.effets = self.effets.copy()
			
		if self.couts is not None:
			carte_fille.couts = self.couts.copy()
		
		return carte_fille
	