from src.utils.Carte import Carte


class CarteGuilde(Carte):
	def __init__(self, nom, effets, couts):
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
		carte_guilde = CarteGuilde(None, None, None)
		
		carte_guilde.nom = self.nom
		
		if self.effets is not None:
			carte_guilde.effets = self.effets.copy()
		
		if self.couts is not None:
			carte_guilde.couts = self.couts.copy()
		
		return carte_guilde