"""
Fichier classe Jeu
"""

from src.utils.Joueur import Joueur
from src.utils.Outils import demander_element_dans_une_liste
from src.utils.Plateau import Plateau


class Jeu:
	"""
	Classe Jeu
	"""
	
	def __init__(self, nom_joueur1, nom_joueur2):
		self.plateau = Plateau(Joueur(nom_joueur1), Joueur(nom_joueur2))
	
	def boucle_principale(self):
		"""
		Boucle principale du plateau
		"""
		
		self.plateau.joueur_qui_joue = self.plateau.joueur1
		while True:
			if not self.plateau.reste_des_cartes():
				# changement d'age
				self.plateau.age += 1
				self.plateau.preparation_cartes()
			else:
				carte_choisie = demander_element_dans_une_liste(
					self.plateau.joueur_qui_joue.nom, "carte_a_enlever",
					self.plateau.liste_cartes_prenables()
				)
				self.plateau.demander_action_carte(carte_choisie)
				self.plateau.appliquer_effets_carte(carte_choisie)
				self.plateau.joueur_qui_joue.cartes.append(carte_choisie)
				
				merveille = self.plateau.demander_action_merveille()
				sortie_effet = ""
				if merveille is not None:
					sortie_effet = self.plateau.appliquer_effet_merveille(merveille)
				
				if sortie_effet != "rejouer":
					self.plateau.joueur_qui_joue = self.plateau.obtenir_adversaire()
				
				else:
					self.plateau.fin_de_partie("cartes_vide")
					break
	
	def lancer(self):
		"""
		Lance le plateau, prepare le plateau et lance la boucle principale.
		"""
		
		self.plateau.preparation_plateau()
		self.boucle_principale()


if __name__ == '__main__':
	jeu = Jeu("pierre", "paul")
	jeu.lancer()
