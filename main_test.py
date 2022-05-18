import random

import pygame

from src.interface_graphique.src.Fenetre import Fenetre
from src.interface_graphique.src.SpriteCarte import SpriteCarte
from src.utils.Carte import Carte
from src.utils.Joueur import Joueur
from src.utils.Plateau import Plateau

if __name__ == '__main__':
	plateau = Plateau(Joueur("joueur"), Joueur("ordi"))
	plateau.preparation_plateau()
	
	# facile = 5
	# normal = 7
	# difficile = 9
	fenetre = Fenetre("7 wonder Duel", plateau, 7)
	fenetre.boucle_principale()