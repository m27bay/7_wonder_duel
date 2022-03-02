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
		_raison_fin_de_partie = "none"
		
		# boucle principale
		while _raison_fin_de_partie == "none":
			
			_nbr_tour += 1
			logger.debug(f"\ttour numero : {_nbr_tour}")
			
			if not self.plateau.reste_des_cartes():
				_raison_fin_de_partie, _joueur_gagnant = self.plateau.changement_age()
				
			else:
				# le joueur choisit une carte
				carte_choisie = demander_element_dans_une_liste(
					self.plateau.joueur_qui_joue.nom, "carte",
					self.plateau.liste_cartes_prenables()
				)
				
				#
				merveille_a_construire = self.plateau.demander_action_merveille()
				
				# le joueur construit la merveille
				if merveille_a_construire is not None:
					_raison_fin_de_partie, _joueur_gagnant = self.plateau.appliquer_effets_merveille(merveille_a_construire)
					
					# si l effet est rejouer, _raison_fin_de_partie = none, _joueur_gagnant = "rejouer"
					if _joueur_gagnant == "rejouer":
						continue
				
				else:
					self.plateau.demander_action_carte(carte_choisie)
					
					_raison_fin_de_partie, _joueur_gagnant = self.plateau.appliquer_effets_carte(carte_choisie)
					self.plateau.joueur_qui_joue.cartes.append(carte_choisie)
				
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
