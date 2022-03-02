"""
Fichier classe Jeu
"""
from src.logger.Logger import logger
from src.utils.Joueur import Joueur
from src.utils.Outils import demander_element_dans_une_liste
from src.utils.Plateau import Plateau


class Jeu:
	"""
	Classe Jeu
	"""
	
	def __init__(self, nom_joueur1, nom_joueur2):
		self.plateau = Plateau(Joueur(nom_joueur1), Joueur(nom_joueur2))
		self.plateau.joueur_qui_joue = self.plateau.joueur1
	
	def boucle_principale(self):
		"""
		Boucle principale du plateau
		"""
		
		logger.debug("boucle_principale")
		_nbr_tour = 0
		
		# boucle principale
		while True:
			
			_nbr_tour += 1
			logger.debug(f"\ttour numero : {_nbr_tour}")
			
			if not self.plateau.reste_des_cartes():
				self.plateau.changement_age()
				
			else:
				# le joueur choisit une carte
				carte_choisie = demander_element_dans_une_liste(
					self.plateau.joueur_qui_joue.nom, "carte",
					self.plateau.liste_cartes_prenables()
				)
				
				#
				merveille_a_construire = self.plateau.demander_action_merveille()
				
				sortie_effet = ""
				if merveille_a_construire is not None:
					# le joueur construit la merveille
					sortie_effet = self.plateau.appliquer_effets_merveille(merveille_a_construire)
				else:
					self.plateau.demander_action_carte(carte_choisie)
					self.plateau.appliquer_effets_carte(carte_choisie)
					self.plateau.joueur_qui_joue.cartes.append(carte_choisie)
					
				if sortie_effet != "rejouer":
					self.plateau.joueur_qui_joue = self.plateau.obtenir_adversaire()
	
	def lancer(self):
		"""
		Lance le plateau, prepare le plateau et lance la boucle principale.
		"""
		
		logger.debug("lancer")
		
		self.plateau.preparation_plateau()
		self.boucle_principale()


if __name__ == '__main__':
	jeu = Jeu("j1", "j2")
	jeu.lancer()
