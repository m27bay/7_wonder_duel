import pygame

from src.interface_graphique.src.Fenetre import Fenetre
from src.interface_graphique.src.FenetreDefausserCarteCouleur import FenetreDefausserCarteCouleur
from src.interface_graphique.src.SpriteCarte import SpriteCarte
from src.utils.Carte import Carte
from src.utils.Joueur import Joueur
from src.utils.Plateau import Plateau

if __name__ == '__main__':
	# plateau = Plateau(Joueur("joueur"), Joueur("ordi"))
	# plateau.preparation_plateau()
	
	# facile = 5
	# normal = 7
	# difficile = 9
	# fenetre = Fenetre("7 wonder Duel", plateau, 7)
	# fenetre.boucle_principale()
	
	test = FenetreDefausserCarteCouleur()
	liste_sprite_carte = pygame.sprite.Group()
	liste_carte = [Carte("verrerie", ["ressource verre 1"], ["monnaie 1"], None, "gris", age=1),
		Carte("presse", ["ressource papyrus 1"], ["monnaie 1"], None, "gris", age=1),
		Carte("soufflerie", ["ressource verre 1"], None, None, "gris", age=2),
		Carte("sechoir", ["ressource papyrus 1"], None, None, "gris", age=2)]
	
	coordx = 0
	coordy = 0
	for carte in liste_carte:
		liste_sprite_carte.add(SpriteCarte(carte, coordx, coordy, 0.15))
		coordx += 10
	
	test.set_liste_sprite_carte(liste_sprite_carte)
	test.dessiner_cartes()
	test.boucler_principale()