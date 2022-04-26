from src.utils.Carte import Carte


class Merveille(Carte):
	def __init__(self, nom, effets, couts):
		super().__init__(nom, effets, couts, None, None, None)
		self.est_construite = False
		
	def __str__(self):
		"""
		Renvoie une chaine pour afficher les attributs.

		:return: chaine avec les attributs de la classe.
		"""
		return f"nom : {self.nom}, " \
			f"effets : {str(self.effets)}, " \
			f"couts : {str(self.couts)}, " \
			f"est_construite {self.est_construite}"
	
	def constructeur_par_copie(self):
		merveille = Merveille(None, None, None)
		
		merveille.nom = self.nom
		
		if self.effets is not None:
			merveille.effets = self.effets.copy()
			
		if self.couts is not None:
			merveille.couts = self.couts.copy()
			
		merveille.est_construite = self.est_construite
		
		return merveille
	